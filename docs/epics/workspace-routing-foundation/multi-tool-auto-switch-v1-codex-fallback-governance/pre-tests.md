# Pre-Tests: multi-tool-availability-manager-governance

## Acceptance Items

### A1. ordered fallback config truth is written and reloaded
- id: `A1`
- requirement: write_config emits ordered fallback fields and ensure-manager reloads project config before each selection cycle.
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/multi-tool-auto-switch-v1-codex-fallback-governance/code-reviews/20260331-multi-tool-auto-switch-v1-codex-fallback-verification.md`

### A2. Codex remains same-tool-first before cross-tool fallback
- id: `A2`
- requirement: When the current tool has canonical same-tool recovery truth, control plane keeps same-tool recovery ahead of cross-tool fallback.
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`

### A3. cross-tool fallback uses ordered list and fresh handoff
- id: `A3`
- requirement: When same-tool recovery is exhausted or a compatible tool-local failure occurs, ensure-manager scans AI_FALLBACK_TOOLS in order and records launch_kind=fresh_with_handoff.
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`

### A4. all-tools-unavailable keeps no-launch waiting truth
- id: `A4`
- requirement: If every configured tool is unavailable, launch stays blocked and waiting truth records earliest-reset rather than blind relaunch.
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`

### A5. auto-switch-off Kiro path still stops and defers
- id: `A5`
- requirement: When auto-switch is disabled, Kiro availability failures keep the local stop-plus-defer contract instead of relaunching locally.
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`

### A6. cleanup-time recheck waits for teardown and live fallback works
- id: `A6`
- requirement: Teardown-aware one-shot recheck waits for exiting supervisor state to clear, then ordered fallback can still select a non-current tool on canonical develop.
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/multi-tool-auto-switch-v1-codex-fallback-governance/code-reviews/20260331-multi-tool-auto-switch-v1-codex-fallback-verification.md`

### A7. Kiro launcher keeps a supported default model
- id: `A7`
- requirement: If project config leaves AI_MODEL empty for Kiro, launcher falls back to a supported model instead of failing before availability classification.
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-tool-launchers-kiro-default-model`

## Focused Tests

1. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-kiro-to-codex-fallback`
   - 锁住兼容性路径：Kiro tool-local failure 仍能在 order 中选到 Codex
2. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
   - 锁住 fallback 会继续扫描配置顺序，而不是把 Codex 硬编码成唯一 target
3. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
   - 锁住 Codex 先 same-tool recovery，穷尽后才 cross-tool
4. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`
   - 锁住 all-tools-unavailable 时 no-launch 与 earliest-reset waiting truth
5. `bash docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
   - 锁住 auto-switch 未开启时，Kiro availability failure 仍只 stop/defer，不在本地 blind relaunch
6. `bash docs/system/workspace/scripts/tests/test-tool-launchers-kiro-default-model`
   - 锁住 Kiro launcher 在 `AI_MODEL=""` 时仍会使用受支持的默认模型，而不是过期的 `claude-opus-4.6`

## Regression Risks

1. `ensure-manager` 如果不 reload config，watchdog 进程会继续持有旧的 `AI_TOOL=kiro-cli`，导致 config 改了也不生效。
2. 如果把 `tools.md` 优先级直接当成 fallback order，routing truth 与 runtime availability truth 会再次混淆。
3. 如果 cross-tool fallback 没有强制 `fresh_with_handoff`，会把不同 continuity class 的工具误当成可 resume 等价物。
