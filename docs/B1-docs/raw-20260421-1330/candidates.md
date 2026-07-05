# Candidates - 20260421-1330--absorbed-merged-lane-routing-followthrough

## Context
- Source brainstorm: `docs/pre-brainstorms/20260421-1330--absorbed-merged-lane-routing-followthrough/brainstorms.md`
- Status: `promoted`
- Route: `materialize-absorbed-merged-lane-routing-followthrough-owner-and-replay-through-guarded-develop`

## Candidates

### C-20260421-1330-A
- candidate_format_version: `v2`
- title: `Absorbed merged lane routing followthrough governance`
- research_only: `false`
- implementation_ready: `true`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_id: `I-20260421-1330-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/issues/absorbed-merged-lane-routing-followthrough-governance.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- problem: Canonical `develop` dogfooding proved absorbed merged blocker lanes were no longer auto-recovered, but patrol still consumed them as if they were live execution targets because fleet status preserved `role=worker` and task-source-scan preserved `verification` routing for the linked progress owner.
- why_now:
  - this advisory-surface mismatch keeps the manager drifting back toward an already absorbed lane instead of choosing fresh launchable work
  - the narrow fix is already implemented and focused regressions are green in the feature worktree
  - the next truthful acceptance surface is guarded replay into `develop` followed by canonical self-host daemon continuation
- acceptance_criteria:
  - absorbed merged lanes no longer render as `role=worker` in fleet status
  - progress items bound to absorbed merged lanes route to `cleanup` instead of `verification`
  - focused regressions and nearby scan/fleet regressions stay green
  - guarded `feature/* -> test-pre-merge-* -> develop` replay succeeds with concrete owner evidence
  - on canonical `develop`, `freely daemon start` selects a real launchable task, completes it to the current-project success standard, closes the temporary worktree, and continues
- promotion_gate:
  - keep scope on absorbed merged lane routing downgrade only
  - do not widen into scan or live-status redesign
  - keep final canonical self-host acceptance as a required post-merge completion duty
- next_action: Candidate mirror only. `I-20260421-1330-A` is now the canonical owner for absorbed merged lane routing downgrade in fleet status and task-source-scan, plus canonical develop self-host replay.
- revisit_trigger: Re-open only if canonical develop still routes absorbed merged lanes back into edit execution after this bounded downgrade, or if another dogfooding run proves cleanup visibility and execution visibility still cannot stay separated without a larger owner.
- decision_reason: `This is a narrow patrol-surface followthrough. Downgrading absorbed merged lanes in fleet status and task-source-scan closes the drift without reducing Freely autonomy or reopening the broader daemon owner.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
