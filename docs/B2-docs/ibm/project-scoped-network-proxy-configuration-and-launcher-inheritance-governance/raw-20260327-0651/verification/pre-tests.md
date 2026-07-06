# Pre-tests: project-scoped-network-proxy-configuration-and-launcher-inheritance-governance

## Acceptance Structure

### Pre-merge acceptance

1. `freely init` 会把 project-scoped proxy defaults 写进 `.freely/config.env`，不再依赖 runtime shell 里的 hardcoded localhost fallback。
2. resolver 必须稳定支持：
   - `inherit`
   - `explicit`
   - `disabled`
3. codex launcher 与 watchdog 的 OAuth/curl path 必须继承同一份 project-scoped proxy env。
4. 无参 `freely ai switch codex` 必须先刷新保存的 auth inventory，再根据最新结果决定是否切换到 `usable` slot。
5. runtime 真源中不再保留 `127.0.0.1:7890` 这类代理硬编码 fallback。

### Post-merge acceptance

1. 合入 `develop` 后，后续 worktree 只要从新 `develop` 继续推进，就会默认继承同一套 project-scoped proxy contract。
2. 这一批不要求同时完成前端配置入口；前端后续只需改 `.freely/config.env` 即可驱动同一能力。

### Non-goals

1. 不要求在这个 lane 里完成前端 UI。
2. 不要求迁移用户级全局代理配置。
3. 不要求在这个 lane 里重写 watchdog 的完整 limit recovery 状态机。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `freely init writes project-scoped proxy defaults into .freely/config.env`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/raw-20260327-0651/code-reviews/20260327-project-scoped-network-proxy-verification.md`

### PT-2
- id: `PT-2`
- requirement: `network proxy resolver preserves inherit mode and exports explicit and disabled modes consistently`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/raw-20260327-0651/code-reviews/20260327-project-scoped-network-proxy-verification.md`

### PT-3
- id: `PT-3`
- requirement: `codex launcher and OAuth sweep inherit the same project-scoped proxy env and never fall back to hardcoded localhost defaults`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/raw-20260327-0651/code-reviews/20260327-project-scoped-network-proxy-verification.md`

### PT-4
- id: `PT-4`
- requirement: `no-arg freely ai switch codex refreshes saved auth inventory before selecting a usable slot`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/raw-20260327-0651/code-reviews/20260327-project-scoped-network-proxy-verification.md`

### PT-5
- id: `PT-5`
- requirement: `governance-check stays clean aside from the repository's existing legacy naming warnings`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/raw-20260327-0651/code-reviews/20260327-project-scoped-network-proxy-verification.md`
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
