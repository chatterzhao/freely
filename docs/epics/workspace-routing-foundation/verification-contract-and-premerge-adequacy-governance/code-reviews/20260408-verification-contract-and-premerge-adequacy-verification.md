# Verification: verification-contract-and-premerge-adequacy-governance

- issue_id: `I-20260408-1205-A`
- issue_path: `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`
- verification_date: `2026-04-09`
- verifier: `codex`

## Scope Verdict

- `PASS`: worker launch prompts now carry the bounded verification metadata contract instead of pure scheduling truth.
- `PASS`: runtime writes the same verification contract into delegated intake and worker runtime state, so recovery and followthrough can consume one machine-readable projection.
- `PASS`: manager handoff guidance, launcher prompt scaffold, delegated intake, and worker runtime state now share one machine-readable verification contract instead of leaving recovery to prompt prose.
- `PASS`: `pretests-gate` now enforces the four required sections and per-section scalar schema, and rejects `not_applicable` sections that omit concrete `replacement_evidence`.
- `PASS`: guarded `feature/* -> test-pre-merge-* -> develop` promotion proved the verification contract survives both protected merge hops, and the owner now carries an explicit `premerge-integration:develop_merge` adequacy item instead of relying on implicit merge history.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-natural-language-prompt`
3. `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
4. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
5. `./bin/governance-check`

## Implementation Decision Note

- decision: `Bind manager/worker handoff and premerge adequacy review to one shared verification contract rather than leaving test design and merge-time diagnostics as parallel truth.`
- why_this: `The failure mode was not missing tests in the abstract; it was the system being unable to distinguish missing test planning, missing case design, missing execution, and missing completion writeback from the merge path.`
- alternatives_considered: `Keep verification metadata out of worker prompts; rely only on pretests-gate at issue completion; treat premerge integration as a generic pass/fail without actionable adequacy taxonomy.`
- boundary_non_goals: `No claim that premerge replaces post-merge real-environment verification, and no attempt to make merge gate author all test design on behalf of issue owners.`
- residual_risk: `Historical pre-tests files outside this owner still vary in structure, and older dormant research-only trees still need explicit retirement rather than being left ambiguous in fleet inventory.`
