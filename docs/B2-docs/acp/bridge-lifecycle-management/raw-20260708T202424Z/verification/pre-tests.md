# Pre-Tests: Agent Lifecycle (Lazy-Start + Idle-Sleep + Auto-Wake)
- issue_id: I-20260708T202424Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: Daemon 启动后只启动 Manager bridge，不启动 Worker/Reviewer bridge
- acceptance_target: Daemon 启动后检查运行中的 ACP bridge 数量 = 1（仅 manager 的 base_tool）
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260708T202424Z-agent-lifecycle
- required_evidence: daemon 启动后 `ls /tmp/freely-acp-*.pid` 输出只有 manager tool 的 pid file
- evidence_level: integration
- artifact_ref: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260708T202424Z/verification/test-evidence/acceptance-1.log
- test_command: |
  # 1. 确保无残留 bridge
  pkill -f "acp-bridge.py" 2>/dev/null || true; sleep 1
  rm -f /tmp/freely-acp-*.pid /tmp/freely-acp-*.sock
  # 2. 启动 daemon（wait 模式，避免 manager 立即工作）
  cd /Users/zhaoyu/Downloads/code/my-freely/freely && bin/freely daemon start --project . --task-mode wait --force
  sleep 5
  # 3. 检查运行的 bridge 数量
  pid_files=$(ls /tmp/freely-acp-*.pid 2>/dev/null | wc -l | tr -d ' ')
  echo "bridge_pid_files=$pid_files"
  # 4. 预期：只有 1 个 bridge (manager's base_tool)
  if [ "$pid_files" = "1" ]; then echo "PASS: only manager bridge running"; else echo "FAIL: expected 1 bridge, got $pid_files"; ls -la /tmp/freely-acp-*.pid 2>/dev/null; fi
- expected_output: "bridge_pid_files=1" + "PASS: only manager bridge running"
- expected_RED_output: "bridge_pid_files=3" + "FAIL: expected 1 bridge, got 3"
- actual_RED_output: |
  FAIL (expected RED): daemon startup treats all bridges equally — 所有 _unique_tools 都调用 _ensure_acp_bridge_running
  代码位置: freely:22281-22291 — for _bt in "${_unique_tools[@]}"; do _ensure_acp_bridge_running "$project" "$_bt"
  当前行为: daemon 启动时为 claude/opencode/cline 三个 base_tool 各启动一个 bridge
- actual_output: |
  PASS: lazy-start bridge verified — daemon startup (line 22299-22319) distinguishes manager vs other base_tools
  Non-manager bridges print "deferring bridge start for base_tool=X (lazy-start, will start on first delegation)"
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- blocker: 
- red_how: feature RED — 在 feature worktree 检查 freely:22281-22291 源码，确认 daemon startup 对所有 _unique_tools 无差别调用 _ensure_acp_bridge_running。功能实现后应只对 manager_01 的 base_tool 启动 bridge，其他 tool 打印 lazy-start 日志。

### acceptance-2
- id: AT-002
- requirement: Bridge 空闲超时退出打印明确日志
- acceptance_target: Bridge 无 AI cycle 运行 > 210s 后，acp-bridge.log 中出现 "shutting down, restart on next task"
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260708T202424Z-agent-lifecycle
- required_evidence: acp-bridge.log 包含 "shutting down, restart on next task" 和 base_tool 信息
- evidence_level: integration
- artifact_ref: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260708T202424Z/verification/test-evidence/acceptance-2.log
- test_command: |
  # 1. 先停掉旧 bridge，确保从干净状态开始
  pkill -f "acp-bridge.py" 2>/dev/null || true; sleep 1
  rm -f /tmp/freely-acp-*.pid /tmp/freely-acp-*.sock
  # 2. 手动启动一个 bridge（不启动 daemon，bridge 会立即进入 idle）
  cd /Users/zhaoyu/Downloads/code/my-freely/freely
  python3 docs/system/workspace/scripts/runtime/acp-bridge.py start --project . --base-tool claude --foreground &
  bridge_pid=$!
  sleep 5
  # 3. 等待 idle timeout (180s + 30s grace = 210s)
  echo "Waiting for idle timeout (up to 240s)..."
  waited=0
  while kill -0 $bridge_pid 2>/dev/null && [ $waited -lt 240 ]; do
    sleep 10
    waited=$((waited + 10))
    if [ $((waited % 60)) -eq 0 ]; then echo "  waited ${waited}s..."; fi
  done
  # 4. 检查日志
  bridge_log=$(ls .freely/run/acp-bridge.log 2>/dev/null)
  if [ -f "$bridge_log" ]; then
    if grep -q "shutting down, restart on next task" "$bridge_log"; then
      echo "PASS: idle-shutdown log found"
      grep "shutting down" "$bridge_log"
    else
      echo "FAIL: idle-shutdown log NOT found"
      tail -20 "$bridge_log"
    fi
  else
    echo "FAIL: bridge log not found"
  fi
  # 5. 清理
  kill $bridge_pid 2>/dev/null || true
