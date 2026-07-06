# Verification: active-milestone-placement-and-consumption-gate-governance

- issue_id: `I-20260331-2012-A`
- reviewer: `codex`
- verdict: `pass_for_verification`

## Commands

- `bash docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`
- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `./bin/governance-check`

## Results

1. `governance-check` now rejects active candidates that remain `unassigned` / `pending://...`, validates that unresolved candidates are carried by an active milestone `candidate_issues` queue, and confirms candidate-declared `milestone:` matches the actual `M-*` carrier.
2. `governance-merge-gate` now rejects wrong active milestone placement, completed milestone placement for unresolved candidates, and promoted candidates that never materialized into formal issue sequencing.
3. `docs/LAWS.md`, `doc-pre-brainstorm-execution`, milestone-planning, and manager patrol truth now all describe the same keep / cautious rehome / dropped contract for `needs_research`.
4. Current backlog drift was normalized: active candidates that were still `unassigned` or `pending://milestone-binding` are now bound back into the active milestone queue, so the new gate closes a real gap instead of only asserting a hypothetical one.
5. `./bin/governance-check` passes in this worktree; the only residual output is the pre-existing legacy naming warnings, not placement or traceability failures.
6. Post-merge replay exposed one narrow develop-merge follow-up: unresolved candidate placement repairs still hit the per-candidate owner requirement. The follow-up keeps `promoted` / `absorbed` strict, but allows unresolved `proposed|needs_research|blocked` candidate metadata repairs to travel inside the current governance owner while the same merge carries issue/progress/review evidence.

## Implementation Decision Note

- decision: legacy: completed verification artifact
- why_this: legacy: no detailed record
- alternatives_considered: legacy: no detailed record
- boundary_non_goals: legacy: no detailed record
- residual_risk: legacy: no detailed record
