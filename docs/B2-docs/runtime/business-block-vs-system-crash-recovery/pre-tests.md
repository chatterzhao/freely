# Pre-Tests: business-block-vs-system-crash-recovery

1. 业务阻塞会显式落成 `blocked_*`，且带阻塞原因与下一步。
2. PID 消失或 CLI 崩溃不会直接把条目标成 `blocked_*`。
3. 恢复流程优先按 `recovery -> progress -> issue -> milestone -> active worktree` 定位上下文。
4. 若已知 `tool/session_id` 且存在有效 `resume_hint`，恢复流程可推导正确的 resume 或 attach 路径。
5. `milestone` 只能帮助发现活跃 issue，不单独充当恢复事实源。
