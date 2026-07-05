# Progress: all-tools-unified-slot-contract-governance

- issue_id: `I-20260401-0840-A`
- title: All-tools unified slot contract governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`

## Current Slice

- close the old ordered-fallback owner as v1 instead of silently widening it
- freeze all-tools slot inventory truth
- add generic current-slot scheduler truth
- preserve Codex watchdog parity while widening the scheduler to every tool family
- current implementation now persists generic per-tool current-slot truth in `.ai-auth/.<tool>-current-slot`
- manager recovery now retries non-Codex same-tool slots before cross-tool fallback and records earliest `tool + slot` waiting truth

## Evidence

- `docs/B1-docs/raw-20260401/brainstorms.md`
- `docs/B1-docs/raw-20260401/candidates.md`
- `docs/epics/workspace-routing-foundation/all-tools-unified-slot-contract-governance/issues/all-tools-unified-slot-contract-governance.md`
- `docs/system/workspace/scripts/tests/test-ai-cli-generic-tool-login-creates-slot-container`
- `docs/system/workspace/scripts/tests/test-ai-cli-generic-tool-switch-persists-current-slot`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-entry-blocked-cross-tool-fallback`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-non-codex-slot-first-then-cross-tool`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-tool-slot`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-single-slot-failure-falls-through-to-cross-tool`
- `docs/epics/workspace-routing-foundation/all-tools-unified-slot-contract-governance/code-reviews/20260401-all-tools-unified-slot-contract-verification.md`

- closure_status: `merged-and-verified`
- closure_evidence:
  - `merge_commit: e8b5e0a`
  - `tests: bash docs/system/workspace/scripts/tests/test-ai-cli-generic-tool-login-creates-slot-container && bash docs/system/workspace/scripts/tests/test-ai-cli-generic-tool-switch-persists-current-slot && bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-non-codex-slot-first-then-cross-tool && bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-tool-slot`
  - `review: docs/epics/workspace-routing-foundation/all-tools-unified-slot-contract-governance/code-reviews/20260401-all-tools-unified-slot-contract-verification.md`
  - `live_validation: canonical develop runtime recovered from kiro-cli monthly limit through a later usable Codex slot`
