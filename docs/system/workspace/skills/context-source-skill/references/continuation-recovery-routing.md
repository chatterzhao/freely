# Continuation And Recovery Routing

## Progress

- `progress` 只跟踪 dev-loop 执行态
- 默认下一跳是 `dev-loop-execution`

## Issue

- docs 不足：`doc-ibm-execution`
- docs 足够：`dev-loop-execution`

## Recovery

- 先恢复到中断前目标环
- 不直接把恢复条目当成新发现问题

## Stale `in_*` rule

若条目停在 `in_*`：

1. 检查会话是否仍可 attach / resume
2. 检查最近 `progress` / `recovery` 是否证明执行连续
3. 若证据中断或会话不可续接，进入 `recovery-subagent-governance`
4. 只有恢复判定通过，才继续原 `in_*`
5. 若会话技术上仍可续接，但已出现 `context compacted`、缺少最小 resume evidence 或连续 resume 退化，不要把它当成健康执行中；进入恢复判定并允许 `fresh_with_handoff`

## System crash rule

- 系统监控发现 PID 消失或 CLI 崩溃时，不得直接写 `blocked_*`
- 固定按 `recovery -> progress -> issue -> milestone -> active worktree` 定位上下文
- 根据 `tool/session_id/jsonl_path/resume_hint`、最近 cycle 质量与 handoff 证据选择 `resume`、`fresh_with_handoff` 或 restart
