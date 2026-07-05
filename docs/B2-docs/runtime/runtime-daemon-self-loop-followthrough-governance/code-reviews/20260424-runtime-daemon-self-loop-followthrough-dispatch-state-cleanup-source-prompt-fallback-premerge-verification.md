# Verification: runtime-daemon-self-loop-followthrough-governance dispatch-state cleanup source-prompt fallback premerge replay

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-24`
- verifier: `codex`
- source_branch: `feature/cleanup-prompt-materializer-fallback-20260424`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-cleanup-prompt-materializer-fallback`
- premerge_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-test-pre-merge-cleanup-prompt-materializer-fallback`

## Scope Verdict

- `PASS`: close the narrower cleanup-governance seam where fresh replay continuity exposed retained-lane prompt truth only through `## Dispatch State` `worker_prompt_paths:` and no longer carried legacy `issue_truth`.
- `PASS`: keep the launchability gate strict. The merged-lane `edit` prompt remains nonlaunchable on its own once the branch is already merged into `develop`; runtime may only reuse it as metadata source for a fresh cleanup prompt.
- `PENDING`: canonical `develop` replay still must prove the retained receipt-closeout lane launches as cleanup followthrough, closes or reclassifies lawfully, and Freely advances to the next task.

## Current-Window Evidence

1. Fresh replay at `2026-04-24 17:52:10 PDT` wrote `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260424-175210.md` with `route_kind=cleanup_governance`, `## Dispatch State`, and `worker_prompt_paths:` pointing at `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260424-175210-worker-runtime-lifecycle-receipt-closeout-reconcile-codex.txt`.
2. That prompt still carried the authoritative owner/pre-tests/verification metadata for the retained worktree `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-runtime-lifecycle-receipt-closeout-reconcile`, but its `intent_kind=edit` made it correctly nonlaunchable after the branch was already merged into `develop`.
3. Runtime therefore needed two repairs at once: parse `## Dispatch State` `worker_prompt_paths:` as continuity prompt truth, and treat the continuity-carried merged-lane prompt as metadata source only while rematerializing a fresh `cleanup` prompt for the same retained worktree.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-autofills-cleanup-prompt-from-continuity-source-prompt`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-delegate-workers-requires-launchable-prompt`

## Implementation Decision Note

- decision: `Allow cleanup-governance autofill to recover verification metadata from the latest continuity-carried prompt for the same retained worktree, and rewrite dispatch-state prompt refs to the fresh cleanup prompt once rematerialized.`
- why_this: `The retained lane had already lost worker-local authoritative prompt truth, and continuity no longer carried legacy issue fields, but the manager-authored continuity still held enough owner metadata in the stale merged-lane prompt to lawfully mint a new cleanup prompt.`
- alternatives_considered: `Relax the merged-lane edit-prompt launch gate; require continuity to keep legacy issue fields forever; silently reuse the merged-lane edit prompt as if it were still launchable ownership.`
- boundary_non_goals: `No scan-source redesign, no relaxation of delegate-workers validation, and no claim that canonical end-to-end daemon looping is already complete.`
- residual_risk: `Canonical replay may still expose a later cleanup execution or retirement seam after this launchability repair, but fresh cleanup continuity should no longer stall simply because only dispatch-state prompt refs and source-prompt metadata remain.`

## Implementation

- Added `## Dispatch State` `worker_prompt_paths:` parsing to the continuity prompt discovery path used by cleanup-governance rematerialization.
- Added `manager_cleanup_source_prompt_file_from_continuity()` so cleanup autofill can recover verification metadata from the continuity-carried prompt targeting the same retained worktree when no local authoritative worker prompt or legacy `issue_truth` remains.
- Rebases owner/pre-tests/verification paths from that source prompt into the retained worker worktree before writing the fresh cleanup prompt.
- Rewrites `## Dispatch State` `worker_prompt_paths:` to the fresh cleanup prompt and prevents merged cleanup-governance lanes from treating their old merged-lane `edit` / `promotion` prompt as pending active ownership once the branch is merged into `develop`.
- Added focused regression `test-freely-manager-exit-contract-autofills-cleanup-prompt-from-continuity-source-prompt`.

## Verification

### Feature lane

- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-autofills-cleanup-prompt-from-continuity-source-prompt`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-delegate-workers-requires-launchable-prompt`

### Protected replay

- `PASS`: merged `feature/cleanup-prompt-materializer-fallback-20260424` into `test-pre-merge-cleanup-prompt-materializer-fallback-20260424`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-autofills-cleanup-prompt-from-continuity-source-prompt`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-delegate-workers-requires-launchable-prompt`

## Adjacent Risk

- `KNOWN ADJACENT`: canonical `develop` replay has not yet been rerun after this narrower dispatch-state/source-prompt fallback repair, so a later cleanup execution or retirement seam may still surface after the launchability repair lands.
