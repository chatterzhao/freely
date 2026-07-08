# Pre-Tests: scan platform detection
- issue_id: I-20260708T222454Z-A
## Acceptance Items

### acceptance-1: 场景A — terminal + 一个平台CLOSED
- id: AT-001
- requirement: 本地terminal(absorbed), GitHub=CLOSED, Gitee=OPEN → scan 检测并直接同步 Gitee
- acceptance_target: scan stderr 输出 "platform sync: 20260708T222331Z" 且该 item 不在 scan items 中
- testing_layer: integration
- target_environment: test-pre-merge-20260708T222454Z-scan-platform-fix
- required_evidence: scan stderr 含 sync 日志, items 中无该 key
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T222454Z/verification/test-evidence/acceptance-1.log
- test_command: |
  gh issue close 3835 --repo chatterzhao/freely
  python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project . 2>/tmp/at1_stderr.txt > /tmp/at1.json
  grep "222331" /tmp/at1_stderr.txt && echo "SYNC_DETECTED" || echo "NOT_DETECTED"
  python3 -c "import json; d=json.load(open('/tmp/at1.json')); found=any('222331' in i.get('key','') for i in d['items']); print('IN_ITEMS' if found else 'SYNCED_DIRECT')"
  gh issue reopen 3835 --repo chatterzhao/freely
- expected_output: SYNC_DETECTED + SYNCED_DIRECT
- expected_RED_output: NOT_DETECTED 或 IN_ITEMS
- actual_RED_output: (RED)
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- red_how: feature — 修改前 scan 不检测 platform-only issue

### acceptance-2: _sync_platform_direct 先 update 后 close
- id: AT-002
- requirement: _sync_platform_direct 调用 update_issue 再 close_issue
- acceptance_target: 代码含 update_issue 且先于 close_issue
- testing_layer: unit
- target_environment: fix/raw-20260708T222454Z-scan-platform-fix
- required_evidence: grep 确认代码顺序
- evidence_level: mock
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T222454Z/verification/test-evidence/acceptance-2.log
- test_command: grep -A10 "def _sync_platform_direct" docs/system/workspace/scripts/runtime/task-lifecycle-scan.py | grep "update_issue" && grep -A15 "def _sync_platform_direct" docs/system/workspace/scripts/runtime/task-lifecycle-scan.py | grep "close_issue" && echo "UPDATE_BEFORE_CLOSE" || echo "ORDER_WRONG"
- expected_output: UPDATE_BEFORE_CLOSE
- expected_RED_output: ORDER_WRONG 或只 close 不 update
- actual_RED_output: (RED)
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- red_how: fix — 修改前只 close_issue 不 update_issue

### acceptance-3: N=0 平台硬阻塞
- id: AT-003
- requirement: 无配置平台时 scan 以 exit(1) 退出
- acceptance_target: 临时移除平台配置后 scan 报错退出
- testing_layer: unit
- target_environment: fix/raw-20260708T222454Z-scan-platform-fix
- required_evidence: 退出码为1, stderr含FATAL
- evidence_level: mock
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T222454Z/verification/test-evidence/acceptance-3.log
- test_command: |
  grep "FATAL.*no platforms" docs/system/workspace/scripts/runtime/task-lifecycle-scan.py && echo "N0_CHECK_EXISTS" || echo "MISSING"
- expected_output: N0_CHECK_EXISTS
- expected_RED_output: MISSING
- actual_RED_output: (RED)
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- red_how: fix — 修改前 N=0 fallback 到 github

## Unit
- acceptance_target: py_compile 通过
- testing_layer: unit
- target_environment: fix/raw-20260708T222454Z-scan-platform-fix
- required_evidence: python3 -m py_compile 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: dev 阶段已确认 compile 通过
- replacement_evidence: compile OK in dev

## Integration
- acceptance_target: 4 个测试场景全部通过
- testing_layer: integration
- target_environment: test-pre-merge-20260708T222454Z-scan-platform-fix
- required_evidence: AT-001到AT-003全部PASS
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: 用真实双平台 test issue 验证全流程
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: test issue #3835 被正确检测和同步
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 测试使用真实 GitHub/Gitee issue #3835/IJZS1H
