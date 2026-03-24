# 预研：application-native runtime observation and observability planes

## Trigger

- 这轮 Freely 自举里，用户明确指出“固定 90 秒观察窗口”不如先看会话 `jsonl`、cycle log 和当前态末尾信号。
- 现有 `live-status` 已经解决了“当前谁在跑、在做什么”的最小 CLI 面，但还没有把“如何判断仍在推进 / 已经空转 / 已具备插话着力点”收成统一协议。
- Freely 未来要开发任意应用，不能把 `live-status / fleet-status / jsonl / cycle log` 写死成通用观察法；这些只是 Freely 自举时最先落地的 concrete profile。
- CLI / TUI / GUI / future API 都需要暴露当前应用的运行态给用户观察、插话和回放；多个 worktree、多个 subagent、多个会话/日志也要能被同一控制面解释，但不同应用的具体 surface 可以不同。

## Problem

当前仓库已经有三块相关能力，但缺桥：

1. `watchdog live-status surface` 解决了最小 current-state surface。
2. `pre-test-merge acceptance stall` 在收窄“什么时候 delegated continuation 真 stall”。
3. `frontend probe dogfooding loop` 在讨论用户可观察、可打断、可回放的产品面。

缺的部分是：

- 什么叫“应用原生真实环境测试”的观察协议。
- 主管、watchdog、用户插话之前，应该按什么顺序读哪些证据面。
- 多个状态平面、会话平面、流式日志平面、fleet 平面之间如何对应。
- 如何把 Freely 自己的观测信号泛化成未来任意应用都能消费的 contract。

## Direction

不要把这条线写成“继续扩 live-status”，也不要把它收缩成“stall 检测技巧”。

更合适的能力边界是：

- `application-native runtime observation contract`
- `observability planes for CLI / TUI / GUI / future API`

它应该回答：

1. 当前应用有哪些 observation surfaces。
2. 哪些 surface 回答“现在谁在干活、在干什么”。
3. 哪些 surface 回答“这个 loop 还在推进还是已空转”。
4. 哪些 surface 回答“用户应该往哪个状态、哪个会话、哪个 artifact 插话”。
5. 哪些 surface 回答“什么时候测试真正通过，什么时候还不能删 worktree”。

## Proposed Planes

### 1. Current-state plane

回答：

- 当前有哪些 runtime / manager / worker / subagent 活着
- 每个 worktree 当前 phase / ownership / desired state 是什么
- 当前 continuity / prompt 聚焦点是什么

Freely 当前 concrete profile：

- `live-status`
- `fleet-status`
- `manager continuity`
- `worker prompts`

### 2. Session plane

回答：

- 当前状态对应哪个会话
- 哪个 `tool / session_id / jsonl_path / cycle_log / prompt_file` 是深挖入口
- 多个 worktree、多个 subagent 的会话如何映射回同一 topic / lane

Freely 当前 concrete profile：

- `session_refs`
- `~/.codex/sessions/**/*.jsonl`
- `.freely/logs/cycle-*.log`
- `.freely/run/prompt-*.txt`

### 3. Stream plane

回答：

- 当前有哪些实时日志 / 事件流可看
- 默认展示多少，何时展开
- 如何从“状态卡片”跳到实时流
- 具体 transport 可以是日志、事件流、trace、console 或其他应用原生 stream，只要能提供 tail 和 deep ref

Freely 当前 concrete profile：

- cycle log tail
- session jsonl tail

### 4. Fleet plane

回答：

- 多 worktree / 多 lane / 多 subagent 的全局排班视图
- 哪些 active / queued / frozen / stale / retire-candidate
- 哪些 lane 是 manager-owned，哪些是 worker-owned

Freely 当前 concrete profile：

- `fleet-status`
- milestone / issue / progress / recovery

### 5. Artifact plane

回答：

- continuity、resolution、verification、cleanup、pre-tests 等 canonical artifact 在哪里
- 当前 loop 是卡在 artifact 未生成、未消费，还是测试未完成

Freely 当前 concrete profile：

- interruption intake / resolution
- manager continuity
- worker continuity
- verification / cleanup evidence
- issue `pre-tests.md`

## Observation Order

本线的核心不是时间阈值，而是先观察“是否有前进信号”。

推荐顺序：

1. current-state plane
2. stream plane 的 tail（最后 10-20 行）
3. artifact plane 的增量
4. fleet plane 的状态冲突
5. 时间阈值只作为最后 watchdog fallback

对 Freely 自举来说，当前 concrete 顺序是：

1. `freely live-status`
2. 最新 cycle log tail
3. 对应 session jsonl tail
4. `manager-continuity` / `worker-prompts` / `live-status` generated-consumed delta
5. 需要全项目判断时再看 `fleet-status`
6. 超过 stall threshold 仅作为最后兜底

## Boundary

本线不直接实现：

- 新的 stall recovery runtime patch
- 新的 TUI / GUI 页面
- 新的 JSON API server

本线先冻结：

- observation planes 词典
- application-native observation contract
- Freely self-host concrete profile
- 与现有 `live-status` issue、stall candidate、frontend probe 的依赖关系

## Coordination With Existing Lines

### 与 `I-20260320-1945` 的关系

- `I-20260320-1945` 已完成最小 `live-status` surface。
- 本线不是重开它，而是定义后续如何把 `live-status` 放进更大的 observation planes 框架。
- 若未来需要扩 CLI/TUI/API 的多平面暴露，可回到该 issue 族或由本线 materialize 新 issue 承接。

### 与 `C-20260322-0715-A` 的关系

- `0715` 关注 delegated acceptance stall 何时成立。
- 本线为它提供上游观察协议：先看哪些 plane、哪些 tail、哪些 artifact delta。
- `0715` 不应自己再定义一套独立观察顺序。

### 与 frontend probe 的关系

- frontend probe 关注产品界面和交互承载。
- 本线定义这些界面/接口到底应该展示哪些 plane、怎么让用户找到插话着力点。
- 也就是说，本线是 probe/UI 的信息架构与观测 contract 上游。

## Intended Landing

若后续边界稳定，最终真源预计会落到：

- `docs/system/workspace/skills/multi-worktree-supervision/**`
- `docs/system/workspace/skills/watchdog-control-plane/**`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/tools.md`
- CLI / TUI / GUI / future API 的状态 surface 真源
