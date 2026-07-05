# Pre-Tests
- issue_id: I-20260703T080443Z-A

## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: daemon startup writes __manager__ record to agent_working
- acceptance_target: agent_working.get_all returns __manager__ row after daemon start
- testing_layer: end-to-end
- surface_kind: end_to_end
- target_lane: premerge-integration  
- promotion_gate: develop_merge
- task_refs: A1
- case_design: start daemon, verify agent_working table has __manager__ row
- target_environment: test-pre-merge
- required_evidence: rows=1 with raw_key=__manager__, manager_id=manager_01
- evidence_level: real_env
- artifact_ref: docs/B2-docs/git-worktree/closeout/raw-20260703T080443Z43Z/verification/test-evidence/acceptance-1.log
- test_command: python3 -c "from agent_working import _db_rpc; r=_db_rpc('.','agent_working.get_all',{}); assert len(r.get('rows',[]))==1"
- expected_output: rows=1
- expected_RED_output: rows=0
- actual_RED_output: rows=0 (IDN residual_risk documented gap)
- actual_output: rows=1, __manager__ record confirmed
- evidence_file: docs/B2-docs/git-worktree/closeout/raw-20260703T080443Z43Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: fix: 修复前 daemon 启动后 agent_working 表为空

### acceptance-2
- id: AT-002
- requirement: start-lead-agent.sh no longer errors on meta_env_value
- acceptance_target: daemon start log has no "meta_env_value: command not found"
- testing_layer: integration
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: A2
- case_design: start daemon, check log for meta_env_value errors
- target_environment: test-pre-merge
- required_evidence: log has no meta_env_value error
- evidence_level: real_env
- artifact_ref: docs/B2-docs/git-worktree/closeout/raw-20260703T080443Z43Z/verification/test-evidence/acceptance-2.log
- test_command: grep "meta_env_value: command not found" .freely/logs/daemon-launch.log && echo FAIL || echo PASS
- expected_output: PASS
- expected_RED_output: meta_env_value: command not found
- actual_RED_output: meta_env_value: command not found at line 146
- actual_output: no meta_env_value errors in latest daemon start
- evidence_file: docs/B2-docs/git-worktree/closeout/raw-20260703T080443Z43Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- red_how: fix: 修复前 start-lead-agent.sh:146 报 meta_env_value 未找到

## Unit
- acceptance_target: code review
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: syntax check passes
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/002 覆盖端到端验证
- replacement_evidence: AT-001/002 acceptance logs

## Integration
- acceptance_target: full daemon flow
- testing_layer: integration
- target_environment: test-pre-merge
- required_evidence: daemon starts without errors
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/002 覆盖
- replacement_evidence: AT-001/002 acceptance logs

## End-to-End
- acceptance_target: full daemon flow
- testing_layer: end-to-end
- target_environment: test-pre-merge
- required_evidence: daemon starts without errors
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/002 覆盖
- replacement_evidence: AT-001/002 acceptance logs

## Real-Environment
- real_environment_status: pass
- real_environment_reason: daemon 在 test-pre-merge 中验证通过
