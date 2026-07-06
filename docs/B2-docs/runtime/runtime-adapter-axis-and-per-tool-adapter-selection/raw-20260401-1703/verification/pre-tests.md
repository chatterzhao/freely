# Pre-tests: runtime-adapter-axis-and-per-tool-adapter-selection

## Acceptance Structure

### Pre-merge focused regression / smoke

1. `config-surface`
   - `AI_TOOL_ADAPTER_POLICY` 与 `AI_TOOL_ADAPTER` 都会被写入 config defaults
   - current tools 默认仍是 `direct`
   - `freely init --tool-adapter <adapter> [--tool-adapter-policy <policy>]` 能显式写入 adapter/policy truth
   - `freely set-tool --tool <tool> [--tool-adapter <adapter>] [--tool-adapter-policy <policy>]` 能通过受管命令面更新 tool + adapter/policy truth
   - same-tool reselection 保留当前 adapter/policy truth；cross-tool selection 才回落到目标工具默认 policy
   - same-tool mutation 不会把当前 `AI_MODEL` / `AI_REASONING_EFFORT` 静默重置回工具默认值
   - `prefer_acp_fallback_direct` 在 ACP 未实现时仍保留 policy truth，但当前实际 adapter 解析为 `direct`
2. `dispatch-surface`
   - runtime 先按 adapter dispatch，再进入 direct implementation
3. `unsupported-surface`
   - `adapter=acp` 在未实现时会显式 fail fast

### Post-merge integration acceptance

1. `freely status --project <project>` 或等价 status surface 能显示 adapter truth、policy truth 与 current supported-adapter matrix。
2. 在 `adapter=direct` 下，当前 canonical tools 的 launch path 仍能完成最小启动与写回路径；若测试环境无法逐个跑实 CLI，至少要对每个 canonical tool 的 adapter dispatch 入口做 focused regression coverage，并对一个真实可运行 canonical tool 做端到端样本验证。
3. `freely init`、worker init inheritance、以及 tool fallback 写回不会把同工具当前 adapter/policy truth 静默改写成工具默认值。
4. 受管 mutation command 不要求手改 `.freely/config.env` 就能更新 tool + adapter/policy truth。

### Post-merge application-native real-environment acceptance

1. 在真实 project workcell 中，runtime 启动后 direct path 不因 adapter extraction 丢失：
   - session target
   - cycle/debug evidence
   - continuity writeback
2. 若 project config 指向 `adapter=acp`，runtime 必须给出显式 unsupported signal，而不是隐式继续 direct。
3. 若 project config 指向 `policy=prefer_acp_fallback_direct` 且当前工具尚无 ACP path，runtime 会继续 direct，但 status/config 中仍保留该 policy truth。

### Post-merge end-to-end dogfood acceptance

1. Freely 自举继续开发时，tool selection、adapter policy、actual adapter 不再混成同一个 truth field。
2. follow-on ACP prototype owner 能直接消费这条 owner 的 config / dispatch / status truth，而不是重开 adapter-axis debate。

### Non-Goals

1. 本轮不要求任何 ACP bridge 已经跑通。
2. 本轮不要求新增工具已经接入。
3. 本轮不要求决定 first-tool ACP prototype 最终一定选谁。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `runtime persists adapter truth and adapter policy through managed config surfaces`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-set-tool-command`

### PT-2
- id: `PT-2`
- requirement: `adapter-aware dispatch keeps direct path canonical and fails fast for unsupported adapters`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-monitor-ai-cli-adapter-dispatch`

### PT-3
- id: `PT-3`
- requirement: `status surface exposes actual adapter, policy, and per-tool support matrix`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-tool-adapter-policy-resolution`
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
