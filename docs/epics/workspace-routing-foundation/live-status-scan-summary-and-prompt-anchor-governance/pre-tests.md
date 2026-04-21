# Pre-Tests: live-status-scan-summary-and-prompt-anchor-governance

- owner: `I-20260421-1530-A`
- target environment: `test-pre-merge-20260421-live-status-scan-summary`

## Cases

1. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-includes-scan-summary`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-prefers-session-state-prompt-anchor`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`.
5. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-includes-milestone-patrol-seed`.
6. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`.
7. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-suppresses-broad-patrol-while-worker-active`.
8. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`.
9. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`.
10. Run `bash docs/system/workspace/scripts/tests/test-start-lead-agent-verification-metadata-contract`.
11. Run `bash -n docs/system/workspace/scripts/runtime/freely`.
12. Run `./bin/governance-check`.

## Acceptance Target

Prove that this owner keeps prompt-anchor current-state truth authoritative while adding advisory scan-summary observation, without regressing daemon, patrol, worker-launch, or verification-contract behavior.
