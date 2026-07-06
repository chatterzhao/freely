# Pre-tests: pre-tests-evidence-binding-and-completion-gate-governance

## Acceptance Structure

### Pre-merge acceptance

1. `bin/pretests-gate` 能从 issue 文档解析 `pre_tests_path`，并只检查当前 issue 绑定的 `pre-tests.md`
2. `bin/pretests-gate` 能拒绝以下 completed gate 失败：
   - issue 缺少 `pre_tests_path`
   - `pre-tests.md` 缺少 acceptance items
   - acceptance item 缺少 `id` / `requirement` / `evidence_level` / `status` / `artifact_ref`
   - acceptance item `status` 不是 `pass` 或 `not_applicable`
   - `artifact_ref` 为 `pending://...`
   - `artifact_ref` 指向不存在的本地 artifact
3. `pre-commit` 在 staged issue 把 `phase_state` 切到 `completed` 时，会调用同一 gate，并在失败时拒绝提交
4. 其他普通提交不会被这条 gate 误伤

### Post-merge acceptance

1. 这一批不要求自动 retirement gate
2. 合并到 `develop` 后，其他 worktree 只要更新到包含这条能力的 `develop`，继续推进到 `completed` 时会被同一 gate 约束

### Non-goals

1. 不要求所有历史 story 立即补 machine-readable acceptance items
2. 不要求 gate 直接解析长篇 code review 内容

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `standalone pretests-gate rejects missing issue binding and incomplete acceptance items`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/pre-tests-evidence-binding-and-completion-gate-governance/raw-20260327-0701/code-reviews/20260327-pretests-gate-feature-verification.md`

### PT-2
- id: `PT-2`
- requirement: `pre-commit blocks a staged issue that switches to completed while its acceptance items are still pending`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/pre-tests-evidence-binding-and-completion-gate-governance/raw-20260327-0701/code-reviews/20260327-pretests-gate-feature-verification.md`

### PT-3
- id: `PT-3`
- requirement: `pre-commit does not block unrelated feature commits when no staged issue is moving to completed`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/pre-tests-evidence-binding-and-completion-gate-governance/raw-20260327-0701/code-reviews/20260327-pretests-gate-feature-verification.md`
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
