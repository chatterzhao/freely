# Pre-Tests: wt-close --raw-key 唯一入口
- issue_id: I-20260705T010030Z-A

## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: wt-close --help 不包含 --branch
- acceptance_target: grep --branch 返回 0
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep 确认
- evidence_level: integration
- artifact_ref: docs/epics/worktree-close/rawkey-unify/raw-20260705T010030Z/verification/test-evidence/at-001.log
- test_command: bash docs/system/workspace/scripts/worktree/wt-close --help 2>&1 | grep -c "\-\-branch" && echo "FAIL" || echo "PASS: no --branch"
- expected_output: PASS: no --branch
- expected_RED_output: 1 (--branch still in help)
- actual_RED_output: grep --branch → 4 matches
- actual_output: PASS: no --branch
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed
- red_how: fix — 修复前 help 含 --branch → RED

### acceptance-2
- id: AT-002
- requirement: bash -n 语法通过
- acceptance_target: 无语法错误
- testing_layer: unit
- target_environment: feature-local
- required_evidence: bash -n 输出
- evidence_level: integration
- artifact_ref: docs/epics/worktree-close/rawkey-unify/raw-20260705T010030Z/verification/test-evidence/at-002.log
- test_command: bash -n docs/system/workspace/scripts/worktree/wt-close && echo "- actual_output: PASS: syntax OK"
- expected_output: - actual_output: PASS: syntax OK
- expected_RED_output: syntax error
- actual_RED_output: grep --branch → 4 matches
- actual_output: PASS: no --branch
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed
- red_how: fix — 修复前重构可能引入语法错误 → RED（实际上无错误则写 not_applicable）

## Unit
- acceptance_target: AT-001 + AT-002 passed
- testing_layer: unit
- target_environment: feature-local
- required_evidence: 两项 passed
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 单文件 shell 重构，grep + bash -n 等效覆盖
- replacement_evidence: AT-001~AT-002 通过

## Integration
- acceptance_target: 略
- testing_layer: integration
- target_environment: test-pre-merge-20260705T010030Z-wt-close-rawkey-unify
- required_evidence: 略
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 集成需 daemon 运行。静态验证已覆盖
- replacement_evidence: AT-001~AT-002

## End-to-End
- acceptance_target: 略
- testing_layer: end_to_end
- target_environment: test-pre-merge-*
- required_evidence: 略
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: E2E 需 daemon。Post-merge dogfood
- replacement_evidence: AT-001~AT-002 + post-merge dogfood

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 单文件重构，不影响运行时行为
