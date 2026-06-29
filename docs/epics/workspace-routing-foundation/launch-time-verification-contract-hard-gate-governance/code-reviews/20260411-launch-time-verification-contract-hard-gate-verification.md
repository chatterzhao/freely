# Verification: launch-time-verification-contract-hard-gate-governance

- issue_id: `I-20260411-1414-A`
- issue_path: `docs/epics/workspace-routing-foundation/launch-time-verification-contract-hard-gate-governance/issues/launch-time-verification-contract-hard-gate-governance.md`
- verification_date: `2026-04-12`
- verifier: `codex`

## Scope Verdict

- `PASS`: worker prompt parsing now treats missing verification fields as a real contract failure instead of a truthy partial-metadata success path.
- `PASS`: manager-driven worker launch now blocks branch-only and partially specified prompts, writes blocked contract state, and avoids creating delegated intake artifacts for invalid launches.
- `PASS`: a fully populated manager-to-worker handoff still launches, writes runtime/intake verification contracts, and preserves active-worker reentry behavior.
- `PASS`: manager recovery fails closed when a worker is marked expected-running but its persisted verification contract is missing or malformed.
- `PASS`: unresolved worker targets, missing prompt files, stale discovery caches, and partial metadata against an already active worker now surface bounded blocked diagnostics without clobbering live state.
- `PASS`: a disposable `test-pre-merge-*` replay has now been used to prove the owner carries explicit `premerge-integration:develop_merge` adequacy coverage instead of relying only on feature-local completion evidence.
- `PASS`: canonical owner/progress closeout text now matches reality after develop promotion and retirement, so future continuation routing no longer points operators back at an already-closed premerge replay.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
3. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-branch-only-prompt`
4. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-malformed-verification-contract`
5. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-without-verification-contract`
6. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-partial-verification-metadata`
7. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-unresolved-worktree-blocked`
8. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-projection-without-state`
9. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-worker-partial-metadata-keeps-running-state`
10. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-missing-prompt-blocked`
11. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-refreshes-stale-discovery-cache`
12. `./bin/governance-check`
13. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
14. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-branch-only-prompt`
15. `./bin/test-lane premerge-integration -- ./bin/governance-check`
16. `freely pr-merge-guarded test-pre-merge-20260412-completed-owner-closeout-truth feature/completed-owner-closeout-truth-20260412`

## Implementation Decision Note

- decision: `Move verification contract enforcement to the runtime launch boundary so invalid manager-to-worker handoffs fail closed before any worker supervisor start or delegated intake materialization occurs.`
- why_this: `The prior design only recorded missing verification metadata after launch had already crossed the boundary, which let ambiguous or incomplete prompts consume worker capacity and blur the source of testing truth.`
- alternatives_considered: `Continue allowing launch with best-effort diagnostics; infer missing context from branch-only prompts; recover expected-running workers without a valid persisted contract.`
- boundary_non_goals: `This owner does not harden guarded develop merge adequacy, cleanup retirement enforcement, or broader testing orchestration outside the launch boundary.`
- residual_risk: `The launch boundary is now covered for both feature-local completion and guarded premerge replay, but future changes to the verification contract fields or owner closeout copy still need explicit staged review refreshes so develop-bound adequacy does not silently fall back to stale truth.`
