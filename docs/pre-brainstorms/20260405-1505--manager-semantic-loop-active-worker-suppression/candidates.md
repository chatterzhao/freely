# Candidates - 20260405-1505--manager-semantic-loop-active-worker-suppression

## C-20260405-1505-A

- candidate_format_version: `v2`
- title: Manager semantic-loop active-worker suppression governance
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/manager-semantic-loop-active-worker-suppression-governance/issues/manager-semantic-loop-active-worker-suppression-governance.md`
- promoted_issue_id: `I-20260405-1505-A`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: Canonical `develop` still surfaces `manager_continuity_rewrite_without_state_advance` even after a worker lane is already running, so semantic-loop monitoring is no longer conservative.
- why_now:
  - the failure is reproducible on current canonical `develop`
  - `I-20260322-0445` is already completed and explicitly should not be reopened for later queue / active-worker evolution
  - leaving the gap unresolved makes `live-status` and `fleet-status` misclassify normal worker execution as manager loop suspicion
- acceptance_criteria:
  - reproduce and freeze the active-worker false-positive semantic-loop path on canonical `develop`
  - suppress semantic-loop suspicion whenever runtime can authoritatively see active worker execution
  - keep a conservative fallback when launch-state still records active workers even if process discovery is briefly stale
  - preserve the existing missing-run-dir quieting and zero-worker semantic-loop detection behavior
- promotion_gate:
  - do not reopen `I-20260322-0445` unless its completed latest generated/consumed contract is proven false
  - do not widen this lane into delegated-continuation stall recovery or blocked-intake/websocket supervision
  - keep the repair focused on semantic-loop suppression truth for active worker execution
- open_questions:
  - should launch-state active-worker count act only as a semantic-loop suppression fallback, or as broader status truth
  - is the real detection miss in PID ownership validation, worktree enumeration, or simply status-time fallback policy
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports`
    note: The failure is bounded, reproducible, and no unresolved active owner absorbs it lawfully.
- next_action: Materialize the owner, add the minimal runtime suppression fallback, and replay semantic-loop plus adjacent status regressions before merge.
- revisit_trigger: Reopen only if canonical `develop` again reports a semantic loop while active worker execution is already present after this owner completes.