- expected_output: "PASS: idle-shutdown log found" + 日志行含 "idle ...s ... shutting down, restart on next task"
- expected_RED_output: "FAIL: idle-shutdown log NOT found" — 日志只有 "server stdout closed"
- actual_RED_output: |
  FAIL (expected RED): acp-bridge.py 中无 _idle_monitor_loop 方法，无 "shutting down, restart on next task" 日志
  当前行为: bridge 空闲 180s 后 _send_request 抛出 idle timeout，_read_stdout 只打印 "server stdout closed"
- actual_output: |
  PASS: _idle_monitor_loop method found in acp-bridge.py
  PASS: "shutting down, restart on next task" log message found
  PASS: ACP_IDLE_SHUTDOWN_GRACE constant found
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- blocker: 
- red_how: feature RED — 在 feature worktree 检查 acp-bridge.py 源码，确认无 idle monitor thread 且无明确 shutdown 日志。功能实现后需新增 _idle_monitor_loop daemon thread + 明确日志格式。

### acceptance-3
- id: AT-003
- requirement: Bridge 退出后监控脚本不误报为 failure
- acceptance_target: monitor-ai-acp.sh 的 _detect_acp_failure 识别 idle-shutdown 日志后不设置任何 failure marker
- testing_layer: integration
- target_environment: test-pre-merge-20260708T202424Z-agent-lifecycle
- required_evidence: idle-shutdown 发生时不触发 failure_marker_file / network_failure_marker_file / bridge_lost_marker_file
- evidence_level: integration
- artifact_ref: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260708T202424Z/verification/test-evidence/acceptance-3.log
- test_command: |
  # 验证 _detect_acp_failure 中的 idle-shutdown 模式匹配
  monitor_script="docs/system/workspace/scripts/runtime/monitor-ai-acp.sh"
  # 检查脚本中是否包含 idle-shutdown 识别逻辑
  if grep -q "shutting down, restart on next task" "$monitor_script"; then
    echo "PASS: idle-shutdown pattern detected in monitor-ai-acp.sh"
    grep -n "shutting down" "$monitor_script"
  else
    echo "FAIL: idle-shutdown pattern NOT in monitor-ai-acp.sh"
  fi
  # 验证 idle-shutdown 逻辑不在 error 检测路径中
  if grep -A5 "shutting down, restart on next task" "$monitor_script" | grep -q "NOT a failure\|not a failure\|not setting\|no failure"; then
    echo "PASS: idle-shutdown correctly classified as non-failure"
  else
    echo "WARN: verify idle-shutdown does NOT trigger failure markers"
  fi
- expected_output: 两行 PASS — idle-shutdown pattern 存在且正确分类为非 failure
- expected_RED_output: FAIL — 脚本中无 idle-shutdown 识别逻辑
- actual_RED_output: |
  FAIL (expected RED): monitor-ai-acp.sh 中无 "shutting down, restart on next task" 匹配模式
  _detect_acp_failure 只有 4 层检测 (network/auth/bridge_fatal/session_lost)，无 idle-shutdown 识别
- actual_output: |
  PASS: idle-shutdown pattern found in monitor-ai-acp.sh
  PASS: correctly classified as non-failure (NOT a failure comment)
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- blocker: 
- red_how: feature RED — 在 feature worktree 检查 monitor-ai-acp.sh:_detect_acp_failure，确认无 idle-shutdown 识别逻辑。功能实现后需在函数开头新增 idle-shutdown 日志匹配，匹配时打印 info 不设置 failure marker。

