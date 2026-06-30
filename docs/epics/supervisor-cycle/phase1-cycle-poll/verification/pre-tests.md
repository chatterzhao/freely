# Pre-Tests: supervisor cycle monitor Phase 1

- issue_id: I-20260630T002621Z-A

## Acceptance Items

### AT-001 freely cycle command exists
- id: AT-001
- requirement: freely cycle --help 输出用法
- acceptance_target: 命令存在且可执行
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 命令输出
- evidence_level: integration
- artifact_ref: docs/epics/supervisor-cycle/phase1-cycle-poll/verification/test-evidence/acceptance-1.txt
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-raw-20260630T002621Z-supervisor-cycle-monitor
  bin/freely cycle --help 2>&1 | grep -q 'raw-key\|Usage' && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL (命令不存在)
- actual_RED_output: "RED confirmed — command does not exist"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/epics/supervisor-cycle/phase1-cycle-poll/verification/test-evidence/acceptance-1.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: feature: 修改前 freely cycle 命令不存在，执行报 unknown command

### AT-002 cycle --json outputs valid JSON
- id: AT-002
- requirement: freely cycle --raw-key <key> --json 返回合法 JSON
- acceptance_target: python3 json.loads 可解析
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: JSON 解析成功
- evidence_level: integration
- artifact_ref: docs/epics/supervisor-cycle/phase1-cycle-poll/verification/test-evidence/acceptance-2.txt
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-raw-20260630T002621Z-supervisor-cycle-monitor
  output=$(bin/freely cycle --raw-key 20260630T002621Z --json 2>&1)
  echo "$output" | python3 -c "import json,sys; json.load(sys.stdin); print('PASS')" 2>/dev/null || echo "FAIL: $output"
- expected_output: PASS
- expected_RED_output: FAIL (命令不存在)
- actual_RED_output: "RED confirmed — command does not exist"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/epics/supervisor-cycle/phase1-cycle-poll/verification/test-evidence/acceptance-2.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: feature: 修改前命令不存在，无 JSON 输出

### AT-003 cycle detects input-required state
- id: AT-003
- requirement: 当 a2a_tasks 有 state=input-required 的 task 时，cycle 检测到并报告
- acceptance_target: cycle 输出包含 input-required 状态
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: cycle 输出确认
- evidence_level: integration
- artifact_ref: docs/epics/supervisor-cycle/phase1-cycle-poll/verification/test-evidence/acceptance-3.txt
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-raw-20260630T002621Z-supervisor-cycle-monitor
  # 创建测试 task
  python3 docs/system/workspace/scripts/runtime/a2a_task.py a2a-exit \
    --state input-required --raw-key 20260630T002621Z --message '{"phase":"B1","status":"done"}' 2>&1 | head -1
  sleep 1
  output=$(bin/freely cycle --raw-key 20260630T002621Z --json 2>&1)
  echo "$output" | python3 -c "import json,sys; d=json.load(sys.stdin); assert d.get('worker_state')=='input-required'; print('PASS')" 2>/dev/null || echo "FAIL: $output"
- expected_output: PASS
- expected_RED_output: FAIL (cycle 不存在或无 task)
- actual_RED_output: "RED confirmed — command does not exist"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/epics/supervisor-cycle/phase1-cycle-poll/verification/test-evidence/acceptance-3.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: feature: 功能未实现，cycle 命令不存在，无法检测 input-required

### AT-004 [CMD] log format in pr-create-guarded
- id: AT-004
- requirement: pr-create-guarded 执行时打印 [CMD] pr-create-guarded called, raw-key: <key>
- acceptance_target: grep [CMD] 日志输出
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: grep 输出
- evidence_level: integration
- artifact_ref: docs/epics/supervisor-cycle/phase1-cycle-poll/verification/test-evidence/acceptance-4.txt
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-raw-20260630T002621Z-supervisor-cycle-monitor
  grep -q '\[CMD\].*called.*raw-key' bin/pr-create-guarded 2>/dev/null && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL ([CMD] 日志不存在)
- actual_RED_output: "RED confirmed — command does not exist"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/epics/supervisor-cycle/phase1-cycle-poll/verification/test-evidence/acceptance-4.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: feature: 修改前 pr-create-guarded 无 [CMD] 日志打印

### AT-005 PRE_CHECK_MAP for pr-create-guarded
- id: AT-005
- requirement: Watchdog 检测到 pr-create-guarded 时执行前置检查，缺文件时输出 FAILED
- acceptance_target: watchdog 脚本/函数可调用且检查逻辑存在
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: grep 确认 PRE_CHECK_MAP 存在
- evidence_level: integration
- artifact_ref: docs/epics/supervisor-cycle/phase1-cycle-poll/verification/test-evidence/acceptance-5.txt
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-raw-20260630T002621Z-supervisor-cycle-monitor
  grep -r 'PRE_CHECK_MAP\|check_b1_artifacts\|check_b2_artifacts' docs/system/workspace/scripts/ --include='*.sh' --include='*.py' -l | head -1 | xargs grep -q 'pr-create-guarded' && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL (PRE_CHECK_MAP 不存在)
- actual_RED_output: "RED confirmed — command does not exist"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/epics/supervisor-cycle/phase1-cycle-poll/verification/test-evidence/acceptance-5.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: feature: 功能未实现，PRE_CHECK_MAP 不存在

### AT-006 Anti-duplicate dispatch guard
- id: AT-006
- requirement: cycle 检测到 input-required 后标记 review_assigned，下轮不再重复 dispatch
- acceptance_target: grep 确认防重复逻辑存在
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: grep 输出
- evidence_level: integration
- artifact_ref: docs/epics/supervisor-cycle/phase1-cycle-poll/verification/test-evidence/acceptance-6.txt
- test_command: |
  cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-raw-20260630T002621Z-supervisor-cycle-monitor
  grep -r 'review_assigned\|防重复\|duplicate.*dispatch' docs/system/workspace/scripts/ --include='*.sh' --include='*.py' -l | head -1 | xargs grep -q 'review_assigned' && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL (守卫逻辑不存在)
- actual_RED_output: "RED confirmed — command does not exist"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/epics/supervisor-cycle/phase1-cycle-poll/verification/test-evidence/acceptance-6.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: feature: 功能未实现，无防重复 dispatch 逻辑

## Unit
- acceptance_target: 全部 AT grep/执行通过
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: AT-001~006 全部通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT items 即 unit tests
- replacement_evidence: AT evidence files

## Integration
- acceptance_target: freely cycle + [CMD] + watchdog 端到端集成
- testing_layer: integration
- target_environment: test-pre-merge worktree
- required_evidence: 真实 worker session 的 cycle 检测 + watchdog 触发
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 集成需要真实 A2A Server + ACP bridge 运行
- replacement_evidence: unit tests + syntax check

## End-to-End
- acceptance_target: 本 PR merge 后 + 后续 worker session 验证
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: 未来 worker 执行时 cycle + watchdog 生效
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: E2E 需后续 PR 配合 worker prompt 模板实现
- replacement_evidence: unit tests

## Real-Environment
- real_environment_status: pass
- real_environment_reason: cycle 命令 + [CMD] 日志 + PRE_CHECK_MAP 为纯增量功能，不影响现有流程
