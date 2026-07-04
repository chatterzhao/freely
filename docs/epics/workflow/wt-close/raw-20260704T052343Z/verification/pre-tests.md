# Pre-Tests: wt-close --force 警告信息优化

- issue_id: I-20260704T052343Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 3 处 --force 警告信息区分收口与废弃，不再误导为常规清理手段
- acceptance_target: pre-commit.sh、freely:16597、freely:21591 三处信息准确
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep 验证
- evidence_level: integration
- artifact_ref: docs/system/workspace/hooks/pre-commit.sh
- test_command: grep "wt-close.*force" docs/system/workspace/hooks/pre-commit.sh docs/system/workspace/scripts/runtime/freely
- expected_output: 所有 --force 引用都有明确"废弃丢弃"语义，无 "or --force to clean up" 等轻描淡写
- expected_RED_output: "use wt-close or wt-close --force to clean up" 出现在 pre-commit.sh
- actual_RED_output: pre-commit.sh:29 'use wt-close or wt-close --force to clean up' — 错误建议 --force 作为常规清理
- actual_output: GREEN. pre-commit.sh 现在区分收口/废弃。freely:16597 同样区分。freely:21591 建议 stop 失败后才 --force。
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed
- red_how: fix — 搜索现有代码中的 'use wt-close or wt-close --force to clean up'，确认存在

## Unit
- acceptance_target: 文本修改验证
- testing_layer: unit
- target_environment: feature-local
- required_evidence: git diff 确认仅文本修改
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯文本警告信息修改，无函数逻辑变更，grep 静态验证足够
- replacement_evidence: AT-001 grep 验证通过

## Integration
- acceptance_target: N/A
- testing_layer: integration
- target_environment: test-pre-merge-20260704T052343Z-wt-close-force-warning
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 纯文本修改，不影响集成行为
- replacement_evidence: 无集成面

## End-to-End
- acceptance_target: N/A
- testing_layer: end_to_end
- target_environment: develop merge chain
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 纯文本修改
- replacement_evidence: 无 E2E 面

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 纯文本修改，不影响运行时行为