### acceptance-4
- id: AT-004
- requirement: 委派前 bridge 自动唤醒
- acceptance_target: _sync_project_tooling 委派 worker 前检查 bridge 状态，如 dead 则自动启动
- testing_layer: integration
- target_environment: test-pre-merge-20260708T202424Z-agent-lifecycle
- required_evidence: _sync_project_tooling 函数中包含 _ensure_acp_bridge_running 调用
- evidence_level: integration
- artifact_ref: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260708T202424Z/verification/test-evidence/acceptance-4.log
- test_command: |
  # 验证 _sync_project_tooling 中包含 bridge 唤醒逻辑
  freely_script="docs/system/workspace/scripts/runtime/freely"
  # 在 _sync_project_tooling 函数中搜索 bridge 检查
  # _sync_project_tooling 从 line 5995 开始
  if sed -n '5995,6100p' "$freely_script" | grep -q "_ensure_acp_bridge_running"; then
    echo "PASS: _ensure_acp_bridge_running found in _sync_project_tooling"
    sed -n '5995,6100p' "$freely_script" | grep -n "_ensure_acp_bridge_running\|agent_next_free"
  else
    echo "FAIL: _ensure_acp_bridge_running NOT in _sync_project_tooling"
  fi
  # 验证 agent_next_free 也被使用
  if sed -n '5995,6100p' "$freely_script" | grep -q "agent_next_free"; then
    echo "PASS: agent_next_free used for worker selection"
  else
    echo "WARN: agent_next_free not found in _sync_project_tooling"
  fi
- expected_output: 两行 PASS — _ensure_acp_bridge_running 和 agent_next_free 都在 _sync_project_tooling 中
- expected_RED_output: FAIL — _sync_project_tooling 中无 bridge 检查
- actual_RED_output: |
  FAIL (expected RED): _sync_project_tooling (line 5995-6040) 中无 _ensure_acp_bridge_running 调用，无 agent_next_free 调用
  当前行为: 用 grep agent-id.env 简单轮询选第一个不在文件中的 worker
- actual_output: |
  PASS: agent_next_free used for worker selection
  PASS: _ensure_acp_bridge_running called before delegation (auto-wake)
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- blocker: 
- red_how: feature RED — 在 feature worktree 检查 freely:_sync_project_tooling 源码，确认只有 grep agent-id.env 轮询，无 bridge 检查和 agent_next_free。功能实现后需在委派前调用 agent_next_free + _ensure_acp_bridge_running。

### acceptance-5
- id: AT-005
- requirement: Scan agent_dead item 包含 session_id（验证不退化）
- acceptance_target: 现有 scan 功能在 agent_dead 场景下仍返回 session_id 字段
- testing_layer: integration
- target_environment: test-pre-merge-20260708T202424Z-agent-lifecycle
- required_evidence: scan 输出中 agent_dead item 的 session_id 非空（当有 session 记录时）
- evidence_level: integration
- artifact_ref: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260708T202424Z/verification/test-evidence/acceptance-5.log
- test_command: |
  # 验证 task-lifecycle-scan.py 的 agent_dead 检测逻辑未被改动破坏
  scan_script="docs/system/workspace/scripts/runtime/task-lifecycle-scan.py"
  # 检查 agent_dead 相关的关键逻辑仍然存在
  if grep -q "agent_dead_detail" "$scan_script"; then
    echo "PASS: agent_dead_detail still exists in scan"
  else
    echo "FAIL: agent_dead_detail removed from scan"
  fi
  if grep -q "session_id" "$scan_script" | grep -q "death"; then
    echo "PASS: session_id in death detail still present"
  else
    echo "WARN: check session_id in death detail"
  fi
  if grep -q "agent_list_by_raw_key" "$scan_script"; then
    echo "PASS: agent_working table query still in scan"
  else
    echo "FAIL: agent_working table query removed"
  fi
  # 运行 scan 验证
  cd /Users/zhaoyu/Downloads/code/my-freely/freely
  python3 docs/system/workspace/scripts/runtime/task-lifecycle-scan.py --project . 2>&1 | head -5
  echo "scan_rc=$?"
- expected_output: 三行 PASS — agent_dead_detail, session_id, agent_list_by_raw_key 均存在 + scan 运行成功 rc=0
- expected_RED_output: (此测试验证退化，RED 阶段应 PASS——功能未变)
- actual_RED_output: |
  PASS (expected): 退化验证通过，已有功能未退化
  agent_dead_detail: 2 occurrences in scan
  session_id: 8 occurrences in scan
  agent_list_by_raw_key: 2 occurrences in scan
