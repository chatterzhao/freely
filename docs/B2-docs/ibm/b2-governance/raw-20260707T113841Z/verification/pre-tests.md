# Pre-Tests: Review Gate
- issue_id: I-20260707T113841Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: agent_working.py 有 review verdict 函数
- acceptance_target: agent_record_review + agent_find_first_missing_review 存在
- testing_layer: unit
- target_environment: test-pre-merge-20260707T113841Z-phase-review-gate
- required_evidence: python3 -m py_compile 通过 + grep 确认函数
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T113841Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "agent_record_review\|agent_find_first_missing_review" docs/system/workspace/scripts/runtime/agent_working.py
- expected_output: ">=2"
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前 agent_working.py 无 review verdict 函数
### acceptance-2
- id: AT-002
- requirement: freely-review ACP 不可用时 exit 1（非 exit 0）
- acceptance_target: grep 确认代码含 exit 1 + ACP bridge 不可用提示
- testing_layer: unit
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T113841Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c "ACP bridge 不可用" bin/freely-review
- expected_output: ">=1"
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前 ACP 不可用时 exit 0 静默跳过
### acceptance-3
- id: AT-003
- requirement: pr-create-guarded 包含 review signature 检查
- acceptance_target: Step 2c2 存在 + review check 逻辑
- testing_layer: unit
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T113841Z/verification/test-evidence/acceptance-3.log
- test_command: grep -c "REVIEW-GATE\|review signature" docs/system/workspace/scripts/worktree/pr-create-guarded
- expected_output: ">=2"
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前无 review signature 检查
## Unit
- acceptance_target: Python + bash 语法全部通过
- testing_layer: unit
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯函数添加，python3 -m py_compile + bash -n 作为验证
- replacement_evidence: 三个文件语法检查全部通过
## Integration
- acceptance_target: review gate 与现有 gate chain 不冲突
- testing_layer: integration
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 新增 gate step 是独立检查，不与现有 gate 交互
- replacement_evidence: bash -n pr-create-guarded 通过
## End-to-End
- acceptance_target: pr-create-guarded 门禁链通过
- testing_layer: end-to-end
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 门禁链覆盖
- replacement_evidence: pr-create-guarded gate chain
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 3 AT GREEN
