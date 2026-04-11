# Implementation Decision: runtime-concurrent-start-stop-followthrough-governance

- issue_id: `I-20260411-0517-A`
- date: `2026-04-11`
- decision: `Materialize a narrow followthrough owner instead of leaving the remaining runtime diff as candidate-only closeout notes.`

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