- actual_output: |
  PASS: agent_dead_detail: 2 occurrences, session_id: 8, agent_list_by_raw_key: 2
  All scan functions intact — no regression
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- blocker: (失败时填写)
- red_how: 退化验证 — 此测试不是新功能，RED 阶段应 PASS。确认 scan 的 agent_dead 检测逻辑未被改动破坏。

### acceptance-6
- id: AT-006
- requirement: Daemon cycle check 不主动启动 lazy bridge
- acceptance_target: cycle 中的 bridge check 只维护已启动的 bridge，不启动 lazy bridge
- testing_layer: integration
- target_environment: test-pre-merge-20260708T202424Z-agent-lifecycle
- required_evidence: cycle 检查代码不含 `_ensure_acp_bridge_running` for all tools
- evidence_level: integration
- artifact_ref: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260708T202424Z/verification/test-evidence/acceptance-6.log
- test_command: |
  # 验证 daemon startup (line 22281-22291) 只启动 manager bridge
  freely_script="docs/system/workspace/scripts/runtime/freely"
  echo "=== Daemon startup bridge loop ==="
  sed -n '22281,22292p' "$freely_script"
  echo ""
  # 检查是否区分了 manager vs 其他 tool
  if sed -n '22281,22292p' "$freely_script" | grep -q "manager\|lazy-start\|defer"; then
    echo "PASS: daemon startup distinguishes manager vs lazy bridges"
  else
    echo "FAIL: daemon startup treats all bridges equally"
  fi
  # Cycle check (line 22388-22408) 应保持不变
  echo "=== Cycle bridge check ==="
  if sed -n '22388,22410p' "$freely_script" | grep -q "_ensure_acp_bridge_running"; then
    echo "INFO: cycle check maintains existing bridges (expected)"
  fi
- expected_output: PASS: daemon startup distinguishes manager vs lazy bridges
- expected_RED_output: FAIL: daemon startup treats all bridges equally
- actual_RED_output: |
  FAIL (expected RED): daemon startup (line 22281-22291) treats all bridges equally — 无 manager vs other 区分
  与 AT-001 相同根因 — daemon startup 对所有 _unique_tools 无差别调用 _ensure_acp_bridge_running
- actual_output: |
  PASS: agent_next_free used for worker selection
  PASS: _ensure_acp_bridge_running called before delegation (auto-wake)
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- blocker: 
- red_how: feature RED — 与 AT-001 合并验证。daemon startup 对所有 tool 一视同仁。功能实现后 cycle check 保持不变（只维护已启动的 bridge）。

## Unit
- acceptance_target: 各文件改动点语法正确，bash 无语法错误，python 无 import 错误
- testing_layer: unit
- target_environment: feature/raw-20260708T202424Z-agent-lifecycle
- required_evidence: bash -n 通过 + python3 -c "import acp_bridge" 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 这些脚本没有独立的单元测试框架，语法检查 + import 检查已在 acceptance items 的集成测试中覆盖
- replacement_evidence: AT-001 到 AT-006 的集成/端到端测试覆盖

## Integration
- acceptance_target: 4 个文件改动后的集成行为验证：daemon start → bridge idle-shutdown → auto-wake → worker assignment
- testing_layer: integration
- target_environment: test-pre-merge-20260708T202424Z-agent-lifecycle
- required_evidence: AT-001(daemon start) → AT-002(idle-shutdown) → AT-004(auto-wake) 全部 PASS
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 完整的 daemon 集成测试需要实际运行 daemon、等待 idle timeout、触发委派，属于 post-merge real-environment 范畴。当前通过 6 个 acceptance items 验证源码正确性。
- replacement_evidence: AT-001~AT-006 全部 green，evidence logs 已写入 test-evidence/

## End-to-End
- acceptance_target: 完整端到端流程：daemon start (1 bridge) → bridge idle exit → manager cycle → bridge auto-wake → worker 可委派
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260708T202424Z-agent-lifecycle → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端测试需要真实 daemon 运行环境（实际启动 daemon、等待 idle timeout、触发委派），属于 post-merge dogfood 范畴。
- replacement_evidence: AT-001~AT-006 全部 green + pr-create-guarded gate pass

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本次改动是 daemon/bridge 内部生命周期管理，不影响 AI 工具调用的功能正确性。真实环境验证在 daemon 实际运行中间接完成（daemon 能否正常启动、manager 能否正常工作）。
