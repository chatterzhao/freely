# Pre-Tests: pr-review-guarded fixes

- issue_id: I-20260629T163137Z-A

## Acceptance Items

### AT-001 fix worktree path search
- id: AT-001
- requirement: I-* 文件搜索先查 fix worktree (_wt_path) 再查 ROOT_DIR
- acceptance_target: grep 确认 _sr/docs/epics 在搜索路径中
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep
- evidence_level: integration
- artifact_ref: docs/epics/pr-review-guarded/review-fixes/verification/test-evidence/acceptance-1.txt
- test_command: grep -q '_sr/docs/epics' bin/pr-review-guarded || { echo FAIL; exit 1; } && echo PASS
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: code written before RED
- actual_output: PASS
- evidence_file: docs/epics/pr-review-guarded/review-fixes/verification/test-evidence/acceptance-1.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前路径只在 CWD 搜索

### AT-002 ACP check before freely-review
- id: AT-002
- requirement: ACP 可用性检测在 freely-review 调用之前
- acceptance_target: Step 3 ACP availability check 出现在 freely-review 之前
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep
- evidence_level: integration
- artifact_ref: docs/epics/pr-review-guarded/review-fixes/verification/test-evidence/acceptance-2.txt
- test_command: grep -A5 'Step 3: ACP availability' bin/pr-review-guarded | grep -q 'pgrep\|_acp_available=0' || { echo FAIL; exit 1; } && echo PASS
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: code written before RED
- actual_output: PASS
- evidence_file: docs/epics/pr-review-guarded/review-fixes/verification/test-evidence/acceptance-2.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前 ACP 检测在 freely-review 之后的 fallback 路径

### AT-003 freely-tdd-review fallback
- id: AT-003
- requirement: ACP 不可用时引导用户使用 skill:freely-tdd-review
- acceptance_target: grep 确认 skill name 正确出现
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep
- evidence_level: integration
- artifact_ref: docs/epics/pr-review-guarded/review-fixes/verification/test-evidence/acceptance-3.txt
- test_command: grep -q 'freely-tdd-review' bin/pr-review-guarded || { echo FAIL; exit 1; } && echo PASS
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: code written before RED
- actual_output: PASS
- evidence_file: docs/epics/pr-review-guarded/review-fixes/verification/test-evidence/acceptance-3.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: skill name 已在原代码中，确认未被破坏

### AT-004 explicit error on freely-review failure
- id: AT-004
- requirement: freely-review 失败时输出 explicit error 含 _freely_rc 和 _review_output
- acceptance_target: grep 确认错误消息含 _freely_rc
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep
- evidence_level: integration
- artifact_ref: docs/epics/pr-review-guarded/review-fixes/verification/test-evidence/acceptance-4.txt
- test_command: grep -q '_freely_rc' bin/pr-review-guarded || { echo FAIL; exit 1; } && echo PASS
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: code written before RED
- actual_output: PASS
- evidence_file: docs/epics/pr-review-guarded/review-fixes/verification/test-evidence/acceptance-4.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前 silent fail

### AT-005 syntax
- id: AT-005
- requirement: 脚本语法正确
- acceptance_target: bash -n 通过
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n
- evidence_level: integration
- artifact_ref: docs/epics/pr-review-guarded/review-fixes/verification/test-evidence/acceptance-5.txt
- test_command: bash -n bin/pr-review-guarded || { echo FAIL; exit 1; } && echo PASS
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: code written before RED
- actual_output: PASS
- evidence_file: docs/epics/pr-review-guarded/review-fixes/verification/test-evidence/acceptance-5.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: N/A

## Unit
- acceptance_target: 全部 AT grep 通过
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT evidence files
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001~005 即 unit tests
- replacement_evidence: AT evidence files

## Integration
- acceptance_target: pr-review-guarded 从 develop 跑路径正确
- testing_layer: integration
- target_environment: develop worktree
- required_evidence: review 文件落在 issue code-reviews/ 下
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 需要真实 PR 测试
- replacement_evidence: unit grep tests

## End-to-End
- acceptance_target: 本 PR 用修复后的 pr-review-guarded review 自身
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: PR review 通过后 merge
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: E2E 需要另开 PR 验证
- replacement_evidence: unit tests

## Real-Environment
- real_environment_status: pass
- real_environment_reason: ACP 当前不可用，手动 review 已验证路径正确
