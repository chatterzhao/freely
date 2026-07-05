# Pre-Tests: 移除 git 跟踪的 .pyc 文件
- issue_id: I-20260703T051533Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 所有 .pyc 文件不再被 git 跟踪
- acceptance_target: git ls-files '*.pyc' 返回空
- testing_layer: unit
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- task_refs: A1
- case_design: 验证 git rm --cached 后没有 .pyc 文件在 git 索引中
- target_environment: test-pre-merge-20260703T051533Z-pycache-gitignore
- required_evidence: git ls-files 输出为 0
- evidence_level: integration
- artifact_ref: docs/epics/git-hygiene/untracked-pycache/raw-20260703T051533Z/verification/test-evidence/acceptance-1.log
- test_command: test $(git ls-files '*.pyc' | wc -l) -eq 0 && echo "PASS: no pyc files tracked" || echo "FAIL"
- expected_output: PASS: no pyc files tracked
- expected_RED_output: 6 个 .pyc 文件被 git 跟踪
- actual_RED_output: git ls-files '*.pyc' | wc -l → 6
- actual_output: PASS: no pyc files tracked
- evidence_file: docs/epics/git-hygiene/untracked-pycache/raw-20260703T051533Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: fix: 修复前 git ls-files *.pyc 返回 6 个文件

### acceptance-2
- id: AT-002
- requirement: daemon 可以正常启动
- acceptance_target: daemon start 成功
- testing_layer: end-to-end
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: A1,A2
- case_design: 在 test-pre-merge 工位验证 daemon 启动不再因 dirty tree 失败
- target_environment: test-pre-merge-20260703T051533Z-pycache-gitignore
- required_evidence: daemon_status: running
- evidence_level: real_env
- artifact_ref: docs/epics/git-hygiene/untracked-pycache/raw-20260703T051533Z/verification/test-evidence/acceptance-2.log
- test_command: ./bin/freely daemon start --task-mode auto --project $(pwd)
- expected_output: daemon_status: running
- expected_RED_output: develop working tree is dirty — cannot start daemon
- actual_RED_output: develop working tree is dirty — cannot start daemon. Modified: __pycache__/agent_working.cpython-314.pyc
- actual_output: daemon_status: running, supervisor_pid 非空
- evidence_file: docs/epics/git-hygiene/untracked-pycache/raw-20260703T051533Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- red_how: fix: 修复前 daemon start 因 dirty tree 失败

## Unit
- acceptance_target: git ls-files 验证
- testing_layer: unit
- target_environment: test-pre-merge-20260703T051533Z-pycache-gitignore
- required_evidence: 无 .pyc 被跟踪
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖了单元验证
- replacement_evidence: AT-001 结果

## Integration
- acceptance_target: daemon 启动集成验证
- testing_layer: integration
- target_environment: test-pre-merge-20260703T051533Z-pycache-gitignore
- required_evidence: daemon 正常启动
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-002 覆盖了集成验证
- replacement_evidence: AT-002 结果

## End-to-End
- acceptance_target: daemon 端到端启动
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260703T051533Z-pycache-gitignore → develop merge chain
- required_evidence: daemon 正常运行
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-002 就是端到端测试
- replacement_evidence: AT-002 结果

## Real-Environment
- real_environment_status: pass
- real_environment_reason: develop daemon 在修复 pyc 后成功启动
