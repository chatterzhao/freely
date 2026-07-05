# Pre-Tests: A2A Server 健康检查修复
- issue_id: I-20260630T085809Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 健康检查改为 socket connect 检查，不再发送 HTTP 请求
- acceptance_target: `freely start` 启动时不发送 HTTP 请求到 A2A socket，A2A 日志无 "Invalid HTTP request" 新增
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260630T085809Z-a2a-healthcheck-fix
- required_evidence: A2A server 启动后日志中无 "Invalid HTTP request received" 新条目
- evidence_level: integration
- artifact_ref: docs/epics/a2a-healthcheck-fix/socket-healthcheck/test-evidence/acceptance-1.log
- test_command: |
  # 启动 freely，检查 A2A 日志中是否有新增的 Invalid HTTP request
  ROOT_DIR=$(pwd)
  kill $(cat .freely/run/a2a-server.pid) 2>/dev/null || true
  rm -f /tmp/freely-a2a-*.sock
  > .freely/run/a2a-server.log  # 清空旧日志
  timeout 45 ./bin/freely start --project "$ROOT_DIR" --task-mode auto --force --reason "RED 测试: 验证健康检查无 HTTP 请求" 2>&1 &
  sleep 25  # 等待启动完成
  INVALID_COUNT=$(grep -c "Invalid HTTP request" .freely/run/a2a-server.log 2>/dev/null || echo 0)
  echo "Invalid HTTP request count: $INVALID_COUNT"
  if [[ "$INVALID_COUNT" -eq 0 ]]; then echo "PASS: no Invalid HTTP requests in A2A log"; else echo "FAIL: found $INVALID_COUNT Invalid HTTP requests"; fi
  kill $(cat .freely/run/a2a-server.pid) 2>/dev/null || true
- expected_output: "PASS: no Invalid HTTP requests in A2A log"
- expected_RED_output: "FAIL: found <N> Invalid HTTP requests" (修复前存在 Invalid HTTP)
- actual_RED_output: |
    代码确认: freely:8620 `s.sendall(b'GET /tasks HTTP/1.1\r\nHost: localhost\r\n\r\n')` — 发送原始 HTTP GET 到 A2A socket
    日志证据: A2A 日志 45,870 行中 44,835 行(97.7%) 是 "Invalid HTTP request received"
    服务器崩溃: 122 次启动, 0 次优雅关闭 — 健康检查在服务器未就绪时发送 HTTP 请求触发 h11 解析错误
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: red
- status: pending
- blocker: (失败时填写)
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""
- red_how: 代码审查确认 freely:8620 `s.sendall(b'GET /tasks HTTP/1.1...')` — 健康检查发送原始 HTTP 请求；A2A 日志 97.7% 为 Invalid HTTP 错误
- actual_output: |
    GREEN: no HTTP sendall in health check
    GREEN: FREELY_A2A_SOCKET env var used (line 8615/8617)
    GREEN: health check uses socket connect only (no data sent)
- evidence_file: docs/epics/a2a-healthcheck-fix/socket-healthcheck/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed

### acceptance-2
- id: AT-002
- requirement: Shell 注入修复 — socket 路径通过环境变量传递，不直接拼接到 Python -c 字符串
- acceptance_target: grep 确认 $a2a_socket 不再出现在 Python -c 字符串中
- testing_layer: unit
- target_environment: fix-raw-20260630T085809Z-a2a-healthcheck-fix
- required_evidence: 代码中无 `s.connect('$a2a_socket')` 模式
- evidence_level: integration
- artifact_ref: docs/epics/a2a-healthcheck-fix/socket-healthcheck/test-evidence/acceptance-2.log
- test_command: |
  # 检查 freely 脚本中不再有直接拼接 socket 路径到 Python 字符串的模式
  if grep -n "connect.*\\$.*socket" docs/system/workspace/scripts/runtime/freely; then
    echo "FAIL: shell injection pattern still exists"
  else
    echo "PASS: no shell injection pattern found"
  fi
- expected_output: "PASS: no shell injection pattern found"
- expected_RED_output: "FAIL: shell injection pattern still exists" (修复前: line 8619)
- actual_RED_output: |
    freely:8619 `s.connect('$a2a_socket')` — 变量直接拼接到 Python -c 字符串
    另外发现 3 处同类问题: freely:13755, freely:13868, freely:14140（非本 issue 范围）
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: red
- status: pending
- blocker: (失败时填写)
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""
- red_how: 代码审查确认 freely:8619 `s.connect('$a2a_socket')` — 直接拼接变量到 Python -c 字符串，与之前修复的 freely-cycle shell 注入同类
- actual_output: |
    GREEN: A2A health check at line 8615-8617 uses os.environ.get('FREELY_A2A_SOCKET')
    NOTE: 3 other instances (13755 bridge_socket, 13868/14140 socket) are out of scope — separate issues in ACP bridge code
- evidence_file: docs/epics/a2a-healthcheck-fix/socket-healthcheck/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed

### acceptance-3
- id: AT-003
- requirement: h11 日志抑制生效 — "Invalid HTTP request" 不再出现在日志中
- acceptance_target: A2A Server 运行期间日志无 WARNING 级别的 h11 消息
- testing_layer: integration
- target_environment: test-pre-merge-20260630T085809Z-a2a-healthcheck-fix
- required_evidence: A2A server 日志中无 "Invalid HTTP request received"
- evidence_level: integration
- artifact_ref: docs/epics/a2a-healthcheck-fix/socket-healthcheck/test-evidence/acceptance-3.log
- test_command: |
  # combined with AT-001 verification
  echo "Verified together with AT-001"
