# 研究：Token 节省型会话连续性、轮换与证据引用

## Context

- 日期：2026-03-19
- 触发：Freely 当前已经具备 `context_ratio` / `context compacted` / `fresh_with_handoff` / handoff 文件等能力，但“如何在免交互 Codex 模式下以更省 token 的方式保住上下文”仍未完全收敛。
- 当前暴露问题：
  - Codex CLI 在非交互模式下没有公开的“带 session id 触发压缩/总结”的参数。
  - 仅靠脚本在会话退出后写 handoff，质量上限偏低，且会重复消耗 token。
  - 若把整份旧 `jsonl` 或大段旧日志重新喂给新会话，会浪费 token，且不一定比模型内压缩更好。
  - 目前 `context warn`、`fresh_with_handoff`、manager bootstrap handoff、continuity artifact 之间已经有能力雏形，但缺统一口径和场景边界。

## 核心判断

这不是单一“压缩策略”问题，而是三层能力协作问题：

1. **优先级最高的是 AI 还活着时的主动 continuity**
   - 当 `context_ratio` 达到 warn 阈值时，应先推动当前会话更新当前阶段的 continuity artifact，而不是立刻强制外部轮换。
   - 这一步是高质量交接的主路。

2. **`fresh_with_handoff` 是脚本层轮换，不是模型内压缩**
   - 在官方 CLI 没有非交互压缩参数的前提下，Freely 只能通过：
     - 记录 `session_id`
     - 记录 `jsonl_path`
     - 写 handoff / continuity
     - 启动新 `codex exec`
     来实现“新会话续接”。
   - 这条链是必要 fallback，但不该被误认为“高质量压缩”。

3. **旧会话证据应按需引用，不应默认整份重喂**
   - `previous_tool_session_id`
   - `previous_tool_jsonl_path`
   - `previous_cycle_log`
   这些信息对恢复有价值，但默认应作为“可追溯证据路径”，而不是大段 prompt 主体。
   - 新会话默认应优先读取：
     - phase-appropriate continuity artifact
     - session handoff
     - 少量结构化状态
   - 只有确实需要时，再按需读取旧 `jsonl` / log 片段。

4. **watchdog 不负责压缩**
   - 若 AI 已死，watchdog 只负责切号、等待、拉起主管或 worker。
   - 总结/continuity 应尽可能在 AI 还能输出时完成。

5. **它不是与 auto-loop 并列的新 loop，而是 auto-loop 的正式子控制面**
   - `auto-loop runtime` 负责持续运行、选择 `resume` / `fresh_with_handoff`、维护 session state。
   - `context/session continuity` 负责定义：
     - 何时先 continuity
     - 何时 rotate
     - 新会话默认携带哪些最小上下文
     - 何时允许按需读取旧 `jsonl` / log
   - `global watchdog` 负责在 AI 已经无能为力、甚至主管/worker runtime 都不在时，把主管重新拉起。
   - 因此这条能力与 auto-loop 有重叠，但不是替代关系，而是“runtime 中的上下文治理子系统 + 外层脚本兜底”的关系。

## 场景拆分

### 1. Context warn，但当前会话仍健康

- 触发：`context_ratio >= warn`
- 动作：
  - prompt 注入“先更新 continuity artifact”
  - 当前 AI 先写进度/continuity
  - 视情况继续当前会话，不必立刻 fresh

### 2. Context rotate，旧会话不值得继续

- 触发：
  - `context compacted`
  - `context_ratio >= rotate`
  - `resume_streak` 超阈值
  - `route_only_handoff` 连续发生
- 动作：
  - runtime 写 `Session Handoff`
  - 新起 `codex exec`
  - handoff 与 continuity 一起进入下一轮 prompt

### 3. 会话已退出，但仍需低 token 恢复

- 动作：
  - 新会话默认只使用：
    - continuity artifact
    - handoff
    - `previous_*_path` 引用
  - 如果需要复核细节，再自己按需读取旧 `jsonl` / log 的局部内容

### 4. AI 已完全无能为力

- 例如：
  - 账号限额
  - 认证失败
  - 进程已退出
  - manager / worker 不存在
- 动作：
  - 由 global watchdog / runtime 脚本恢复
  - 不要求 watchdog 代替 AI 生成高质量总结

### 5. auto-loop / context management / watchdog 的协作

- `auto-loop runtime`
  - 监测 AI 退出
  - 选择 `resume` / `fresh_with_handoff`
  - 写 session state / handoff
- `context/session continuity controller`
  - 决定 continuity 的默认目标和轮换时机
  - 控制新会话默认消费哪些上下文、保留哪些路径引用
- `global watchdog`
  - 当 AI 服务不可用、账号失效、主管 runtime 不存在时，恢复主管入口
  - 不负责业务编排，也不负责替 AI 写语义总结

说明：
- “旧进程没了，需要重启并继续”与“该给新进程带哪些上下文”是相邻但不同的职责。
- 前者属于 runtime/watchdog，后者属于 context/session management。

## 最小可行落点

### 1. 统一 continuity/rotation 口径

- 将以下信号统一到一条运行时口径：
  - `context warn`
  - `context rotate`
  - `fresh_with_handoff`
  - `continuity refresh`
  - `session evidence references`

### 2. 明确 handoff 的主次内容

- 主内容：
  - continuity artifact
  - 当前 issue / phase / branch / worktree / fleet snapshot
- 次内容：
  - `session_id`
  - `jsonl_path`
  - `cycle_log`
  - recent excerpt

### 3. 建立“按需引用旧会话证据”的规则

- 在 handoff 中始终保留 `previous_tool_jsonl_path`
- 新会话默认不全文读取
- 只有当 continuity/handoff 无法回答当前问题时，才允许按需读取旧证据

### 4. 主管 continuity 单独定义

- worker continuity 以 issue / phase 为中心
- manager continuity 以 fleet / delegation / blocked workers / promote queue 为中心

### 5. 明确与 auto-loop 的集成边界

- 不把这条能力设计成新的平行 loop。
- 它应作为 `auto-loop` 的正式组成部分被实现：
  - 内层：`runtime/freely` 的 session/rotation/continuity 决策
  - 外层：`ensure-manager --watch` 负责 AI 无能为力时的恢复入口
- 若未来引入独立的全局上下文 watchdog，也应被视为 `auto-loop` 的外层守护，而不是替代 `auto-loop` 自身。

### 6. 形成触发矩阵而不是散落提示

- 必须形成一份统一矩阵，至少包含：
  - `trigger`
  - `owner`
  - `artifact`
  - `action`
  - `fallback`
- 最小覆盖场景：
  - `context warn, AI still healthy`
  - `context rotate`
  - `AI exited but auto-loop still alive`
  - `manager/worker runtime vanished`
  - `global account/service unavailable`
- 这样后续实现时才不会把：
  - 进度文档更新
  - `fresh_with_handoff`
  - manager bootstrap
  - watchdog 拉起
 误做成重复能力。

## 约束

- 在官方公开支持非交互压缩参数前，不假定 Codex CLI 有可调用的压缩命令。
- 不把“整份旧 jsonl 重新喂给新会话”作为默认主路。
- watchdog 只负责脚本恢复，不负责替 AI 做语义压缩。
- 若未来引入独立上下文 watchdog，其职责仍应受 `auto-loop` 编排约束，不得抢占 manager / worker 的业务判断。
