# Pre-Tests: B2_IBM skill 反糊弄铁律
- issue_id: I-20260625T084506Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: B2_IBM SKILL.md 包含反糊弄铁律警告
- testing_layer: unit
- target_environment: test-pre-merge-20260625T084506Z-b2-ibm-anti-cheating
- required_evidence: grep 确认反糊弄铁律文本存在于 SKILL.md
- test_command: grep -q "反糊弄铁律" docs/system/workspace/skills/freely-doc-B2_IBM-execution/SKILL.md && grep -q "严重失职行为" docs/system/workspace/skills/freely-doc-B2_IBM-execution/SKILL.md && grep -q "端到端测试和集成测试是 AI 编程中防止项目失败的最重要保证" docs/system/workspace/skills/freely-doc-B2_IBM-execution/SKILL.md && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker: (失败时填写)
^- status: passed

### acceptance-2
- acceptance_target: pretests-retirement-gate 包含 E2E/集成测试层级检查
- testing_layer: unit
- target_environment: test-pre-merge-20260625T084506Z-b2-ibm-anti-cheating
- required_evidence: grep 确认层级检查逻辑存在于 gate 脚本
- test_command: grep -q "E2E and Integration test adequacy" docs/system/workspace/scripts/quality/pretests-retirement-gate && grep -q "测试层级不充分" docs/system/workspace/scripts/quality/pretests-retirement-gate && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker: (失败时填写)
^- status: passed

## Unit
- acceptance_target: 文本内容验证
- testing_layer: unit
- target_environment: test-pre-merge-20260625T084506Z-b2-ibm-anti-cheating
- required_evidence: 两条 acceptance 全部 PASS

## Integration
- acceptance_target: gate 脚本语法检查
- testing_layer: integration
- target_environment: test-pre-merge-20260625T084506Z-b2-ibm-anti-cheating
- required_evidence: bash -n 通过
- not_applicable_reason: （本次改动为纯文档/governance，集成测试通过 bash -n 语法检查覆盖）
- not_applicable_explanation: 改动为 skill 文档 + gate 脚本逻辑，无多模块协作。bash -n 语法检查 + grep 文本验证足够。
- replacement_evidence: bash -n pretests-retirement-gate 无语法错误

## End-to-End
- acceptance_target: 完整链路验证——gate 在真实 pre-tests.md 上正确拦截
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260625T084506Z-b2-ibm-anti-cheating → develop merge chain
- required_evidence: gate 对缺少 E2E/集成的 pre-tests.md 返回 non-zero exit code
- not_applicable_reason: documentation_only_change_no_runtime_behavior
- not_applicable_explanation: 本次改动为纯文档/governance（SKILL.md 文本 + gate 脚本检查逻辑），不涉及运行时行为变更。端到端验证需在后续真实 issue 的 pr-create-guarded 流程中由 gate 实际拦截触发，不在本次范围。
- replacement_evidence: 语法检查 + 文本验证通过

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: 改动为 skill/governance 文档，真实环境验证需在后续 PR 流程中体现
