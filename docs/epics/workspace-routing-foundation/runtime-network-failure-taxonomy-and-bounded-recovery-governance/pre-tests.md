# Pre-Tests: runtime-network-failure-taxonomy-and-bounded-recovery-governance

## Acceptance Contract

1. Runtime distinguishes `oauth_unreachable` from execution-time network failures.
2. Execution-time network failures are classified as `execution_network_transient`, `execution_network_persistent`, or `proxy_config_invalid`.
3. Network-local execution failures do not trigger slot rotation or cross-tool fallback by default.
4. During an active retry/cooldown window, manager recovery stays blocked on the current `tool + slot`.
5. After the retry window expires, manager recovery relaunches the same current `tool + slot`.
6. Existing slot-first and cross-tool fallback regressions remain green, proving this slice does not regress slot/tool availability behavior.

## Focused Tests

1. `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
2. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-network-failure-blocks-fallback`
3. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-network-failure-relaunches-current-slot`
4. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
5. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
6. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`