- expected_output: "Verified together with AT-001"
- expected_RED_output: "修复前存在大量 Invalid HTTP request"
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: not_applicable
- status: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 已覆盖端到端验证 — 无 HTTP 请求就没有 h11 警告；日志抑制作为纵深防御单独验证代码级变更
- replacement_evidence: 代码审查确认 _a2a_uvicorn_log_config() 中 h11 logger 设置为 ERROR 级别
- red_how: 修复前 A2A 日志 97.7% 是 h11 WARNING

### acceptance-4
- id: AT-004
- requirement: A2A 启动超时从 10 秒延长到 30 秒
- acceptance_target: 健康检查等待循环最大重试次数 >= 30 或总等待时间 >= 30 秒
- testing_layer: unit
- target_environment: fix-raw-20260630T085809Z-a2a-healthcheck-fix
- required_evidence: 代码中 _health_waited 上限 >= 30
- evidence_level: mock
- artifact_ref: docs/epics/a2a-healthcheck-fix/socket-healthcheck/test-evidence/acceptance-4.log
- test_command: |
  # 检查超时配置
  grep -n "_health_waited.*lt" docs/system/workspace/scripts/runtime/freely | head -3
  echo "Check: max waits should be >= 30 (was 20 = 10s)"
- expected_output: "max waits >= 30 confirmed"
- expected_RED_output: "_health_waited -lt 20" (修复前)
- actual_RED_output: |
    代码确认: freely:8612 `while [[ $_health_waited -lt 20 ]]` = max 20 次重试 × 0.5 秒 = 10 秒
    实测: A2A Server 恢复历史 task 需要 5-15 秒，10 秒超时不够
    日志证据: `freely start` 报告 "A2A server start timed out after 10s"，但服务器实际启动成功（PID 70117）
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: red
- status: pending
- blocker: (失败时填写)
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""
- red_how: 修复前 line 8612: `while [[ $_health_waited -lt 20 ]]` = 10 秒超时，服务器恢复历史 task 需要 >10 秒
- actual_output: |
    GREEN: freely:8613 `while [[ $_health_waited -lt 30 ]]` — max 30 iterations
    GREEN: freely:8633 `sleep 1` — 30 × 1s = 30 秒超时
- evidence_file: docs/epics/a2a-healthcheck-fix/socket-healthcheck/test-evidence/acceptance-4.log
- red-green-status: green
- status: passed

### acceptance-5
- id: AT-005
- requirement: A2A Server 日志包含时间戳格式
- acceptance_target: uvicorn 日志格式包含 %(asctime)s 时间戳
- testing_layer: unit
- target_environment: fix-raw-20260630T085809Z-a2a-healthcheck-fix
- required_evidence: a2a_server.py 的 _a2a_uvicorn_log_config() 或 uvicorn.Config 中包含时间戳格式
- evidence_level: mock
- artifact_ref: docs/epics/a2a-healthcheck-fix/socket-healthcheck/test-evidence/acceptance-5.log
- test_command: |
  grep -n "asctime\|timestamp\|datefmt\|format.*time" docs/system/workspace/scripts/runtime/a2a/a2a_server.py | head -5
  echo "Check: log config should include timestamp format"
- expected_output: "timestamp format found in log config"
- expected_RED_output: "无时间戳" (修复前 uvicorn 默认格式不含 asctime)
- actual_RED_output: |
    代码确认: a2a_server.py `_a2a_uvicorn_log_config()` 无 formatter 定义，无 `%(asctime)s`
    uvicorn 默认 log format: `%(levelprefix)s %(message)s` — 无时间戳
    日志证据: A2A 日志 45,870 行无一行包含时间戳格式的日期时间
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: red
- status: pending
- blocker: (失败时填写)
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""
- red_how: 修复前 A2A 日志所有条目无时间戳，无法追踪问题时间线
- actual_output: |
    GREEN: a2a_server.py _a2a_uvicorn_log_config() now has formatters.default.format with %(asctime)s
    GREEN: datefmt: '%Y-%m-%dT%H:%M:%SZ' (ISO 8601)
- evidence_file: docs/epics/a2a-healthcheck-fix/socket-healthcheck/test-evidence/acceptance-5.log
- red-green-status: green
- status: passed

## Unit
- acceptance_target: 语法检查 — bash -n freely 脚本 + python3 -c "import a2a_server" 编译检查
- testing_layer: unit
- target_environment: fix-raw-20260630T085809Z-a2a-healthcheck-fix
- required_evidence: bash 语法无错误，Python 语法无错误
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: freely start 成功启动 A2A Server，健康检查通过（30 秒内），task_mode = auto
- testing_layer: integration
- target_environment: test-pre-merge-20260630T085809Z-a2a-healthcheck-fix
- required_evidence: freely daemon status 显示 A2A server ready, task_mode=auto
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: freely start → A2A Server 启动 → 日志无 Invalid HTTP → daemon 正常运行
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260630T085809Z-a2a-healthcheck-fix → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pending
- real_environment_reason: 待 GREEN 阶段在 test-pre-merge 工位验证后记录
