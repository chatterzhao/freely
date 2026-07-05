# Pre-tests: active-milestone-placement-and-consumption-gate-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `candidate placement correctness enforcement`
- testing layer: `focused regression + governance check`
- target environment: `feature worktree`
- required evidence: updated governance gates plus closeout verification artifact
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. active candidate with `milestone: unassigned` or `pending://...` must be rejected.
2. unresolved `needs_research | proposed | blocked` candidate must be rejected if it is not carried by an active milestone `candidate_issues` queue.
3. candidate-declared `milestone:` must match the actual `M-*` section that carries the candidate.
4. completed milestones must not accept new unresolved candidates by default.
5. `promoted` candidate must materialize into a formal `I-*` milestone issue instead of remaining only a candidate placeholder.

### Post-merge canonical truth acceptance

- acceptance target: `placement correctness truth-source alignment`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: laws, milestone queues, skills/agent guidance, and quality gates use the same placement contract
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. `docs/LAWS.md`, `docs/milestones.md`, skills, and quality gates must agree that unresolved active candidates belong to active milestone `candidate_issues`.
2. `needs_research` guidance must explicitly cover keep / cautious rehome / dropped instead of indefinite parking.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `governance-check rejects invalid active candidate placement and accepts valid active milestone placement`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`

### PT-2
- id: `PT-2`
- requirement: `governance-merge-gate rejects unassigned, wrong-milestone, completed-milestone, and non-materialized promoted placement`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-merge-gate`

### PT-3
- id: `PT-3`
- requirement: `truth sources and backlog normalization reflect the same placement contract`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/active-milestone-placement-and-consumption-gate-governance/code-reviews/20260331-active-milestone-placement-gate-verification.md`
