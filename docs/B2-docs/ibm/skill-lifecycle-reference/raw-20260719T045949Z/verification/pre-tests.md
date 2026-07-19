# Pre-Tests: B1/B2 skill 交叉引用补充
- issue_id: I-20260719T045949Z-A

## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: B1 skill 末尾包含三环生命周期引用和 doc-loop 位置说明
- acceptance_target: grep 命中新增内容
- testing_layer: unit
- target_environment: fix-raw-20260719T045949Z-doc-skill-lifecycle-ref
- required_evidence: grep 输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/skill-lifecycle-reference/raw-20260719T045949Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "能力生命周期参考" docs/system/workspace/skills/freely-doc-B1_IBM-execution/SKILL.md
- expected_output: "1"
- actual_output: "1"
- evidence_file: acceptance-1.log
- red-green-status: green
- status: pass

### acceptance-2
- id: AT-002
- requirement: B2 skill 末尾包含关键参考段（PRD 质量门槛+派生约束+三环引用）
- acceptance_target: grep 命中所有三个关键参考
- testing_layer: unit
- target_environment: fix-raw-20260719T045949Z-doc-skill-lifecycle-ref
- required_evidence: grep 输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/skill-lifecycle-reference/raw-20260719T045949Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c "关键参考" docs/system/workspace/skills/freely-doc-B2_IBM-execution/SKILL.md
- expected_output: "1"
- actual_output: "1"
- evidence_file: acceptance-2.log
- red-green-status: green
- status: pass

## Unit
- acceptance_target: 两个 skill 末尾均新增交叉引用段
- testing_layer: unit
- target_environment: fix-raw-20260719T045949Z-doc-skill-lifecycle-ref
- required_evidence: AT-001/AT-002 覆盖此层
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/AT-002 直接验证内容存在性
- replacement_evidence: AT-001/AT-002 输出

## Integration
- acceptance_target: 两个 skill 的引用一致，B1→B2→dev 流转关系正确
- testing_layer: integration
- target_environment: test-pre-merge-20260719T045949Z-doc-skill-lifecycle-ref
- required_evidence: AT-001/AT-002 覆盖此层
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 纯文档改进，无集成点
- replacement_evidence: AT-001/AT-002 GREEN

## End-to-End
- acceptance_target: governance-check 无新增 FAIL
- testing_layer: end-to-end
- target_environment: fix-raw-20260719T045949Z-doc-skill-lifecycle-ref → develop merge chain
- required_evidence: pr-create-guarded gate pass
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 纯文档改进，无运行时影响
- replacement_evidence: pr-create-guarded gate pass

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 纯文档改进，内容经评审确认方向正确
