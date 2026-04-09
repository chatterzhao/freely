# Verification: verification-contract-and-premerge-adequacy-governance

- issue_id: `I-20260408-1205-A`
- issue_path: `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`
- verification_date: `2026-04-08`
- verifier: `codex`

## Scope Verdict

- `PASS`: worker launch prompts now carry the bounded verification metadata contract instead of pure scheduling truth.
- `PASS`: premerge adequacy diagnostics now surface the missing verification layer explicitly enough for guarded promotion review.
- `PASS`: guarded premerge integration proves the feature survives the protected merge path instead of only passing in a feature lane.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-natural-language-prompt`
3. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
4. `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
5. `./bin/governance-check`

## Implementation Decision Note

- decision: `Bind manager/worker handoff and premerge adequacy review to one shared verification contract rather than leaving test design and merge-time diagnostics as parallel truth.`
- why_this: `The failure mode was not missing tests in the abstract; it was the system being unable to distinguish missing test planning, missing case design, missing execution, and missing completion writeback from the merge path.`
- alternatives_considered: `Keep verification metadata out of worker prompts; rely only on pretests-gate at issue completion; treat premerge integration as a generic pass/fail without actionable adequacy taxonomy.`
- boundary_non_goals: `No claim that premerge replaces post-merge real-environment verification, and no attempt to make merge gate author all test design on behalf of issue owners.`
- residual_risk: `The repo still needs stronger hard gating for four required pre-tests sections and task-to-test consistency if status-only diagnostics prove insufficient.`
