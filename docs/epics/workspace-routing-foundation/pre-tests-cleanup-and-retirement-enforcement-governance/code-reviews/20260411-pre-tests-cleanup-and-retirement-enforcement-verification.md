# Verification: pre-tests-cleanup-and-retirement-enforcement-governance

- issue_id: `I-20260411-1416-A`
- issue_path: `docs/epics/workspace-routing-foundation/pre-tests-cleanup-and-retirement-enforcement-governance/issues/pre-tests-cleanup-and-retirement-enforcement-governance.md`
- verification_date: `2026-04-12`
- verifier: `codex`

## Scope Verdict

- `PASS`: retirement now reads recorded owner issue metadata and bound `pre_tests_path` before deciding whether a worktree may retire.
- `PASS`: pending acceptance items, missing cleanup state, missing owner bindings, ambiguous issue resolution, and unsupported adequacy requirements all fail closed with machine-readable retirement blocker output.
- `PASS`: cleanup followthrough retains merged worktrees when owner pre-tests still block retirement or when the retirement gate itself is unavailable.
- `PASS`: retained merged worktrees are escalated into manager continuation instead of being silently dropped, while clean merged worktrees can still retire.
- `PASS`: this owner adds cleanup/retirement closure without widening into launch-time gating or changing the existing completion/develop-merge gate contract.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
2. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-pretests-retain`
3. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-retained-continuation`
4. `./bin/governance-check`

## Implementation Decision Note

- decision: `Bind cleanup retirement to the same issue-owned pre-tests truth already used by completion and guarded promote, instead of inventing a separate retirement-only test ledger.`
- why_this: `The gap was lifecycle closure, not missing test concepts. Retirement previously had no bounded way to prove owner evidence was closed, so merged worktrees could disappear while required acceptance items were still pending.`
- alternatives_considered: `Treat cleanup as heuristics-only; introduce a parallel retirement test document; force cleanup to understand adequacy-v2 before it can protect baseline completion truth.`
- boundary_non_goals: `This owner does not harden launch-time verification contracts, change guarded develop merge adequacy semantics, or require cleanup to consume every future adequacy-v2 field.`
- residual_risk: `Develop-bound promotion still needs a separate premerge replay and owner-level promote evidence before canonical merge, because this verification only closes the feature-lane cleanup/retirement surface.`
