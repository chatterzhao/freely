# Brainstorms - 20260321-2010--explicit-session-addressed-resume-over-last-and-pty

## Context

在 Freely 自举时，我们重新检查了工具续会话模型，发现一条很具体的风险：

- 多进程并行时，`resume --last` 不可靠
- supervisor 也不应把“向旧终端输入框写内容”当成默认重入模型

这件事不只影响 `codex`，也影响 Freely 如何统一理解：

- process lifecycle
- session continuity
- event-driven re-entry
- 多 worker / 多 worktree 并行下的会话寻址
- 主管在理解 signal 之后，如何把 handoff 精确交给某个 worker

## Current Implementation Findings

### codex

当前 Freely 对 `codex` 的 resume 实现是：

- `codex exec resume --last --skip-git-repo-check ...`

这在单链路下可以工作，但在多进程并行时存在显式风险：

- `--last` 不是稳定的 session addressing
- 新进程可能续到“最近的别的会话”，而不是当前 workcell 的会话

### cc / cc-use-codex-cli

当前 `cc` / `cc-use-codex-cli` 已使用：

- `claude -p --session-id <uuid> ...`

这说明 Freely 已经在另一个工具上采用了更稳的“显式会话寻址”模型。

### iflow / kiro-cli

当前 Freely 对这两个工具的 resume 仍是较弱寻址：

- `iflow -c ...`
- `kiro-cli chat --resume ...`

也就是：

- 有 continuation 概念
- 但没有像 `cc` 那样由 Freely 明确传入每个 workcell 的具体 session id

### opencode

本机已安装 `opencode`，但当前 Freely runtime 还没有接入它。现阶段它只是潜在工具，不是当前 canonical runtime surface。

## Codex Research Findings

本机 `codex-cli 0.116.0` 已确认存在正式的续会话接口：

- `codex resume [SESSION_ID] [PROMPT]`
- `codex exec resume [SESSION_ID] [PROMPT]`

并且：

- `codex exec resume --help` 明确支持 `PROMPT`
- `PROMPT` 可以是 `-`，即从 stdin 读取

这意味着对 Freely 来说，正确的 canonical model 更像：

- `new process + explicit session id + resumed prompt`

而不是：

- `resume --last`
- `write to PTY`

## Why `--last` Is Not Enough

Freely 经常：

- 多 worktree 并行
- 多 worker 并行
- 同一工具开多个会话

在这种场景下：

- `--last` 只表达“最近一个”
- 不表达“当前 workcell 应该接哪一个”

所以 supervisor/runtime 需要的是：

- explicit session addressing

至少要能表达：

- `tool`
- `session_id`
- `rollout_path/jsonl_path`
- `cwd`
- `workcell ownership`

还要能表达：

- 当前 handoff 该交给哪个 worker / workcell
- 这个 worker 下一轮应接哪一个 session

## PTY Injection Interpretation

给活着的 Codex 终端直接写字符，不是不能做，但它不应是 canonical path：

- 它依赖 PTY/terminal 状态
- 它要求那个进程仍然活着且真的在等输入
- 它不天然适合 supervisor 重启和多进程治理

它最多只应保留为 fallback：

- 同一交互终端仍活着
- 且明确需要即时交互

## Forced Termination Risk

如果 runtime 为了让新 signal 生效而强制结束当前 AI 进程，会额外引入一个问题：

- 进程里可能仍有未落盘内容

这意味着 canonical contract 不应只定义“怎么 resume”，还要定义：

- 优先如何做 graceful preemption
- 什么情况下允许 hard kill
- hard kill 后 supervisor 最少要保留哪些 recovery evidence

对 Freely 更合理的顺序应是：

1. 优先 graceful handoff / checkpoint / structured flush
2. 如果工具或当前场景做不到，再退化到 hard kill
3. hard kill 不能丢失 session evidence、current issue ownership 和 delegated handoff

## Candidate Direction

优先候选应是：

1. 把 `explicit session-addressed resume` 定义成 Freely 的 canonical continuity model
2. 先修 `codex` 的 `--last`
3. 再审视 `iflow` / `kiro-cli` 是否也需要显式 session addressing contract
4. 定义 manager -> worker handoff 时的 explicit session target
5. PTY 注入只保留为 fallback，不作为 supervisor 默认路径
6. 把 graceful preemption / hard kill fallback 也收进 continuity contract
