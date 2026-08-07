# Pre-Tests: task-lifecycle-scan platform_adapter import 断裂修复
- issue_id: I-20260807T114900Z-A

## Acceptance Items

### AT-001
- id: AT-001
- requirement: 端到端 — scan 恢复平台可见性（platform_health 非 degraded 且 total > 0）
- acceptance_target: `freely task-source-scan --json` 不再降级，87 个 open platform issues 重新可见
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260807T114900Z-scan-platform-adapter-import
- required_evidence: scan JSON summary.platform_health != degraded 且 summary.total > 0
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-scan-platform-adapter-import.py
- expected_output: OK: platform_health=<非 degraded>，total=<大于0>
- expected_RED_output: FAIL: platform_health degraded: No module named 'platform_adapter'（或 total==0）
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/verification/test-evidence/acceptance-1.log
- red-green-status: pending
- status: pending
- blocker: ""
- red_how: "修复前直接跑 test 脚本：_get_pa 不存在（AttributeError）或 scan 报 platform_health=degraded，bug 可复现"

### AT-002
- id: AT-002
- requirement: 单元 — importlib `_get_pa()` 加载器暴露所需平台符号
- acceptance_target: `_get_pa(project)` 加载 `platform-adapter.py` 并暴露 configured_platforms / list_open_issue_records / _handlers / _safe
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 测试脚本 loader smoke test OK
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/verification/test-evidence/acceptance-2.log
- test_command: python3 docs/system/workspace/scripts/tests/test-scan-platform-adapter-import.py
- expected_output: OK: _get_pa() loads platform-adapter.py and exposes required symbols
- expected_RED_output: FAIL: 模块缺失符号 / _get_pa 不存在
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/verification/test-evidence/acceptance-2.log
- red-green-status: pending
- status: pending
- blocker: ""
- red_how: "修复前 _get_pa() helper 不存在，加载脚本报 AttributeError"

### AT-003
- id: AT-003
- requirement: 单元 — 三处直接 `from platform_adapter import` 全部移除
- acceptance_target: task-lifecycle-scan.py 中不再残留直接导入（grep 计数为 0）
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: grep 计数 = 0
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/verification/test-evidence/acceptance-3.log
- test_command: python3 docs/system/workspace/scripts/tests/test-scan-platform-adapter-import.py
- expected_output: OK: no direct 'from platform_adapter import' remains
- expected_RED_output: FAIL: 3 direct 'from platform_adapter import' statements remain
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/verification/test-evidence/acceptance-3.log
- red-green-status: pending
- status: pending
- blocker: ""
- red_how: "修复前 grep 统计 3 处直接导入"

## Unit
- acceptance_target: `_get_pa()` loader 加载正确 + 直接导入清零
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 测试脚本单元部分 OK
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: scan 全链路对平台 issue 恢复可见（platform_health 健康、total>0）
- testing_layer: integration
- target_environment: test-pre-merge-20260807T114900Z-scan-platform-adapter-import
- required_evidence: E2E 测试 OK 且非平台类别不回归
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: `freely task-source-scan --project <project> --json` 端到端验证
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260807T114900Z-scan-platform-adapter-import → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pending
- real_environment_reason: 修复后对真实主仓跑 scan JSON，platform_health 恢复健康、total>0，与发布环境一致
