# Brainstorm: business-block-vs-system-crash-recovery

## Focus

把“业务阻塞”和“系统崩溃恢复”分层为正式治理规则，并绑定到 auto-loop 的恢复定位流程。

## Key Decisions

1. `blocked_*` 只用于业务阻塞，不用于 PID/CLI 崩溃。
2. 系统崩溃后优先保留原 `in_*`，先做恢复定位，而不是伪造 `blocked_*`。
3. `milestone` 只是发现入口，不是恢复事实源。
4. 选择正确 resume 命令依赖 `tool/session_id/jsonl_path/resume_hint`，不应靠猜。

## Open Checks

1. `resume_hint` 是直接写命令模板，还是只写模式和值域。
2. 当前是否需要把 `branch/worktree_path` 正式纳入 `session_refs`，还是仅要求 recovery/progress 必须带上。
3. 当前研究阶段缺失 `docs/progress/**` / `docs/recovery/**` 时，如何定义等价留痕的最小要求。
