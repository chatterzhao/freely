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
- artifact_ref: `docs/B2-docs/ibm/pre-tests-evidence-binding-and-completion-gate-governance/code-reviews/20260327-pretests-gate-feature-verification.md`

### PT-2
- id: `PT-2`
- requirement: `pre-commit blocks a staged issue that switches to completed while its acceptance items are still pending`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/pre-tests-evidence-binding-and-completion-gate-governance/code-reviews/20260327-pretests-gate-feature-verification.md`

### PT-3
- id: `PT-3`
- requirement: `pre-commit does not block unrelated feature commits when no staged issue is moving to completed`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/pre-tests-evidence-binding-and-completion-gate-governance/code-reviews/20260327-pretests-gate-feature-verification.md`
