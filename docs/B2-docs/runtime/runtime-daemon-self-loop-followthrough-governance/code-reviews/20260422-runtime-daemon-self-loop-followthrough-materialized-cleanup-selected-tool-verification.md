# Verification: runtime-daemon-self-loop-followthrough-governance materialized cleanup worker selected tool

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-22`
- verifier: `codex`
- source_branch: `feature/cleanup-worker-prompt-selected-tool-20260422`
- protected_test_branch: `test-pre-merge-20260422-cleanup-worker-prompt-selected-tool`

## Scope Verdict

- `PASS`: canonical `develop` replay disproved the assumption that the earlier worker restart `selected_tool` fix was sufficient; manager-selected cleanup followthrough could still materialize a brand new worker prompt without `selected_tool`, leaving retained cleanup worktrees stuck on stale local tool config.
- `PASS`: `docs/system/workspace/scripts/runtime/freely` now writes `selected_tool` into materialized cleanup worker prompts, taking continuity-selected truth first and falling back to current project tool truth only when continuity omits it.
- `PASS`: `docs/system/workspace/scripts/tests/test-freely-manager-materialized-cleanup-worker-applies-selected-tool` reproduces the real retained-cleanup shape and proves launch rewrites stale `AI_TOOL=\"cc-use-codex-cli\"` to `codex` before supervisor startup.
- `PASS`: adjacent selected-tool paths remain green via `test-freely-manager-launches-materialized-cleanup-worker-without-continuity-prompt`, `test-freely-manager-worker-launch-applies-selected-tool`, and `test-freely-worker-restart-reapplies-selected-tool-from-verification-contract`.
- `PASS`: this remains a same-owner followthrough inside `I-20260421-1200-A`; no wider tool-switching, slot policy, or cleanup-governance redesign is introduced.
- `PENDING`: canonical `develop` still needs protected absorption plus daemon replay proving the retained cleanup lane launches as `codex`, retires, and allows manager patrol to continue to another task.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-manager-materialized-cleanup-worker-applies-selected-tool`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-materialized-cleanup-worker-without-continuity-prompt`
3. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-applies-selected-tool`
4. `bash docs/system/workspace/scripts/tests/test-freely-worker-restart-reapplies-selected-tool-from-verification-contract`
5. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260422-feature-cleanup-worker-prompt-selected-tool --issue docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
6. `./bin/governance-check`
7. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-manager-materialized-cleanup-worker-applies-selected-tool`
8. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-manager-launches-materialized-cleanup-worker-without-continuity-prompt`
9. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-applies-selected-tool`
10. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-worker-restart-reapplies-selected-tool-from-verification-contract`
11. `./bin/test-lane premerge-integration -- ./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260422-test-pre-merge-cleanup-worker-prompt-selected-tool --issue docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
12. `./bin/test-lane premerge-integration -- ./bin/governance-check`

## Implementation Decision Note

- decision: `Make materialized cleanup worker prompts carry selected_tool so retained cleanup worktrees are corrected from prompt truth before launch.`
- why_this: `The failing canonical replay did not come from worker restart recovery anymore; it came one step earlier when manager generated a new cleanup prompt without the tool field that existing launch/recovery logic already relies on. Adding the missing field fixes the real seam with the smallest possible change.`
- alternatives_considered: `Keep relying on stale worktree-local config; infer the tool from branch naming or cleanup role; widen the repair into broader tool auto-switch or slot policy changes.`
- boundary_non_goals: `No auto tool switching, no slot switching, no broader cleanup-governance rewrite, and no claim that daemon success standard is met before protected develop replay proves task completion, upward merge, retirement, and next-task continuation.`
- residual_risk: `If future cleanup prompt materialization paths bypass the same helper or omit continuity-selected truth in a new format, a similar stale-tool replay could recur and would need another bounded same-owner followthrough.`
