# Pre-Tests: E2E测试与回归门禁
- issue_id: I-20260720T120329Z-C

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 回归门禁 — agent-id.env 在生产代码中零引用
- acceptance_target: pytest test_regression_agent_id_env_gate.py PASS
- testing_layer: unit
- target_environment: test-pre-merge-20260720T120329Z-agent-id-test-gate
- required_evidence: test output shows PASSED
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/verification/test-evidence/acceptance-1.log
- test_command: python3 -m pytest tests/test_regression_agent_id_env_gate.py -v
- expected_output: 1 passed
- expected_RED_output: FAILED (agent-id.env found in production code)
- actual_RED_output: FAILED — 2 violations found (scan.py detail msg + agent_working.py docstring)
- actual_output: 1 passed
- evidence_file: test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: ""
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""
- red_how: fix — 旧代码 agent-id.env 在生产脚本中多处读写，回归门禁应报 FAIL

### acceptance-2
- id: AT-002
- requirement: E2E 测试 — 真实 DB daemon 下三角色闭环
- acceptance_target: 4/4 E2E tests PASS (full cycle, atomic no-dup, persistence, upsert)
- testing_layer: integration
- target_environment: test-pre-merge-20260720T120329Z-agent-id-test-gate
- required_evidence: test output shows 4 passed
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/agent-identity-single-truth/raw-20260720T120329Z/verification/test-evidence/acceptance-2.log
- test_command: python3 -m pytest tests/test_e2e_agent_working_real_db.py -v
- expected_output: 4 passed
- expected_RED_output: FAILED (mock-only or no real DB tests)
- actual_RED_output: FAILED — 旧测试全mock，无真实DB daemon E2E验证
- actual_output: 4 passed
- evidence_file: test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- blocker: ""
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: ""
- red_how: fix — 旧代码 tests/ 目录无真实 DB daemon E2E 测试（缺陷 #10）

### acceptance-3
- id: CAT-010
- requirement: worker 分配只接受从目标工位解析出的时间戳型 raw key；解析失败必须拒绝，绝不能回退为 `develop`
- acceptance_target: sync 与 direct launch 路径都使用同一已验证 key；无 key 时不调用 allocate/release/register
- testing_layer: unit + static production-path regression
- target_environment: fix worktree 与对应 test-pre-merge 工位
- required_evidence: 新增 raw key 提取单测和 worker launch 静态回归测试 PASS
- test_command: `python3 -m pytest tests/test_agent_working_fail_closed_and_idempotent.py tests/test_worker_launch_fail_closed_review.py -q`
- expected_RED_output: 当前实现包含 `or 'develop'` 且 sync 路径未初始化 `_worker_raw_key`
- actual_RED_output: `2 failed, 32 passed`；缺失 raw key 回退和非法 worker identity 均被新增 RED 用例捕获
- actual_output: `55 passed in 0.49s`；同轮 `bash -n` 与 Python 编译检查通过
- red-green-status: green
- status: passed
- blocker: ""
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: `tests/test_agent_working_fail_closed_and_idempotent.py` + `tests/test_worker_launch_fail_closed_review.py`

### acceptance-4
- id: CAT-011
- requirement: `pr-review-guarded` 对 absorbed continuation 必须读取 B1 `absorbed_into` 并定位 canonical I-*，不得伪造当前 raw 的新 I 节点
- acceptance_target: `raw-20260720T171146Z` review 路由到 `I-20260720T120329Z-C`，且从 fix worktree 优先查找对应 B2 issue
- testing_layer: static production-path regression + guarded command
- target_environment: fix worktree 与对应 test-pre-merge 工位
- required_evidence: 静态回归 PASS，`pr-review-guarded` 进入 canonical review 阶段
- test_command: `python3 -m pytest tests/test_agent_working_fail_closed_and_idempotent.py -q`
- expected_RED_output: 当前脚本回退到不存在的 `I-20260720T171146Z-A`
- actual_RED_output: `1 failed, 25 passed`；静态回归确认脚本未读取 `absorbed_into`
- actual_output: `56 passed in 0.68s`；`bash -n bin/pr-review-guarded` 同轮通过
- red-green-status: green
- status: passed
- blocker: ""
- not_applicable_reason: ""
- not_applicable_explanation: ""
- replacement_evidence: `tests/test_agent_working_fail_closed_and_idempotent.py`

## Unit
- acceptance_target: 回归门禁 + E2E 测试全部通过
- testing_layer: unit
- target_environment: test-pre-merge-20260720T120329Z-agent-id-test-gate
- required_evidence: AT-001 + AT-002 通过
- blocker_taxonomy: execution_pending_or_failed
1. test_regression_agent_id_env_gate.py: agent-id.env regression gate
2. test_e2e_agent_working_real_db.py: full trirole cycle (4 sub-tests)

## Integration
- acceptance_target: E2E 测试覆盖三角色完整闭环
- testing_layer: integration
- target_environment: test-pre-merge-20260720T120329Z-agent-id-test-gate
- required_evidence: AT-002 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 集成级覆盖由 AT-002 E2E 测试提供（真实 DB daemon dispatch）
- replacement_evidence: AT-002 4/4 GREEN

## End-to-End
- acceptance_target: 回归门禁在 CI 中生效
- testing_layer: end-to-end
- target_environment: CI pipeline
- required_evidence: CI 中 agent-id.env 引用会导致 build fail
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: CI 集成需合并后在真实 CI 环境中验证。本地 pytest 已通过
- replacement_evidence: AT-001 + AT-002 本地 GREEN

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本地 5/5 测试通过（1 回归门禁 + 4 E2E）。CI 验证合并后自动生效
