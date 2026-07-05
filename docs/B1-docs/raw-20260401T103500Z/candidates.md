# 候选：develop-push-pending-guard-governance

- id: `C-20260401T103500Z-A`
- candidate_format_version: `v2`
- title: Materialize develop push-pending governance after protected-branch merge
- source_brainstorm: `docs/B1-docs/raw-20260401T103500Z/brainstorms.md`
- problem: Freely currently enforces branch protection and develop-bound merge governance, but it still lacks a canonical state for “merge already happened on local develop, remote push has not happened yet”. Without that state, post-merge acceptance, push debt, cleanup, and next-lane sequencing can blur together, which allows false completion or long-lived local-only truth.
- why_now:
  - protected-branch merge governance is already strict, but post-merge push sequencing is still mostly implicit
  - current hooks can block illegal push, yet they cannot actively surface “develop is ahead and unresolved”
  - if this gap remains implicit, Freely can still lose real work by treating local merge as final completion before remote canonical truth is updated
- acceptance_criteria:
  - define a canonical state model for `develop` when local HEAD is ahead of its remote after merge
  - distinguish at minimum `push_pending` and `push_deferred`, while keeping unresolved push debt visible as patrol truth rather than a new phase gate
  - define the minimum structured defer reasons that may justify a temporary local-only develop state
  - define where the truth should surface first: status-family output, manager patrol, or hook messaging
  - explicitly freeze that hooks must not auto-push on behalf of the operator/runtime
- promotion_gate:
  - do not turn this into “git hook auto-push”
  - first materialize status/patrol truth and defer-reason detection, then decide later whether any narrow blocker belongs in `governance-merge-gate`
  - keep `post-merge acceptance` as a valid reason to delay push, but require explicit reason capture
  - prefer machine-readable patrol/check truth over agent-only reminders
- open_questions:
  - should the first owner land only in `freely status/fleet-status` plus manager patrol, or also mirror into `wt-fleet-status`
  - where should deferred-reason truth live so that protected branch worktrees and runtime can both see it
  - which canonical defer reasons are enough for the first slice without inventing a generic pending-state workflow
  - how should temporary remote/network failure be distinguished from an operator-intentional post-merge acceptance window
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The right first slice is not auto-push. The missing capability is explicit push-pending governance that status, patrol, and merge sequencing can all consume.`
    verdict: `promote`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/ibm/develop-push-pending-guard-governance/issues/develop-push-pending-guard-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- expected_outcome:
  - freeze a canonical governance state for local protected-branch merges that are not yet pushed
  - make “merge happened but push is still pending” visible to status and patrol layers
  - define the first enforcement surface that prevents silent drift without forcing auto-push
- decision_reason:
  - existing laws and hooks already define legal push behavior, so the missing piece is not permissioning but lifecycle state
  - auto-push would erase the intentional gap needed for post-merge acceptance and would hide network/remote side effects inside hook execution
  - agent/skill reminders alone are too weak because they cannot detect long-lived local-only develop truth
  - the first bounded owner can now be frozen: `develop` ahead detection, explicit defer reason, status/fleet/patrol visibility, and manager-owned standing-source followthrough
- next_action:
  - keep the promoted owner in dev-loop until status surfaces, defer-reason truth, and patrol visibility are all implemented together
- revisit_trigger:
  - revisit candidate-level research only if `develop`-scoped push debt proves insufficient and the state model must widen to other protected branch families
