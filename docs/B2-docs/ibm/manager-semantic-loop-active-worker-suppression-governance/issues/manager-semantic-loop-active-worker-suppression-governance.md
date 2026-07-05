# Issue: manager-semantic-loop-active-worker-suppression-governance

- issue_id: `I-20260405-1505-A`
- title: Manager semantic-loop active-worker suppression governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-semantic-loop-active-worker-suppression-governance`
- issue-name: `manager-semantic-loop-active-worker-suppression-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260405/candidates.md#c-20260405-1505-a`
- source_brainstorm: `docs/B1-docs/raw-20260405/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/manager-semantic-loop-active-worker-suppression-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-manager-semantic-loop-active-worker-suppression-governance.md`
- verification_artifact_dir: `docs/B2-docs/ibm/manager-semantic-loop-active-worker-suppression-governance/code-reviews`
- depends_on: `docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/issues/latest-manager-continuity-worker-consumption-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

The read-only semantic-loop signal introduced under `I-20260322-0445` is supposed to stay conservative: it should surface only when the manager keeps rewriting equivalent continuity while no worker is actually running and capacity is still available. Current canonical `develop` still fails that contract. The same regression test proves the signal can remain active even after a worker supervisor and AI process are already present, which turns a monitoring hint into a false positive during normal execution.

`I-20260322-0445` stays completed. Its latest continuity / prompt generated-consumed truth remains valid, and its own progress explicitly routes later queue or active-worker evolution into a new owner rather than reopening the completed issue family. This follow-on owner only freezes how semantic-loop suppression should consume active-worker truth.

## Scope

1. Reproduce and freeze the active-worker false-positive semantic-loop path on canonical `develop`.
2. Keep the signal conservative: active worker execution must suppress semantic-loop suspicion.
3. Allow launch-state `ACTIVE_RUNNING_WORKER_COUNT` to act as a bounded semantic-loop suppression fallback when status-time process discovery is temporarily behind the last runtime write.
4. Preserve the existing missing-run-dir quieting and zero-worker semantic-loop detection path.

## Acceptance

- `bash docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface` passes on the repaired branch.
- When a worker is actively running, `live-status` reports `semantic_loop_signal_reason: unavailable`.
- The suppression fallback does not remove the original zero-active-worker semantic-loop signal.
- The lane remains focused on semantic-loop suppression truth, not broader stall recovery or blocked-intake supervision redesign.

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-fleet-status`
- `./bin/governance-check`

## Next

- Keep this owner closed once the active-worker suppression contract is on `develop`.
- Any future semantic-loop auto-recovery, delegated-continuation stall repair, or broader active-worker stall orchestration must materialize as separate follow-on owners.
