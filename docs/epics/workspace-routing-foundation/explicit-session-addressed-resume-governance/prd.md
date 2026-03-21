# PRD: explicit-session-addressed-resume-governance

## Goal

让 Freely 的多进程 continuity 以显式会话寻址为基础，而不是依赖 `--last` 或旧终端输入框。

## Product Surface

- `docs/system/workspace/tools.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`

## User Value

- 多 worktree / 多 worker 并行时不易串会话
- supervisor/runtime 更容易判断该 resume 谁
- 工具进程可以结束，但会话 continuity 仍可被稳定恢复
