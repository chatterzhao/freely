# Implementation Decision: runtime-concurrent-start-stop-followthrough-governance

- issue_id: `I-20260408-0231-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-concurrent-start-stop-followthrough-governance/issues/runtime-concurrent-start-stop-followthrough-governance.md`
- branch: `feature/runtime-concurrent-start-stop-followthrough-20260411`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260411-feature-runtime-concurrent-start-stop-followthrough`
- decision_date: `2026-04-11`
- author: `codex`

## Implementation Decision Note

- decision: `Materialize the remaining runtime half of C-20260408-0231-A as the bounded execution owner instead of leaving the develop-bound runtime diff in candidate-only closeout notes.`
- why_this: `Canonical develop already absorbed the generated-truth status half, but the same candidate still owns unresolved runtime behavior around same-project bootstrap attach, project stop breadth, and stop-marker preservation. Keeping the same lifecycle key preserves candidate -> issue traceability while narrowing scope to the unmerged execution slice.`
- alternatives_considered: `Leave the runtime diff as candidate-only closeout notes; open a brand-new unrelated issue id; reopen the already-absorbed status-surface half together with the runtime followthrough.`
- boundary_non_goals: `Do not reopen generated-truth status alignment, broader watchdog/runtime recovery redesign, or the separate checkpoint-risk preflight capability discussion.`
- residual_risk: `Canonical closeout still depends on guarded merge and tracked-root replay; if that replay regresses adjacent status surfaces or merge gates require additional lifecycle normalization, this owner may need one more bounded followthrough update.`

## Why

- `C-20260408-0231-A` mixed two defects.
- The generated-truth status half is already absorbed on canonical `develop`.
- The remaining diff is still real runtime behavior and therefore needs a lawful develop-bound owner chain.

## Scope decision

- Keep only:
  - degraded bootstrap attach reuse under same-project supervisor hints
  - project-scoped stop across all discovered same-project supervisors
  - stop-marker preservation until the last same-project supervisor exits
- Exclude:
  - new status-surface design
  - generic runtime recovery redesign
  - checkpoint-risk preflight capability work
