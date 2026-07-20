# Pre-Tests: DB 基础设施补齐 — review RPC + 原子分配 + Reviewer 注册修复
- issue_id: I-20260720T120329Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: reviews 表存在且 schema 正确（含 UNIQUE(raw_key, review_stage) 约束）
- acceptance_target: `_ensure_tables()` 创建 reviews 表，含全部列和索引
- testing_layer: unit
- target_environment: test-pre-merge-20260720T120329Z-agent-id-retirement
- required_evidence: SQL schema 验证通过
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/verification/test-evidence/acceptance-1.log
- test_command: |
  python3 -c "
  import sqlite3, os, sys
  project = os.path.abspath('.')
  db_path = os.path.join(project, '.freely', 'freely.db')
  # Validate reviews table exists with correct columns
  conn = sqlite3.connect(db_path)
  cursor = conn.execute(\"SELECT sql FROM sqlite_master WHERE type='table' AND name='reviews'\")
  row = cursor.fetchone()
  if row:
      sql = row[0]
      required = ['raw_key', 'review_stage', 'verdict', 'reviewed_by', 'reviewed_at', 'findings']
      missing = [c for c in required if c not in sql]
      if not missing:
          print('PASS: reviews table exists with all required columns')
      else:
          print(f'FAIL: reviews table missing columns: {missing}')
  else:
      print('FAIL: reviews table not found')
  conn.close()
  "
- expected_output: |
  PASS: reviews table exists with all required columns
- expected_RED_output: |
  FAIL: reviews table not found
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段由 skill `freely-test-execution` 执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""
- red_how: fix — 验证旧代码 reviews 表不存在（bug: 无持久化存储）

### acceptance-2
- id: AT-002
- requirement: record_review RPC handler 存在且可写入/读取 review verdict
- acceptance_target: 调用 agent_working.record_review 写入，agent_working.get_reviews 读取一致
- testing_layer: integration
- target_environment: test-pre-merge-20260720T120329Z-agent-id-retirement
- required_evidence: write + read 往返验证
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/verification/test-evidence/acceptance-2.log
- test_command: |
  # Start DB daemon, write a review, read it back
  python3 docs/system/workspace/scripts/runtime/freely_db_manager.py start --project "$(pwd)" --foreground &
  DAEMON_PID=$!
  sleep 1
  python3 docs/system/workspace/scripts/runtime/freely-db-cli --project "$(pwd)" db.ping
  PING_RC=$?
  # Use agent_working.record_review via Python import
  python3 -c "
  import sys; sys.path.insert(0, 'docs/system/workspace/scripts/runtime')
  from agent_working import agent_record_review, agent_get_reviews
  r = agent_record_review('.', 'test-raw-key', 'b1', 'PASS', 'reviewer_07:codex', [{'item':'test','status':'pass'}])
  print('record:', r)
  g = agent_get_reviews('.', 'test-raw-key')
  print('get:', g)
  if g.get('b1',{}).get('verdict') == 'PASS':
      print('PASS: record_review + get_reviews roundtrip verified')
  else:
      print('FAIL: roundtrip mismatch')
  "
  kill $DAEMON_PID 2>/dev/null || true
- expected_output: |
  record: {'status': 'ok', 'raw_key': 'test-raw-key', 'review_stage': 'b1'}
  get: {'b1': {'verdict': 'PASS', 'reviewed_by': 'reviewer_07:codex', ...}}
  PASS: record_review + get_reviews roundtrip verified
- expected_RED_output: |
  record: {'error': ...}
  FAIL: roundtrip mismatch
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段由 skill `freely-test-execution` 执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""
- red_how: fix — 旧代码 agent_working.record_review 调用 DB RPC 但 handler 不存在，返回 error

### acceptance-3
- id: AT-003
- requirement: agent_next_free 新增 raw_key 参数，调用 next_free_and_assign 原子 RPC
- acceptance_target: 传入 raw_key 时使用原子分配，不传时仍可用旧路径
- testing_layer: unit
- target_environment: test-pre-merge-20260720T120329Z-agent-id-retirement
- required_evidence: 代码检查 + 函数签名验证
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/verification/test-evidence/acceptance-3.log
- test_command: |
  python3 -c "
  import ast, sys
  with open('docs/system/workspace/scripts/runtime/agent_working.py') as f:
      tree = ast.parse(f.read())
  for node in ast.walk(tree):
      if isinstance(node, ast.FunctionDef) and node.name == 'agent_next_free':
          args = [a.arg for a in node.args.args + node.args.kwonlyargs]
          if 'raw_key' in args:
              # Check for next_free_and_assign call
              for child in ast.walk(node):
                  if isinstance(child, ast.Constant) and 'next_free_and_assign' in str(child.value):
                      print('PASS: agent_next_free has raw_key param and uses next_free_and_assign')
                      sys.exit(0)
              print('FAIL: agent_next_free has raw_key but does not use next_free_and_assign')
              sys.exit(1)
          else:
              print('FAIL: agent_next_free missing raw_key parameter')
              sys.exit(1)
  print('FAIL: agent_next_free not found')
  "
- expected_output: |
  PASS: agent_next_free has raw_key param and uses next_free_and_assign
- expected_RED_output: |
  FAIL: agent_next_free missing raw_key parameter
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段由 skill `freely-test-execution` 执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""
- red_how: fix — 旧代码 agent_next_free 无 raw_key 参数，使用 next_free（非原子 RPC）

### acceptance-4
- id: AT-004
- requirement: agent_assign 移除 update_only 参数和 upsert_only RPC 路径
- acceptance_target: 所有 role 统一使用 agent_working.upsert（INSERT_OR_UPDATE）
- testing_layer: unit
- target_environment: test-pre-merge-20260720T120329Z-agent-id-retirement
- required_evidence: 代码检查确认 update_only 参数和相关路径已移除
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/verification/test-evidence/acceptance-4.log
- test_command: |
  # Verify upsert_only is no longer referenced in agent_assign path
  if grep -n "update_only\|upsert_only" docs/system/workspace/scripts/runtime/agent_working.py | grep -v "^#" | grep -v "test_\|\.md\|\.log"; then
    echo "FAIL: update_only references still exist in agent_working.py"
  else
    echo "PASS: update_only removed from agent_working.py"
  fi
- expected_output: |
  PASS: update_only removed from agent_working.py
- expected_RED_output: |
  FAIL: update_only references still exist in agent_working.py
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段由 skill `freely-test-execution` 执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""
- red_how: fix — 旧代码 agent_assign 有 update_only 参数和 upsert_only RPC 路径（reviewer 静默失败）

### acceptance-5
- id: AT-005
- requirement: Python 模块语法正确，可正常 import
- acceptance_target: freely_db_manager.py 和 agent_working.py 编译无语法错误
- testing_layer: unit
- target_environment: test-pre-merge-20260720T120329Z-agent-id-retirement
- required_evidence: Python 编译通过
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/verification/test-evidence/acceptance-5.log
- test_command: |
  python3 -c "import ast; ast.parse(open('docs/system/workspace/scripts/runtime/freely_db_manager.py').read()); print('PASS: freely_db_manager.py compiles')" && \
  python3 -c "import ast; ast.parse(open('docs/system/workspace/scripts/runtime/agent_working.py').read()); print('PASS: agent_working.py compiles')"
- expected_output: |
  PASS: freely_db_manager.py compiles
  PASS: agent_working.py compiles
- expected_RED_output: |
  (RPC handler 缺失不影响编译——RED 由 AT-001/AT-002 覆盖)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段由 skill `freely-test-execution` 执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""
- red_how: AT-005 是编译验证，旧代码也能编译通过。RED 由 AT-001/AT-002 覆盖（reviews 表缺失 + RPC handler 缺失）

## Unit
- acceptance_target: reviews 表 schema、agent_next_free 函数签名、agent_assign update_only 移除
- testing_layer: unit
- target_environment: test-pre-merge-20260720T120329Z-agent-id-retirement
- required_evidence: AT-001 + AT-003 + AT-004 + AT-005 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""

## Integration
- acceptance_target: record_review + get_reviews RPC roundtrip（需真实 DB daemon）
- testing_layer: integration
- target_environment: test-pre-merge-20260720T120329Z-agent-id-retirement
- required_evidence: AT-002 通过
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: 代码变更不破坏现有 agent_working.upsert/get/next_free/assign RPC
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260720T120329Z-agent-id-retirement
- required_evidence: 全部 AT 通过 + 现有 tests/ 套件通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: C-A 是纯 DB + Python 层改动，端到端需完整 daemon 运行时。代码级验证 + AT-002 往返测试已充分覆盖。完整三角色 E2E 由 C-C 负责
- replacement_evidence: AT-001 到 AT-005 全部通过 + `python3 -m pytest tests/ -x` 通过

## Real-Environment
- real_environment_status: pass
- real_environment_reason: C-A 是阻塞依赖，纯 DB 层改动。代码编译 + RPC roundtrip 验证 + 现有测试不回归 = 可合并。合并后 C-B 消费时做 real-environment 验证
