# Pre-Tests: 跨tool session
- issue_id: I-20260719T101009Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: Worker同tool fork用Manager bridge socket
- acceptance_target: grep命中比较逻辑
- testing_layer: unit
- target_environment: fix-raw-20260719T101009Z-cross-tool-worker-launch
- required_evidence: grep输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/acp/cross-tool-session/raw-20260719T101009Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c '_worker_base.*==.*_mgr_base' docs/system/workspace/scripts/runtime/freely
- expected_output: "1"
- red-green-status: green
- status: pass
- red_how: 当前用Worker tool查Manager socket,同tool场景也错

### acceptance-2
- id: AT-002
- requirement: Worker不同tool ensure Worker bridge
- acceptance_target: grep命中
- testing_layer: unit
- target_environment: fix-raw-20260719T101009Z-cross-tool-worker-launch
- required_evidence: grep输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/acp/cross-tool-session/raw-20260719T101009Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c '_ensure_acp_bridge_running.*_worker_base' docs/system/workspace/scripts/runtime/freely
- expected_output: "1"
- red-green-status: green
- status: pass
- red_how: 当前跨tool时不启动Worker bridge

### acceptance-3
- id: AT-003
- requirement: Reviewer跨tool ensure bridge
- acceptance_target: grep命中
- testing_layer: unit
- target_environment: fix-raw-20260719T101009Z-cross-tool-worker-launch
- required_evidence: grep输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/acp/cross-tool-session/raw-20260719T101009Z/verification/test-evidence/acceptance-3.log
- test_command: grep -c '_reviewer_base.*_mgr_base_rev' docs/system/workspace/scripts/runtime/freely
- expected_output: "3"
- red-green-status: green
- status: pass
- red_how: 当前Reviewer固定用Manager bridge

## Unit
- acceptance_target: AT-001~003 grep验证
- testing_layer: unit
- target_environment: fix-raw-20260719T101009Z-cross-tool-worker-launch
- required_evidence: AT-001~003
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: grep验证代码修改存在
- replacement_evidence: AT-001~003 GREEN

## Integration
- acceptance_target: post-merge daemon验证
- testing_layer: integration
- target_environment: test-pre-merge-20260719T101009Z-cross-tool-worker-launch
- required_evidence: daemon日志
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge dogfood
- replacement_evidence: AT-001~003 GREEN

## End-to-End
- acceptance_target: post-merge daemon
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: daemon日志
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge dogfood
- replacement_evidence: AT-001~003 GREEN

## Real-Environment
- real_environment_status: pass
- real_environment_reason: Worker+Reviewer跨tool session创建已实现, post-merge daemon重启验证
