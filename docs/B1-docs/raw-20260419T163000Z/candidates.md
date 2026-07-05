# Candidates - 20260419-1630--runtime-startup-self-healing-boundary

- Source brainstorm: `docs/B1-docs/raw-20260419-1630/brainstorms.md`

### C-20260419T163000Z-A: legacy issue

- title: `Runtime startup self-healing boundary`
- source_class: `discovery`
- route_kind: `pre_brainstorm`
- phase_state: `in_dev`
- candidate_status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- problem: `Protected-root startup can leave machine-owned runtime truth in a self-contradictory state before manager AI launch: status says running/up while the supervisor and dispatcher PIDs are dead, lifecycle logs stop before a lawful AI handoff, and active prompt/continuity artifacts still reference a missing dedicated worktree.`
- why_now:
  - `2026-04-19` protected-root replay again stalls at `activity_state: stalled_without_runtime` after `daemon start`
  - stale pid files and missing-worktree references show the startup surface can already be non-canonical before AI recovery begins
  - current prompts still instruct continuation into a deleted worktree, so manager routing cannot be trusted until startup truth is repaired or explicitly degraded
- proposed_scope:
  - define exactly what startup scripts may auto-heal before launching manager AI
  - require startup to downgrade unrecoverable stale machine state into machine-readable blocked truth instead of publishing a fake healthy runtime
  - keep semantic continuation / lifecycle decisions on the manager side after startup canonicalization
- non_goals:
  - reopening the closed status-truth owner wholesale
  - widening the in-flight after-failure recovery handoff fix into a mixed startup-governance owner
  - generic fleet supervision redesign
- acceptance_criteria:
  - startup self-heal scope is frozen for stale pid, stale process ownership, missing continuity/prompt artifacts, and missing worktree anchors
  - manager-owned scope is frozen for continuation, issue routing, worktree strategy, and governance judgment after startup
  - the new owner explains how machine-owned blocked truth should look when startup cannot safely repair a stale reference
  - the owner remains narrow enough to drive focused pre-tests rather than a broad runtime rewrite
- depends_on:
  - `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
  - `docs/B2-docs/ibm/freely-start-auto-recovery-rootcause-governance/issues/freely-start-auto-recovery-rootcause-governance.md`
- promoted_issue_path: `docs/B2-docs/runtime/runtime-startup-self-healing-governance/issues/runtime-startup-self-healing-governance.md`
- next_action: `Finish focused regressions, replay the protected root, and then promote this bounded owner into canonical develop without widening it into manager recovery semantics.`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}
