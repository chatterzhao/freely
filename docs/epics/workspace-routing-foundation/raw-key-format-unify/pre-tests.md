# Pre-Tests — raw key 格式统一

## Unit

- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `本次为 regex 模式匹配层重构，18 个文件的变更均为正则表达式和 glob 模式更新，不涉及可执行的单元测试边界。所有验证通过 grep/sed/scan 命令行手工执行完成。`
- replacement_evidence: `docs/epics/workspace-routing-foundation/raw-key-format-unify/code-reviews/review.md`

## Integration

- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `集成测试的验证面是 scan chain trace 和 pre-push hook 的行为不变性。已通过手工运行 task-lifecycle-scan.py 和 grep 测试确认旧格式无回归、新格式被识别。`
- replacement_evidence: `docs/epics/workspace-routing-foundation/raw-key-format-unify/code-reviews/review.md`

## End-to-End

- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `端到端验证面是整个 Freely 流程（scan → wt-create → pre-push → merge-gate），这些行为完全由 regex 模式匹配决定。手工测试已覆盖所有新旧格式组合。`
- replacement_evidence: `docs/epics/workspace-routing-foundation/raw-key-format-unify/code-reviews/review.md`

## Real-Environment

- real_environment_status: `pass`
- real_environment_reason: `本次为 regex 重构，不涉及运行时行为变更。所有更改仅在模式匹配层，不需要真实环境测试。`

## Acceptance Items

### A1 - All regex patterns dual-compatible

- id: `A1`
- requirement: `All regex/glob patterns in pre-push.sh, wt-create, task-lifecycle-scan.py, governance-merge-gate, freely accept both old (YYYYMMDD-HHMM) and new (YYYYMMDDTHHMMZ) raw key formats`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/raw-key-format-unify/code-reviews/review.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`

### A2 - Scan output no regression

- id: `A2`
- requirement: `task-lifecycle-scan.py produces identical output for all old-format items; new format items correctly detected`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/raw-key-format-unify/code-reviews/review.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`

### A3 - Governance merge gate passes

- id: `A3`
- requirement: `governance-merge-gate --range "develop..HEAD" passes with complete C/M/I chain`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/raw-key-format-unify/code-reviews/review.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
