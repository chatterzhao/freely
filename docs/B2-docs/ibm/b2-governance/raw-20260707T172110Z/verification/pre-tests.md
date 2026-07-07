# Pre-Tests: scan fix
- issue_id: I-20260707T172110Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: scan --project 参数正确 + 返回 >0 items
- testing_layer: unit
- target_environment: test-pre-merge-20260707T172110Z-scan-argparse-fix
- required_evidence: scan 输出确认
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T172110Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project . --json 2>&1 | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('items',[])))"
- expected_output: ">0"
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前返回 0 items
## Unit
- acceptance_target: py_compile + scan 输出 >0
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 不适用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: py_compile + scan 行为测试
- replacement_evidence: AT-001
## Integration
- acceptance_target: 无集成面
- testing_layer: integration
- target_environment: test-pre-merge-20260707T172110Z-scan-argparse-fix
- required_evidence: 不适用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯 Python 修改
- replacement_evidence: AT-001
## End-to-End
- acceptance_target: pr-create-guarded 门禁链
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 门禁链覆盖
- replacement_evidence: pr-create-guarded gate chain
## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT-001: scan 返回 273 items
