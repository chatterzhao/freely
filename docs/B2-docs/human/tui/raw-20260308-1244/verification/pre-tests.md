# Pre-Tests: rust-tauri-probe-bridge-v1

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `real tauri probe bridge interaction validation`
- testing layer: `focused regression plus live smoke`
- target environment: `feature worktree`
- required evidence: frontend tauri seam fixes, rust validation reporting, and a passed real-host tauri interaction report
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. Frontend default bridge names remain aligned with the issue contract: `probe_request_snapshot`, `probe_send_command`, `probe_server_event`.
2. Frontend `freely.probe.v1` manifest remains compatible with the day-1 Rust/Tauri bridge contract.
3. Real `probe_request_snapshot` succeeds through Tauri invoke and returns a minimal single-project snapshot.
4. Real `probe_send_command` covers `ControlRun`, `CreateOrResumeSession`, and `SendChatIntervention`.
5. Real `probe_server_event` yields the frontend-consumed minimal event subset.
6. Under real `Transport=tauri`, `Frontend Probe v0` completes one start, one session create/resume, and one chat intervention interaction loop.

### Post-merge canonical truth acceptance

- acceptance target: `develop carries canonical real tauri interaction evidence for probe bridge v1`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: progress closeout, verification artifact, and develop commit provenance
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. This owner closes only after real `Transport=tauri` interaction evidence is written back, not merely host startup evidence.
2. Canonical truth must continue to distinguish this bridge owner from downstream frontend product-surface closeout.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `frontend tauri adapter invokes snapshot requests with the Rust payload shape expected by real tauri commands`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `src/frontend_probe_v0/tauriAdapter.test.ts`

### PT-2
- id: `PT-2`
- requirement: `frontend validation mode can drive real tauri bridge state changes and observe them via snapshot writeback`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/human/tui/raw-20260308-1244/code-reviews/20260401-rust-tauri-probe-bridge-real-interaction-verification.md`

### PT-3
- id: `PT-3`
- requirement: `rust bridge and frontend app continue to compile after validation instrumentation is added`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/human/tui/raw-20260308-1244/code-reviews/20260401-rust-tauri-probe-bridge-real-interaction-verification.md`

### PT-4
- id: `PT-4`
- requirement: `real tauri host startup remains green while interaction validation is added`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/human/tui/raw-20260308-1244/code-reviews/20260401-rust-tauri-probe-bridge-host-validation-verification.md`
## Unit
- acceptance_target: 历史 issue，已完成验证
- testing_layer: unit
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成，当时不要求这些 section。原始测试证据在 issue 开发过程中已验证。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Integration
- acceptance_target: 历史 issue，已完成验证
- testing_layer: integration
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## End-to-End
- acceptance_target: 历史 issue，已完成验证
- testing_layer: end-to-end
- target_environment: develop merge chain (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 此 issue 在 pre-tests v2 标准引入前完成并已合并，原始实现已通过真实环境验证。
