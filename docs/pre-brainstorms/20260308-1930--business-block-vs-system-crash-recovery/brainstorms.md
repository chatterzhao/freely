# 研究：业务阻塞与系统崩溃恢复分层

日期：2026-03-08 19:30 UTC

## 背景

在 `phase_state` 词典收敛之后，又暴露出一个更底层的问题：

1. `blocked_*` 应该只表示 AI 已识别并显式交接的业务阻塞。
2. PID 消失、CLI 崩溃、会话断裂，则属于系统崩溃，不一定来得及有 AI 交接。
3. auto-loop 监控发现系统事件后，不能直接把条目标记成 `blocked_*`，而必须先恢复定位“刚才在做什么”。

如果这层不单独定义，系统会把“任务走不下去”和“运行时断了”混为一谈。

## 当前问题

### 1. `blocked_*` 容易被误当成一切中断的兜底状态

用户明确指出：

- 业务阻塞：AI 主动判断当前直行不下去，需要先补前置、回 brainstorm、补实现或等待依赖
- 系统崩溃：PID 消失、CLI 断掉、状态来不及写回

前者可以有状态交接，后者通常没有。

所以：

- `blocked_*` 不是“进程没了”
- `blocked_*` 不是“监控发现失败”
- `blocked_*` 必须是 AI 已识别并留痕的业务阻塞

### 2. `in_*` 可能是陈旧执行态

当系统监控发现 PID 消失时，条目往往仍停留在：

```yaml
phase_state: in_dev
```

这只说明“上次进入了 dev”，不说明：

- 当前是否还在跑
- 是否还能 resume
- 是否其实已经崩溃
- 是否只是还没来得及写成 `blocked_*`

因此 `in_*` 需要被视为“待恢复判定的执行态”，而不是天然健康运行态。

### 3. 系统恢复时，必须先定位“哪个 issue / 哪个工具 / 哪个 worktree / 哪个 session”

系统崩溃后，AI 无法先交接状态，所以 monitor 只能靠证据恢复：

- 这次是哪条 issue
- 当前在哪个 `in_*`
- 用的是哪个 AI 工具
- 对应哪个 `session_id`
- `jsonl` 或其他日志在哪里
- 当前 worktree / branch 在哪
- 能不能用该工具的正确命令 resume

如果这些只靠 milestone 名字猜，恢复就不可靠。

## 收敛判断

### 1. 业务阻塞与系统崩溃必须分层

推荐硬定义：

- `blocked_*`：AI 已识别并显式留痕的业务阻塞
- system crash：PID 消失、CLI 崩溃、会话断裂、监控探活失败

二者不是一个层面，不能共用一个状态词。

### 2. 系统崩溃不直接改 `phase_state`

系统崩溃发生时，不能直接把：

```yaml
phase_state: in_dev
```

改成：

```yaml
phase_state: blocked_dev
```

因为这会伪造 AI 交接。

正确做法是：

1. 保留原 `in_*`
2. 进入恢复定位
3. 判断能否 resume
4. 恢复成功则继续原 `in_*`
5. 恢复失败且原因已诊断，才允许转成 `blocked_*`

### 3. 恢复定位顺序必须固定

推荐固定为：

```text
recovery -> progress -> issue -> milestone -> active worktree / uncommitted changes
```

其中：

- `recovery`：第一事实源
- `progress`：dev-loop 第一事实源
- `issue`：阶段与范围锚点
- `milestone`：只用于发现活跃 issue，不是恢复事实源
- `active worktree / uncommitted changes`：最后的降级定位手段

### 4. resume 不应靠猜，必须有最小恢复字段

推荐最小恢复字段：

- `tool`
- `session_id`
- `jsonl_path`
- `role`
- `branch`
- `worktree_path`
- `phase_state`
- `runtime_state`
- `resume_hint`

若做不到完整写回，也必须保留显式降级原因。

## 建议状态图补充理解

对于系统崩溃，不新增新的主状态词，而是补一条解释规则：

```text
in_* + pid_lost
-> recovery inspection
-> resume original in_*
or
-> blocked_* only after diagnosis
```

这意味着：

- 系统事件先进入恢复流程
- `blocked_*` 只在诊断后写入
- `phase_state` 继续只承载正式交接后的工作态

## 建议下一跳

1. 创建一个治理 issue，专门收紧：
   - `blocked_*` 的定义
   - system crash 的恢复定位顺序
   - 最小恢复字段
   - resume/attach/restart 的决策入口
2. 在 `LAWS`、`context-source-skill`、`recovery-subagent-governance` 中统一引用该规则。
3. 若后续补 runtime/monitor 脚本，再以该治理 issue 为依据落实现实检查逻辑。
