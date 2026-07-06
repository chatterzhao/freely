# PRD: chat-triggered-worker-runtime-reactivation-governance

## Goal

让 `freely chat` 在 worker 工位上既保持 durable intake，又能在正确条件下重新拉起本工位主循环消费 delegated continuation/verification，不再出现“插话成功但无人推进”。

## Why Now

- 真实狗粮已经出现 stopped worker + delegated continuation 堆积。
- Freely 现在要求默认通过 `chat` 与系统交互，这条路径不能只靠人工重新 `freely start`。
- 这不是新能力域，而是 existing runtime/preflight/reactivation 的缺口。

## Product Surface

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- runtime tests for chat/interruption

## Non-Negotiables

- `freely chat` 仍先 durable 写 intake。
- 只有满足 worker-local delegated handoff gate 时，才自动重激活 worker 主循环。
- 当前已有 active AI 时，不得重复拉起第二个主循环。
- `operator_stop`、`auth_failure`、`runtime crash` 的 reactivation 语义要区分。
- 不把 PTY 注入当作重入方案。

## Decomposition

1. gate 定义
   - 哪些 handoff target 触发 worker reactivation
   - 哪些 runtime state 允许自动重启
2. runtime materialization
   - chat/dispatcher 后的 reactivation preflight
   - start path 选择
3. verification
   - stopped worker + continuation
   - stopped worker + verification
   - active AI present -> no duplicate runtime
