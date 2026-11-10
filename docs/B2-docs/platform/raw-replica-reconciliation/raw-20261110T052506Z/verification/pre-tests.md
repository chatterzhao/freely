# Pre-Tests: guarded PR plan 可诊断 + git 传输超时守卫
- issue_id: I-20261110T052506Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: plan 保留逐平台真实 error；recovery 按环境/分支分类；三处 git 调用有单一 timeout；超时显式诊断；all-or-nothing 与状态判定不变
- acceptance_target: 平台抖动时运维一次就能看到真实原因与正确恢复动作，而不是被误导去同步分支
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 `pr_lifecycle.py` / `platform-adapter.py` 模块加载 + mock `subprocess.run` 注入 `RuntimeError` 与 `TimeoutExpired` + develop HEAD 完整基线快照
- required_evidence: 18 项全 GREEN；基线 RED `6 ok / 12 failed`；64 组状态矩阵 0 差异
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-guarded-pr-plan-diagnostics.py
- test_command: python3 docs/system/workspace/scripts/tests/test-guarded-pr-plan-diagnostics.py
- expected_output: SUMMARY: 18 ok, 0 failed
- expected_RED_output: SUMMARY: 6 ok, 12 failed（C1/C2/B2/B3/B8/B12 对照组 PASS）
- actual_RED_output: develop `169c14d18` 完整基线快照注入最终版 AT-001 → `6 ok, 12 failed`（AT-001-RED.log）
- actual_output: 工位同一断言 → `18 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261110T052506Z/verification/test-evidence/AT-001-RED.log,docs/B2-docs/platform/raw-replica-reconciliation/raw-20261110T052506Z/verification/test-evidence/AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组核对单一 timeout 常量/单一 helper、error 透传、recovery 单一真源与两类文案；对照组验证 `classify_branch` 五状态与 `SAFE/BLOCKED` 集合、all-or-nothing 聚合、健康平台不伪造 error、既有 pr-update 回归全绿。行为组用 mock 注入 `RuntimeError("ssh: connect ... timed out")` 驱动 `plan_platform_updates` 与 `guarded_pr_update`，核对返回体含真实原因且零副作用；再注入 `TimeoutExpired` 验证超时文案带 platform；最后录制三处 git 调用的 kwargs 确认都带 timeout。
- red_how: fix RED — `git archive develop` 出完整快照并补齐 `.freely/tool-boundary-bootstrap.md`，把最终版 AT-001 拷入快照 tests 目录，以 `--source-dir` 运行。

## End-to-End
- acceptance_target: guarded_pr_update 失败返回体携带真实原因且不产生任何平台写
- testing_layer: end-to-end
- target_environment: 真实模块 + mock handler
- required_evidence: AT-001（B7/B8）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-guarded-pr-plan-diagnostics.py

## Unit
- acceptance_target: plan 状态判定与 recovery 分类
- testing_layer: unit
- target_environment: fix/raw-20261110T052506Z-guarded-pr-plan-diagnostics
- required_evidence: AT-001（C1/C2 + B1–B6）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-guarded-pr-plan-diagnostics.py

## Integration
- acceptance_target: 既有 PR 生命周期与平台链路不退化
- testing_layer: integration
- target_environment: 工位 + 未修改 develop 主仓全环境
- required_evidence: AT-001 + 64 组矩阵 + 8 回归
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-pr-update.py
2. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 故障注入全部在 mock 层完成，不访问平台、不建真实 PR；真机健康路径由本轮自身 `pr-create-guarded` 验证。
- real_environment_reason: 本缺陷由 R23 收口时的**真实** GitHub git 通道 502/超时触发，重试同一封装命令即成功，证明 fail-closed 判定正确、缺的是可诊断性；`py_compile`、`check-epics-map`、相关回归基线对比均通过。
