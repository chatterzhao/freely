# Pre-Tests: frontend-probe-v0

## Acceptance Structure

### Post-merge canonical closeout acceptance

- acceptance target: `frontend probe v0 canonical closeout`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: real tauri validation artifact, downstream bridge completion, and a story-local closeout verification
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. 文档必须明确 Probe v0 不是完整工作台，而是最薄产品面。
2. 文档必须覆盖 project switch、session create/resume、message input、stream output、status、stop/retry/resume。
3. 文档必须明确 `control bar`、`chat intervention panel`、`agent roster`、`embedded terminal` 的最小职责。
4. Probe 必须只通过 boundary contract 访问 backend，不直接侵入 runtime/workspace。
5. day-1 主入口必须明确为应用内终端 / 控制台。
6. project switch、session create/resume、message input、stream output、stop/retry/resume 必须都有最小交互流定义。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `frontend probe v0 retains the documented minimal day-1 product surface instead of expanding into a broader workbench`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`

### PT-2
- id: `PT-2`
- requirement: `real tauri validation covers start, session create-resume, terminal attach, and chat intervention for the probe surface`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/code-reviews/20260401-frontend-probe-v0-terminal-attach-validation.md`

### PT-3
- id: `PT-3`
- requirement: `frontend probe closeout remains downstream of completed rust/tauri bridge evidence rather than claiming a mock-only finish`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/code-reviews/20260401-rust-tauri-probe-bridge-real-interaction-verification.md`

### PT-4
- id: `PT-4`
- requirement: `story-local closeout verification records that canonical develop already absorbed the probe v0 implementation and evidence`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/code-reviews/20260402-frontend-probe-v0-closeout-verification.md`
