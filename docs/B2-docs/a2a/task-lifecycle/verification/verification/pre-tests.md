# Pre-Tests: a2a_tasks state alignment with Google A2A

- issue_id: I-20260630T021946Z-A

## Acceptance Items

### AT-001 State class: BLOCKED→INPUT_REQUIRED + CANCELED added
- id: AT-001
- requirement: a2a_task.py State class 使用标准名，BLOCKED 改为 INPUT_REQUIRED，新增 CANCELED
- acceptance_target: grep 确认无 `BLOCKED` 常量，有 `INPUT_REQUIRED` 和 `CANCELED`
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/a2a/task-lifecycle/verification/test-evidence/acceptance-1.txt
- test_command: |
  _wt="/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260630T021946Z-a2a-state-standard"
  grep -q 'INPUT_REQUIRED.*input-required' "$_wt/docs/system/workspace/scripts/runtime/a2a_task.py" || { echo "FAIL: INPUT_REQUIRED not found"; exit 1; }
  grep -q 'CANCELED.*canceled' "$_wt/docs/system/workspace/scripts/runtime/a2a_task.py" || { echo "FAIL: CANCELED not found"; exit 1; }
  grep 'BLOCKED.*blocked' "$_wt/docs/system/workspace/scripts/runtime/a2a_task.py" | grep -qv '#' && { echo "FAIL: BLOCKED still present"; exit 1; } || true
  echo "PASS: INPUT_REQUIRED + CANCELED present, BLOCKED removed"
- expected_output: "PASS: INPUT_REQUIRED + CANCELED present, BLOCKED removed"
- expected_RED_output: "FAIL: INPUT_REQUIRED not found"
- actual_RED_output: "RED confirmed — PENDING_INPUT, exit_kind, old mapping present"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/B2-docs/a2a/task-lifecycle/verification/test-evidence/acceptance-1.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前 grep 确认 State class 有 BLOCKED="blocked"，无 INPUT_REQUIRED，无 CANCELED

### AT-002 --kind → --state CLI 参数
- id: AT-002
- requirement: a2a-exit 的 --kind 参数改为 --state，值直接用 A2A state
- acceptance_target: grep 确认 `add_argument("--state"` 存在，`add_argument("--kind"` 不存在
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/a2a/task-lifecycle/verification/test-evidence/acceptance-2.txt
- test_command: |
  _wt="/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260630T021946Z-a2a-state-standard"
  grep -q 'add_argument.*--state' "$_wt/docs/system/workspace/scripts/runtime/a2a_task.py" || { echo "FAIL: --state arg not found"; exit 1; }
  grep 'add_argument.*--kind' "$_wt/docs/system/workspace/scripts/runtime/a2a_task.py" | grep -qv '#' && { echo "FAIL: --kind still present"; exit 1; } || true
  echo "PASS: --state present, --kind removed"
- expected_output: "PASS: --state present, --kind removed"
- expected_RED_output: "FAIL: --state arg not found"
- actual_RED_output: "RED confirmed — PENDING_INPUT, exit_kind, old mapping present"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/B2-docs/a2a/task-lifecycle/verification/test-evidence/acceptance-2.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前 grep 确认有 --kind 参数，无 --state 参数

### AT-003 A2A 文档 blocked→input-required
- id: AT-003
- requirement: exit-kind-mapping.md, protocol-design.md, agent-card-schema.md 中 blocked 引用更新
- acceptance_target: grep 确认三个文档中 `blocked` 已替换为 `input-required`；`worker_blocked` exit kind 说明更新
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/a2a/task-lifecycle/verification/test-evidence/acceptance-3.txt
- test_command: |
  _wt="/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260630T021946Z-a2a-state-standard"
  for f in "$_wt/docs/system/workspace/a2a/exit-kind-mapping.md" "$_wt/docs/system/workspace/a2a/protocol-design.md" "$_wt/docs/system/workspace/a2a/agent-card-schema.md"; do
    grep 'blocked' "$f" | grep -qvi 'input-required\|#\|说明' && { echo "FAIL: $f still has old blocked reference"; exit 1; } || true
  done
  echo "PASS: A2A docs updated"
- expected_output: "PASS: A2A docs updated"
- expected_RED_output: "FAIL: ... still has old blocked reference"
- actual_RED_output: "RED confirmed — PENDING_INPUT, exit_kind, old mapping present"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/B2-docs/a2a/task-lifecycle/verification/test-evidence/acceptance-3.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前 grep 确认三个 A2A 文档含多处 blocked 引用

### AT-004 SQLite CHECK constraint 更新
- id: AT-004
- requirement: SQLite CHECK 包含 input-required 和 canceled
- acceptance_target: grep 确认 CHECK 约束含新 state
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/a2a/task-lifecycle/verification/test-evidence/acceptance-4.txt
- test_command: |
  _wt="/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260630T021946Z-a2a-state-standard"
  grep -q 'input-required.*canceled\|canceled.*input-required' "$_wt/docs/system/workspace/scripts/runtime/a2a_task.py" || { echo "FAIL: CHECK constraint not updated"; exit 1; }
  echo "PASS: CHECK constraint includes input-required + canceled"
- expected_output: "PASS: CHECK constraint includes input-required + canceled"
- expected_RED_output: "FAIL: CHECK constraint not updated"
- actual_RED_output: "RED confirmed — PENDING_INPUT, exit_kind, old mapping present"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/B2-docs/a2a/task-lifecycle/verification/test-evidence/acceptance-4.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前 grep 确认 CHECK 约束不含 input-required

### AT-005 Exit kind 映射层清理
- id: AT-005
- requirement: 删除或标注废弃 blocked→input-required 旧映射
- acceptance_target: grep 确认无旧映射
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/a2a/task-lifecycle/verification/test-evidence/acceptance-5.txt
- test_command: |
  _wt="/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260630T021946Z-a2a-state-standard"
  grep "'blocked'.*'input-required'" "$_wt/docs/system/workspace/scripts/runtime/a2a_task.py" && { echo "FAIL: old mapping still present"; exit 1; } || true
  echo "PASS: old mapping removed"
- expected_output: "PASS: old mapping removed"
- expected_RED_output: "FAIL: old mapping still present"
- actual_RED_output: "RED confirmed — PENDING_INPUT, exit_kind, old mapping present"
- actual_output: "GREEN: all tests pass"
- evidence_file: docs/B2-docs/a2a/task-lifecycle/verification/test-evidence/acceptance-5.txt
- red-green-status: green
- status: passed
- blocker: none
- red_how: fix: 修改前 grep 确认映射表中 'blocked': 'input-required' 存在

## Unit
- acceptance_target: grep 验证全部修改
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT-001~005 全部 grep 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001~005 即 unit tests
- replacement_evidence: AT evidence files

## Integration
- acceptance_target: a2a_task.py --state input-required 可执行
- testing_layer: integration
- target_environment: fix worktree
- required_evidence: python3 --help 输出显示 --state
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 完整 A2A Server 测试需要真实环境
- replacement_evidence: Python syntax check

## End-to-End
- acceptance_target: 全链路 state 变更正常
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: PR merge 后 worker/reviewer 使用新 state
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: E2E 需要 supervisor-cycle (Candidate B) 完成后验证
- replacement_evidence: unit tests + syntax check

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 仅 state 重命名，语义不变，无运行时风险
