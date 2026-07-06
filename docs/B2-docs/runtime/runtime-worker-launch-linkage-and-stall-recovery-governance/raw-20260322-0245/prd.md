# PRD - runtime-worker-launch-linkage-and-stall-recovery-governance

## Product outcome

让 Freely 在真实自治开发里具备两项 runtime 能力：

1. manager 已产出的 stable worker handoff 能真正触发 worker execution
2. 当前 AI 轮次 stall 时，runtime 能恢复并让新的 delegated continuation 进入下一轮

## User-visible behavior

- 用户通过 `freely chat` 提出项目级治理任务后，manager patrol / continuity 若已给出具体 worker handoff，后续无需人工再复制 prompt；Freely 会自行把 handoff 转成 worker worktree 的执行。
- 若当前 AI 长时间无推进且有新的待处理 signal，Freely 会自动恢复，不需要人工先 `stop/start`。

## Constraints

- 继续使用现有 headless CLI adapter，不改为操纵外部 TUI。
- `develop` 上 manager 仍不直接施工。
- worker execution 仍在各自 feature worktree 中进行。
