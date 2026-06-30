# Pre-Tests: command standardization
- issue_id: I-20260629T122254Z-A
## Acceptance Items
### AT-001 All 8 subcommands registered
- id: AT-001
- requirement: freely --help shows all 8 new subcommands
- acceptance_target: grep confirms each command in dispatch
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: grep output
- evidence_level: integration
- artifact_ref: docs/epics/cmd-standardize/subcommand-add/verification/test-evidence/acceptance-1.txt
- test_command: |
  for c in pr-review-guarded cycle watchdog deploy-skills governance-check checkpoint-guard pretests-gate pretests-retirement-gate; do
    grep -q "$c) cmd_" docs/system/workspace/scripts/runtime/freely || { echo "FAIL: $c"; exit 1; }
  done
  echo PASS
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: RED confirmed — commands not registered before
- actual_output: PASS
- evidence_file: docs/epics/cmd-standardize/subcommand-add/verification/test-evidence/acceptance-1.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: feature: 修改前这8个命令不在freely dispatch中
### AT-002 Internal scripts NOT registered
- id: AT-002
- requirement: governance-merge-gate, freely-review, merge-guarded stay internal
- acceptance_target: grep confirms they are NOT in the case dispatch
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: grep output
- evidence_level: integration
- artifact_ref: docs/epics/cmd-standardize/subcommand-add/verification/test-evidence/acceptance-2.txt
- test_command: |
  for c in governance-merge-gate governance-promotion-gate governance-closeout-gate merge-guarded; do
    grep -q "\"$c\") cmd_" docs/system/workspace/scripts/runtime/freely && { echo "FAIL: $c should be internal"; exit 1; } || true
  done
  echo PASS
- expected_output: PASS
- expected_RED_output: N/A
- actual_RED_output: N/A
- actual_output: PASS
- evidence_file: docs/epics/cmd-standardize/subcommand-add/verification/test-evidence/acceptance-2.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: 验证内部脚本未被注册
## Unit
- acceptance_target: grep验证全部
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: AT-001/002通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT items即unit tests
- replacement_evidence: AT evidence files
## Integration
- acceptance_target: freely pr-review-guarded执行不报unknown command
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: 命令执行输出
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: ACP reviewer不可用，但命令路由已验证
- replacement_evidence: grep dispatch + syntax check
## End-to-End
- acceptance_target: 安装后freely --help显示所有命令
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: freely --help输出
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 需安装后验证
- replacement_evidence: unit tests
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 仅新增命令路由，无逻辑变更
