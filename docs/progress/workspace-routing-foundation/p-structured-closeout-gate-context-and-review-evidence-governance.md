# Progress: structured-closeout-gate-context-and-review-evidence-governance

- issue_id: `I-20260412-0225-A`
- title: Structured closeout gate context and fresh review evidence governance
- phase_state: `in_dev`
- runtime_state: `unavailable`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/structured-closeout-gate-and-review-evidence-followon-20260412`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260412-feature-structured-closeout-gate-and-review-evidence-followon`
- issue_path: `docs/epics/workspace-routing-foundation/structured-closeout-gate-context-and-review-evidence-governance/issues/structured-closeout-gate-context-and-review-evidence-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "dev-loop-and-guarded-replay"}

## Summary

- Worker launch, delegated intake, and workcell state now persist one structured closeout contract: command, target lane, promotion gate, adequacy requirement, and review-artifact policy all travel as first-class verification metadata.
- Cleanup and retirement replay now consume those structured fields directly and fail closed when retained worker state only carries legacy free-text closeout guidance.
- `pretests-gate` and `governance-merge-gate` now use the same `fresh staged owner review artifact` wording, so develop-bound diagnostics no longer split the contract across different phrases.
- This owner is still in `in_dev` because the disposable `test-pre-merge-* -> develop` replay has not yet completed its final truth loop: the diff now carries structured closeout/runtime hardening, but the guarded replay still needs a same-diff adequacy/progress binding and a deliberate proof that fresh review-artifact enforcement remains the final narrow blocker when adequacy is otherwise satisfied.

## Verification Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-verification-metadata`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-natural-language-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-partial-verification-metadata`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-branch-only-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-projection-without-state`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-refreshes-stale-discovery-cache`
- `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-pretests-retain`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-retained-continuation`
- `bash docs/system/workspace/scripts/tests/test-pretests-gate`
- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `./bin/governance-check`
- `./bin/wt-create test-pre-merge-20260412-structured-closeout-gate-review-evidence --base develop`
- `./bin/merge-guarded test-pre-merge-20260412-structured-closeout-gate-review-evidence feature/structured-closeout-gate-and-review-evidence-followon-20260412`
- `./bin/merge-guarded develop test-pre-merge-20260412-structured-closeout-gate-review-evidence`

## Next Action

- Replay the disposable `test-pre-merge-20260412-structured-closeout-gate-review-evidence -> develop` promote after binding this owner's same-diff progress artifact and develop-bound adequacy item, then verify whether the remaining blocker narrows to the expected fresh staged owner review artifact requirement without any gate relaxation.
