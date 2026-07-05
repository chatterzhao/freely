# Pre-Tests — raw key 格式统一

## Unit

- acceptance target: `regex pattern matching — all grep/sed/regex patterns in 18 files accept both old and new raw key formats`
- testing layer: `unit`
- target environment: `feature worktree (local)`
- required evidence: `grep -qoE verification of all 4 format combinations (raw old/new, I old/new)`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `本次为 regex 模式匹配层重构，不涉及可执行的单元测试边界。所有验证通过 grep/sed/scan 命令行手工执行完成。`
- replacement_evidence: `docs/B2-docs/ibm/raw-key-format-unify/code-reviews/closeout-review.md`

## Integration

- acceptance target: `scan chain trace 和 pre-push hook 对新旧两种格式的行为不变性`
- testing layer: `integration`
- target environment: `feature worktree with develop baseline`
- required evidence: `task-lifecycle-scan.py output comparison, pre-push regex acceptance test`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `集成测试的验证面是 scan chain trace 和 pre-push hook 的行为不变性。已通过手工运行 scan 和 grep 测试确认旧格式无回归、新格式被识别。`
- replacement_evidence: `docs/B2-docs/ibm/raw-key-format-unify/code-reviews/closeout-review.md`

## End-to-End

- acceptance target: `完整 Freely 流程中 scan → wt-create → pre-push → merge-gate 对新旧格式的支持`
- testing layer: `end_to_end`
- target environment: `test-pre-merge worktree`
- required evidence: `governance-merge-gate passed, wt-create with new format branch succeeded, pre-push hook accepts both formats`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `端到端验证面是完整 Freely 流程，行为完全由 regex 模式匹配决定。手工测试已覆盖所有新旧格式组合。`
- replacement_evidence: `docs/B2-docs/ibm/raw-key-format-unify/code-reviews/closeout-review.md`

## Real-Environment

- real_environment_status: `pass`
- real_environment_reason: `本次为 regex 重构，不涉及运行时行为变更。所有更改仅在模式匹配层，不需要真实环境测试。`

## Acceptance Items

### A1 - All regex patterns dual-compatible

- id: `A1`
- requirement: `All regex/glob patterns in pre-push.sh, wt-create, task-lifecycle-scan.py, governance-merge-gate, freely accept both old and new raw key formats`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/raw-key-format-unify/code-reviews/closeout-review.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`

### A2 - Scan output no regression

- id: `A2`
- requirement: `task-lifecycle-scan.py produces identical output for all old-format items; new format items correctly detected`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/raw-key-format-unify/code-reviews/closeout-review.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
