# Pre-Tests: scan parse_frontmatter 嵌套解析修复
- issue_id: I-20260807T071225Z-A

## Acceptance Items

### AT-001
- id: AT-001
- requirement: strict raw 的 platform_ids 解析为 dict 且 validate 通过
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 测试 OK
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/scan-frontmatter/raw-20260807T071225Z/verification/test-evidence/scan-frontmatter.log
- test_command: python3 docs/system/workspace/scripts/tests/test-scan-frontmatter-nested.py
- expected_output: OK
- expected_RED_output: FAIL: platform_ids parsed as str
- actual_RED_output: "FAIL: platform_ids parsed as str"
- actual_output: "OK: nested platform_ids parsed; strict raw validates"
- evidence_file: docs/B2-docs/ibm/scan-frontmatter/raw-20260807T071225Z/verification/test-evidence/scan-frontmatter.log
- red-green-status: green
- status: passed
- blocker: ""
- red_how: "单元测试 test-scan-frontmatter-nested.py，修复前 platform_ids 解析为 str"

### AT-002
- id: AT-002
- requirement: bullet/混合格式 I-* 解析不回归（fallback 保留）
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: 扫描 7 个 strict raw 全部 validate 通过
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/scan-frontmatter/raw-20260807T071225Z/verification/test-evidence/scan-frontmatter.log
- test_command: python3 docs/system/workspace/scripts/tests/test-scan-frontmatter-nested.py
- expected_output: OK
- expected_RED_output: 解析失败或顺序错
- actual_RED_output: "平台_ids 解析为 str（既有缺陷）"
- actual_output: "OK"
- evidence_file: docs/B2-docs/ibm/scan-frontmatter/raw-20260807T071225Z/verification/test-evidence/scan-frontmatter.log
- red-green-status: green
- status: passed
- blocker: ""
- red_how: "集成测试：strict raw 全量 validate"

## Unit
- acceptance_target: platform_ids 解析为 dict
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 测试 OK
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: 全量 strict raw validate 通过
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: scan 无新增误报
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 修复后 scan 对 strict raw 的校验恢复真实（不再误报字段顺序）
