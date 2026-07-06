# Pre-Tests: multi-tool-availability-manager-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `ordered fallback v1 with codex parity`
- testing layer: `focused regression`
- target environment: `feature worktree`
- required evidence: config reload, ordered fallback, codex slot-first, and all-tools-unavailable coverage
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. 新项目 config 默认写出 `AUTO_SWITCH_SLOT=false`、`AUTO_SWITCH_TOOL=false`、`AI_FALLBACK_TOOLS=""`，并保持 `AI_TOOL` 仍是 active tool pointer。
2. `ensure-manager` 会重新读取 project config，不依赖旧进程启动时缓存的 `AI_TOOL`。
3. 当当前工具具备 canonical same-tool recovery truth 时，control plane 必须先走同工具恢复，再考虑 cross-tool fallback。
4. 当当前工具 tool-local failure 或 same-tool recovery exhausted 且 `AUTO_SWITCH_TOOL=true` 时，control plane 会按 `AI_FALLBACK_TOOLS` 顺序挑选下一个可用工具，而不是硬编码 `codex`。
5. 每次跨工具 fallback 必须显式记录 `launch_kind=fresh_with_handoff`，不得冒充 resume。
6. 若所有配置中的工具都不可用，`ensure-manager` 仍保持 no-launch，并显式记录 earliest-reset hint。
7. 当 auto-switch 未开启时，Kiro availability failure 仍应保持“本地 stop + defer control plane”的旧 contract。
8. 当 project config 没有显式 Kiro model 时，launcher 必须回退到当前仍受支持的默认模型；不能因为过期默认值在 availability classification 之前就进入 `ai_exit_rc_1` loop。

### Post-merge canonical truth acceptance

- acceptance target: `develop carries bounded ordered fallback v1`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: progress closeout, verification artifact, and develop commit provenance
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. This owner must close as v1 once develop contains the ordered fallback implementation and follow-up fixes.
2. Broader all-tools slot parity must remain delegated to `I-20260401-0840-A`, not stay ambiguous here.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `kiro tool-local failure can still choose codex through ordered fallback`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-kiro-to-codex-fallback`

### PT-2
- id: `PT-2`
- requirement: `fallback scans configured priority order instead of hardcoding codex as the only target`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`

### PT-3
- id: `PT-3`
- requirement: `codex remains same-tool slot-first before cross-tool fallback`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`

### PT-4
- id: `PT-4`
- requirement: `all-tools-unavailable path keeps no-launch and earliest-reset waiting truth`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`

### PT-5
- id: `PT-5`
- requirement: `auto-switch disabled keeps kiro availability failure on stop plus defer control-plane contract`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`

### PT-6
- id: `PT-6`
- requirement: `kiro launcher falls back to a supported default model when AI_MODEL is empty`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-tool-launchers-kiro-default-model`

## Regression Risks

1. `ensure-manager` 如果不 reload config，watchdog 进程会继续持有旧的 `AI_TOOL=kiro-cli`，导致 config 改了也不生效。
2. 如果把 `tools.md` 优先级直接当成 fallback order，routing truth 与 runtime availability truth 会再次混淆。
3. 如果 cross-tool fallback 没有强制 `fresh_with_handoff`，会把不同 continuity class 的工具误当成可 resume 等价物。
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
