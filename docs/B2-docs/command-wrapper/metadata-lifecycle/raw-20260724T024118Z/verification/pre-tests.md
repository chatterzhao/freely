# Pre-Tests: command-wrapper 元数据生命周期契约
- issue_id: I-20260724T024118Z-A

## Acceptance Items

### AT-001
- id: AT-001
- requirement: 契约文档位于能力目录且五要素章节齐全
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 文档存在 + owner/phase/freshness/rejection/evidence 五章
- evidence_level: integration
- artifact_ref: docs/B2-docs/command-wrapper/metadata-lifecycle/raw-20260724T024118Z/verification/test-evidence/contract.log
- test_command: python3 docs/system/workspace/scripts/tests/test-command-wrapper-metadata-contract.py
- expected_output: OK (5 sections)
- expected_RED_output: 文档缺失或章节不全（断言失败）
- actual_RED_output: "FAIL: contract doc missing"
- actual_output: "OK (5 sections; fields referenced)"
- evidence_file: docs/B2-docs/command-wrapper/metadata-lifecycle/raw-20260724T024118Z/verification/test-evidence/contract.log
- red-green-status: green
- status: pending
- blocker: execution_pending_or_failed
- red_how: "单元测试 test-command-wrapper-metadata-contract.py，契约文档未物化时失败"

### AT-002
- id: AT-002
- requirement: 契约引用 wrapper 元数据字段且不修改 runtime wrapper 行为
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: 文档引用字段一致 + runtime/freely 无 wrapper 行为改动
- evidence_level: integration
- artifact_ref: docs/B2-docs/command-wrapper/metadata-lifecycle/raw-20260724T024118Z/verification/test-evidence/contract.log
- test_command: python3 docs/system/workspace/scripts/tests/test-command-wrapper-metadata-contract.py
- expected_output: OK (fields referenced; runtime untouched)
- expected_RED_output: 文档缺字段引用（断言失败）
- actual_RED_output: "FAIL: contract doc missing (字段引用无对象)"
- actual_output: "OK (5 sections; fields referenced)"
- evidence_file: docs/B2-docs/command-wrapper/metadata-lifecycle/raw-20260724T024118Z/verification/test-evidence/contract.log
- red-green-status: green
- status: pending
- blocker: execution_pending_or_failed
- red_how: "集成测试 test-command-wrapper-metadata-contract.py，字段引用缺失时失败"

## Unit
- acceptance_target: 契约文档五要素
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 测试断言通过
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: 字段引用与 runtime 零改动
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: 测试断言通过
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: 契约文档可被后续 B1/B2/skill 引用
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260724T024118Z-command-wrapper-metadata-lifecycle
- required_evidence: 文档在能力目录（docs/system/workspace/）且可引用
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 契约文档位于能力目录 docs/system/workspace/，可被后续流程引用
