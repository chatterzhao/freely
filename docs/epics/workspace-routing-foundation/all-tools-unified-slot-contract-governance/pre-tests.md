# Pre-Tests: all-tools-unified-slot-contract-governance

## Acceptance Contract

1. `I-20260331-1840-A` is explicitly narrowed to ordered fallback v1, and this owner is the canonical follow-on for all-tools slot parity.
2. `~/.ai-auth/<tool>-<slot>/` is the canonical inventory contract for every tool family.
3. `current tool/current slot` scheduler truth is distinct from `last_*` observability truth, with `current_slot` mirrored to `LAST_ACTIVE_SLOT` only for compatibility.
4. Same-tool recovery is slot-first for every tool that has slot inventory when `AUTO_SWITCH_SLOT=true`.
5. Cross-tool fallback still restarts from the leftmost `AI_FALLBACK_TOOLS` entry.
6. all-tools-unavailable waiting truth preserves earliest recovery as `tool + slot`.
7. Real live repro proves `kiro-cli` tool failure + dead current Codex slot still converge to a later usable Codex slot before launch.

## Focused Tests

1. `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool`
2. `bash docs/system/workspace/scripts/tests/test-ai-cli-login-creates-incremented-slot`
3. `bash docs/system/workspace/scripts/tests/test-ai-cli-generic-tool-login-creates-slot-container`
4. `bash docs/system/workspace/scripts/tests/test-ai-cli-generic-tool-switch-persists-current-slot`
5. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-entry-blocked-cross-tool-fallback`
6. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
7. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
8. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`
9. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-cross-tool-restarts-from-leftmost-priority`
10. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-non-codex-slot-first-then-cross-tool`
11. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-tool-slot`
12. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-single-slot-failure-falls-through-to-cross-tool`
