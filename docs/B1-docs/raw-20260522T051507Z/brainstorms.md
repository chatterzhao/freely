# Brainstorm — slot full name compat

## Discovery

Raw issue `raw-20260522T051507Z07Z` (GitHub #2112) titled "slot 全名统一". The Freely codebase had multiple slot naming conventions (short forms like `account-*`, `apikey-*` vs full names like `codex-apikey-xxx`). This caused mismatches in:

1. `codex_infer_slot_kind_from_slot` — used prefix match on `account-*/apikey-*`, fails with full names
2. `cmd_switch` generic path — constructed `alias_name="${tool}-${slot}"`, double-prefixing with full names
3. Slot name parsing/serialization across ACP adapter, watchdog, and probe commands

## Research

- Dependencies: slot naming is consumed by ACP session IDs, watchdog control plane, probe commands, tool switch events
- Existing coverage: multiple pre-brainstorms around same timeframe:
  - `20260522T030835Z--ai-cli-apikey-alias-switch`
  - `20260522T035043Z--ai-cli-codex-apikey`
  - `20260522T042725Z--apikey-full-slot-name-fixes`
  - `20260522T044515Z--slot-probe-generic-hi`
  - `20260522T045227Z--probe-say-hi`
  - `20260522T053702Z--cmd-login-apikey-unified-top`
  - `20260522T071901Z--slot-full-name-final-fixes` (successor fix batch)
- The `071901Z` follow-up brainstorm documents two residual issues after initial refactoring

## Decision

Raw issue was absorbed into candidate `C-20260522T051507Z-A`, promoted to `I-20260522T051507Z-A`, and completed. The issue content has been materialized across multiple fix worktrees. The follow-up `slot-full-name-final-fixes` batch handles remaining edges. No further standalone B1/B2 work needed for this raw issue. Mark as absorbed via existing chain.
