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

## System crash rule

- 系统监控发现 PID 消失或 CLI 崩溃时，不得直接写 `blocked_*`
- 固定按 `recovery -> progress -> issue -> milestone -> active worktree` 定位上下文
- 根据 `tool/session_id/jsonl_path/resume_hint` 选择 resume 或 restart
