# Progress: all-tools-unified-slot-contract-governance

- issue_id: `I-20260401-0840-A`
- title: All-tools unified slot contract governance
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`

## Current Slice

- close the old ordered-fallback owner as v1 instead of silently widening it
- freeze all-tools slot inventory truth
- add generic current-slot scheduler truth
- preserve Codex watchdog parity while widening the scheduler to every tool family
- current implementation now persists generic per-tool current-slot truth in `.ai-auth/.<tool>-current-slot`
- manager recovery now retries non-Codex same-tool slots before cross-tool fallback and records earliest `tool + slot` waiting truth

## Evidence

- `docs/pre-brainstorms/20260401-0840--all-tools-unified-slot-contract-governance/brainstorms.md`
- `docs/pre-brainstorms/20260401-0840--all-tools-unified-slot-contract-governance/candidates.md`
- `docs/epics/workspace-routing-foundation/all-tools-unified-slot-contract-governance/issues/all-tools-unified-slot-contract-governance.md`
- `docs/system/workspace/scripts/tests/test-ai-cli-generic-tool-login-creates-slot-container`
- `docs/system/workspace/scripts/tests/test-ai-cli-generic-tool-switch-persists-current-slot`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-entry-blocked-cross-tool-fallback`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-non-codex-slot-first-then-cross-tool`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-tool-slot`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-single-slot-failure-falls-through-to-cross-tool`
- `docs/epics/workspace-routing-foundation/all-tools-unified-slot-contract-governance/code-reviews/20260401-all-tools-unified-slot-contract-verification.md`
