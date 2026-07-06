# Verification: runtime-daemon-self-loop-followthrough-governance daemon recovery preservation

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-22`
- verifier: `codex`
- source_branch: `feature/daemon-runtime-failure-recovery-preserves-daemon-20260422`
- protected_test_branch: `test-pre-merge-20260422-daemon-runtime-failure-recovery-preserves-daemon`

## Scope Verdict

- `PASS`: canonical `develop` replay exposed a bounded daemon-control-plane seam, not a broader patrol or task-selection failure: after `tool_runtime_failure`, recovery could relaunch manager supervision through foreground `start --project` instead of preserving daemon ownership.
- `PASS`: runtime now persists `LAST_ENTRYPOINT_MODE` in `workcell-state.env`, so control-plane recovery still knows whether the authoritative runtime was daemon-owned after the original supervisor exits.
- `PASS`: manager recovery now relaunches daemon-owned control planes through `daemon-run --project` while preserving existing foreground `start --project` behavior for non-daemon lanes.
- `PASS`: the new regression proves both halves of the contract: daemon entrypoint truth survives follow-up state writes, and `launch_manager_supervisor()` chooses `daemon-run` rather than `start` when the stored control-plane mode is daemon.
- `PASS`: adjacent daemon lifecycle regressions and premerge governance replay still pass on the protected test lane, so this bounded repair does not regress daemon detach, unexpected TERM handling, live-supervisor reuse, or teardown-race recovery.
- `PENDING`: canonical `develop` still needs post-merge daemon replay to prove Freely completes one task, merges upward, retires the temporary lane, and continues to another task without further runtime repair.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-failure-recovery-preserves-daemon`
2. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
3. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
5. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-waits-for-supervisor-teardown-before-fallback`
6. `./bin/governance-check`
7. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-failure-recovery-preserves-daemon`
8. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
9. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
10. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
11. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-waits-for-supervisor-teardown-before-fallback`
12. `./bin/governance-check`

## Implementation Decision Note

- decision: `Persist daemon versus foreground control-plane ownership in workcell state and consume that truth when manager recovery relaunches supervision.`
- why_this: `The failing replay already narrowed the bug to recovery semantics after supervisor exit. Rewriting broader watchdog or daemon architecture would widen the owner unnecessarily; preserving one machine-readable entrypoint fact is enough to stop recovery from silently degrading a daemon-started runtime into a foreground one.`
- alternatives_considered: `Teach ensure-manager to infer daemon ownership from transient process argv after cleanup; bypass ensure-manager and hardwire daemon-specific cleanup relaunches; widen the repair into slot/tool recovery policy even though the observed failure happened after the control plane had already decided to keep desired state running.`
- boundary_non_goals: `No new task-selection logic, no tool/slot policy expansion, no change to protected-branch merge policy, and no attempt to claim final canonical self-host acceptance before develop-side replay.`
- residual_risk: `Post-merge canonical daemon replay may expose another bounded runtime seam after control-plane ownership is preserved; that remains the true completion gate for this owner.`
