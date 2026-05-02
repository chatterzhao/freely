# Pre-Tests: cli-first-entrypoint-and-observability-surface-unification

1. `freely tui` 提交消息后，与 `freely chat` 一样能够触发 dispatcher ensure。
2. `freely tui` 在 worker continuation 场景下，也能触发允许的 runtime reactivation。
3. 真源明确 CLI-first backend contract，未来 TUI/GUI 只复用，不另造语义。

## Acceptance Items

### shared-submit-chain
- id: `shared-submit-chain`
- requirement: freely tui must enter the same high-level submit helper and dispatcher ensure path that freely chat uses.
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/code-reviews/20260322-cli-first-entrypoint-and-observability-surface-unification-verification.md`

### tui-worker-reactivation-gate
- id: `tui-worker-reactivation-gate`
- requirement: freely tui must trigger the same allowed worker runtime reactivation gate as freely chat during continuation flows.
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/code-reviews/20260322-cli-first-entrypoint-and-observability-surface-unification-verification.md`

### cli-first-contract-preserved
- id: `cli-first-contract-preserved`
- requirement: canonical truth must continue to state that freely is the only front-door command and that TUI/GUI are render layers over the same backend contract.
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/code-reviews/20260322-cli-first-entrypoint-and-observability-surface-unification-verification.md`
