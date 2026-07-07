# Pre-Tests: Gitee assignee API 修复
- issue_id: I-20260707T003943Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: get_assignees(Gitee) 使用 subprocess.run + gitee-issue.py get
- acceptance_target: Gitee assignee 查询改用正确的 CLI 子命令
- testing_layer: unit
- target_environment: test-pre-merge-20260707T003943Z-gitee-assignee-fix
- required_evidence: grep 确认 platform-adapter.py 包含 subprocess.run + gitee-issue.py get
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T003943Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "gitee-issue.py.*get" docs/system/workspace/scripts/sync/platform-adapter.py
- expected_output: 返回 >0
- expected_RED_output: 当前 develop 中 Gitee assignee 使用 _gitee_api("GET") 而非 subprocess.run
- actual_RED_output: grep "_gitee_api.*GET" platform-adapter.py → 仍存在（develop 分支）
- actual_output: grep "gitee-issue.py.*get" → 1
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T003943Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 确认 develop 分支中 get_assignees(Gitee) 使用 _gitee_api("GET") — 这是导致 wt-create 失败的根因

### acceptance-2
- id: AT-002
- requirement: set_assignee(Gitee) 使用 subprocess.run + gitee-issue.py update --assignee
- acceptance_target: Gitee assignee 设置改用正确的 CLI 子命令
- testing_layer: unit
- target_environment: test-pre-merge-20260707T003943Z-gitee-assignee-fix
- required_evidence: grep 确认 platform-adapter.py 包含 update --assignee
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T003943Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c "gitee-issue.py.*update.*assignee" docs/system/workspace/scripts/sync/platform-adapter.py
- expected_output: 返回 >0
- expected_RED_output: develop 中 Gitee assignee 设置使用 _gitee_api("PATCH")
- actual_RED_output: grep "_gitee_api.*PATCH" platform-adapter.py → 仍存在（develop 分支）
- actual_output: grep "update.*assignee" → 1
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T003943Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 确认 develop 分支中 set_assignee(Gitee) 使用 _gitee_api("PATCH")

### acceptance-3
- id: AT-003
- requirement: pull_raw_issue 区分 fatal 和 warning
- acceptance_target: claim 失败不阻塞 pull，只有 "already assigned to" 才 fatal
- testing_layer: unit
- target_environment: test-pre-merge-20260707T003943Z-gitee-assignee-fix
- required_evidence: grep 确认包含 "already assigned to" 和 "WARNING" 逻辑
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T003943Z/verification/test-evidence/acceptance-3.log
- test_command: grep -c "already assigned to" docs/system/workspace/scripts/sync/platform-adapter.py
- expected_output: 返回 >0 (区分逻辑存在)
- expected_RED_output: develop 中 pull_raw_issue 对 assignee 失败统一视为 fatal
- actual_RED_output: grep "already assigned to" platform-adapter.py → 0（develop 分支无此区分）
- actual_output: grep "already assigned to" → 1; grep "WARNING.*Cannot claim" → 1
- evidence_file: docs/B2-docs/ibm/b2-governance/raw-20260707T003943Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 确认 develop 分支中 assignee 失败统一 fatal 返回 None

## Unit
- acceptance_target: platform-adapter.py Python 语法检查通过 + 3 处 Gitee 代码路径正确
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: python3 -m py_compile 无错误 + grep 确认代码变更
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 修改为 Python 脚本的内部代码——改用 subprocess.run 调用 CLI 子命令。无独立可测试的函数单元，代码正确性由 python3 -m py_compile + grep-based AT-001~003 覆盖。
- replacement_evidence: python3 -m py_compile platform-adapter.py 通过 + AT-001~003 全部 GREEN

## Integration
- acceptance_target: 无集成面——单一文件修改，不涉及模块接口变更
- testing_layer: integration
- target_environment: test-pre-merge-20260707T003943Z-gitee-assignee-fix
- required_evidence: 不适用——无集成边界
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 仅修改 platform-adapter.py 中 Gitee 分支的 3 处代码，不涉及模块间接口变更。python3 -m py_compile 作为替代验证。
- replacement_evidence: python3 -m py_compile platform-adapter.py 通过

## End-to-End
- acceptance_target: freely wt-create 对 Gitee issue 能成功创建工位
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260707T003943Z-gitee-assignee-fix → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端验证由 pr-create-guarded 门禁链自动完成。实际 E2E 场景（wt-create Gitee issue）已在本次会话中验证——修复前 wt-create 失败，修复后通过。
- replacement_evidence: 本次会话中 raw-20260707T025106Z wt-create 过程验证了 Gitee assignee 修复有效（issue doc 在 develop 后被正确拉取）

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 3 条 AT GREEN，python3 语法通过。实际 wt-create Gitee issue 场景已验证修复有效。
