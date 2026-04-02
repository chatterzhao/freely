# Pre-Tests: frontend-runtime-baseline-for-probe

## Acceptance Structure

### Post-merge absorption closeout acceptance

- acceptance target: `frontend runtime baseline is absorbed by downstream probe and bridge implementation`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: story-local absorption verification and downstream develop truth proving the baseline is no longer hypothetical
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. 文档必须明确宿主入口与 React renderer 挂载路径。
2. 文档必须明确 Tauri runtime 注入的最小要求。
3. 文档必须明确最小 build/test baseline，而不是只说“后面再补”。
4. 文档必须明确该 baseline 是 `Frontend Probe v0` 的依赖，而不是其内部细节。
5. 文档完成后，应能直接把后续 dev-loop 拉回 `I-20260317-1002`，而不是继续停留在 baseline 边界争论。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `frontend runtime baseline issue explicitly records host entry, renderer mount, tauri injection, and minimal build/test baseline as a separate boundary`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/issues/frontend-runtime-baseline-for-probe.md`

### PT-2
- id: `PT-2`
- requirement: `canonical develop contains the frontend host/build/runtime surfaces that this owner was created to freeze`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/code-reviews/20260402-frontend-runtime-baseline-for-probe-absorption-verification.md`

### PT-3
- id: `PT-3`
- requirement: `downstream probe and rust/tauri bridge owners have consumed this baseline so it no longer needs a parked committed lifecycle`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/frontend-probe-dogfooding-loop/frontend-runtime-baseline-for-probe/code-reviews/20260402-frontend-runtime-baseline-for-probe-absorption-verification.md`
