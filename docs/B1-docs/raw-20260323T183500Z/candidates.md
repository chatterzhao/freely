# 候选：worker-delegated-continuation-active-stall-recovery

- id: `C-20260323T183500Z-A`
- title: Detect and recover active worker delegated-continuation stalls
- source_brainstorm: `docs/B1-docs/raw-20260323-1835/brainstorms.md`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://worker-delegated-continuation-active-stall-recovery-materialization`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- why_now:
  - 真实 dogfood 已复现 worker prompt 吸收 delegated continuation 后，AI 假活但 cycle log / closeout 不再推进
  - 当前 manager watchdog 只覆盖 worker 掉线恢复，不覆盖 `worker supervisor 仍存活` 的 stall
- expected_outcome:
  - define a runtime-visible stall contract for active workers after delegated continuation prompt absorption
  - allow manager watchdog to trigger worker-side recovery without human stop/start
  - unblock full loop closure from worktree retention/retirement to next patrol
- decision_reason:
  - 这条 gap 属于 runtime orchestration，而不是单个 worker issue 的局部 closeout
  - 但仍需通过 runtime patch + dogfood 验证边界，确认它应 materialize 为独立 issue，还是吸收到既有 worker/runtime recovery issue 族
- retention_audit:
  - `2026-03-25`: the original runtime patch from this tree is already contained by `develop`, but that does not close the owner lifecycle. `C-20260323T183500Z-A` is still a candidate with `promoted_issue_path: pending://...`, no milestone-owned issue owner, and no surviving issue/progress artifact has absorbed the active-worker delegated-continuation stall acceptance boundary.
  - `2026-03-25`: keep this dedicated worktree retained-with-reason until real dogfood either freezes the boundary into a promoted issue or explicitly reroutes the candidate into another runtime recovery owner.
- next_action:
  - 先给 manager watchdog 补 worker active-stall recovery，并继续真实 dogfood 验证 retained worker 是否能自动收口、cleanup、再继续找新任务
- revisit_trigger:
  - 若再次出现 active worker 已收到 delegated continuation 但 cycle log / closeout 长时间不推进
  - 或当前 runtime 补丁稳定后，需要冻结成独立 issue contract
