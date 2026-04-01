# Pre-Tests: develop-push-pending-guard-governance

## Acceptance Contract

1. Protected-branch push debt is modeled explicitly; it is not hidden behind “merge already happened locally”.
2. `develop` ahead of remote without a valid defer reason is surfaced as `push_pending`.
3. A valid defer reason downgrades the state to `push_deferred`, not silent success.
4. `live-status`, `fleet-status`, and `wt-fleet-status` all expose the new push state.
5. Manager patrol can consume the signal as standing-source followthrough drift without misclassifying explicit post-merge acceptance windows.
6. Existing push hooks still block illegal push patterns and do not auto-push.

## Focused Tests

1. `bash docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`
2. `bash docs/system/workspace/scripts/tests/test-freely-fleet-status-develop-push-pending`
3. `bash docs/system/workspace/scripts/tests/test-wt-fleet-status-develop-push-pending`
4. `bash docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`
5. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
