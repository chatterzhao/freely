# Pre-Tests: task-lifecycle-scan platform_adapter import 断裂修复
- issue_id: I-20260807T114900Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 端到端 — scan 恢复平台可见性（platform_health 非 degraded 且 total > 0）
- acceptance_target: task-source-scan --json 不再降级，平台 open issues 重新可见
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260807T114900Z-scan-platform-adapter-import
- required_evidence: scan JSON summary.platform_health=ok 且 summary.total > 0
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/verification/test-evidence/acceptance-1.log
- test_command: ./bin/freely task-source-scan --project . --json
- expected_output: summary.platform_health=ok 且 summary.total > 0
- expected_RED_output: platform_health=degraded, reason=No module named 'platform_adapter', total=0
- actual_RED_output: platform_health=degraded, reason=No module named 'platform_adapter'（修复前真实 scan JSON）
- actual_output: platform_health=ok, total=110（test 工位真机 scan）
- evidence_file: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T4
- case_design: 在 test 工位真实执行 scan JSON，断言 platform_health 非 degraded 且 total>0。

### acceptance-2
- id: AT-002
- requirement: 单元 — importlib _get_pa() 加载器暴露所需平台符号
- acceptance_target: _get_pa(project) 加载 platform-adapter.py 并暴露 configured_platforms / list_open_issue_records / _handlers / _safe
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: test-pre-merge-20260807T114900Z-scan-platform-adapter-import
- required_evidence: 测试脚本 loader smoke test OK
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/verification/test-evidence/acceptance-2.log
- test_command: python3 docs/system/workspace/scripts/tests/test-scan-platform-adapter-import.py
- expected_output: OK: _get_pa() loads platform-adapter.py and exposes required symbols
- expected_RED_output: AttributeError: module 'tls' has no attribute '_get_pa'
- actual_RED_output: AttributeError: module 'tls' has no attribute '_get_pa'（修复前 loader 不存在）
- actual_output: OK: _get_pa() loads platform-adapter.py and exposes required symbols
- evidence_file: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2
- case_design: 真机 importlib 加载 platform-adapter.py 并断言四个符号存在。

### acceptance-3
- id: AT-003
- requirement: 单元 — 三处直接 from platform_adapter import 全部移除
- acceptance_target: task-lifecycle-scan.py 中不再残留直接导入
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: test-pre-merge-20260807T114900Z-scan-platform-adapter-import
- required_evidence: 测试脚本直接导入检查 OK
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/verification/test-evidence/acceptance-3.log
- test_command: python3 docs/system/workspace/scripts/tests/test-scan-platform-adapter-import.py
- expected_output: OK: no direct 'from platform_adapter import' remains
- expected_RED_output: 3 direct 'from platform_adapter import' statements remain
- actual_RED_output: 3 direct 'from platform_adapter import' statements remain（修复前 L451/502/548）
- actual_output: OK: no direct 'from platform_adapter import' remains
- evidence_file: docs/B2-docs/ibm/scan-platform-adapter/raw-20260807T114900Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2
- case_design: 真机执行测试脚本第三条断言，grep 计数必须为 0。

## Unit
- acceptance_target: _get_pa() loader 加载正确 + 直接导入清零
- testing_layer: unit
- target_environment: test-pre-merge-20260807T114900Z-scan-platform-adapter-import
- required_evidence: acceptance-2/3 OK
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-scan-platform-adapter-import.py，覆盖 loader 符号与直接导入清零两条断言。

## Integration
- acceptance_target: scan 全链路对平台 issue 恢复可见
- testing_layer: integration
- target_environment: test-pre-merge-20260807T114900Z-scan-platform-adapter-import
- required_evidence: acceptance-1 真机 scan OK 且非平台类别不回归
- blocker_taxonomy: execution_pending_or_failed
1. 运行 task-source-scan --json，断言 platform_health=ok 且 total>0。

## End-to-End
- acceptance_target: guarded merge chain 端到端
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260807T114900Z-scan-platform-adapter-import → develop merge chain
- required_evidence: pr-create-guarded / pr-merge-guarded 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 本分支自身经过真实 guarded PR 链路，单列 e2e 脚本不会比真实 gate 链路更真实。
- replacement_evidence: 本分支 PR 的 guarded merge receipts。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: test 工位真实执行 task-source-scan --json，读取 GitHub/Gitee 真实平台数据，platform_health=ok、total=110。
