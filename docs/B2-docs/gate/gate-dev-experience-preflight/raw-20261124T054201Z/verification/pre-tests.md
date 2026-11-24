# Pre-Tests: test-all 失败诊断
- issue_id: I-20261124T054201Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 失败测试输出可见（含断言），成功路径 SUMMARY 格式不变
- acceptance_target: test-all 失败诊断行为
- testing_layer: integration
- target_environment: test-pre-merge-20261124T054201Z-test-all-failure-diagnostics
- required_evidence: AT 在 develop 基线 RED、工位 GREEN
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261124T054201Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-test-all-diagnostics.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: <N-M> ok, M failed（基线吞输出、无日志落盘逻辑）
- actual_RED_output: "SUMMARY: 2 ok, 4 failed — 基线吞输出、无日志目录、无失败诊断"
- actual_output: "SUMMARY: 6 ok, 0 failed；E2E 注入必失败测试后其断言文本 DIAG_PROBE_MARKER_ASSERTION_FAILED 出现在诊断输出中"
- evidence_file: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261124T054201Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: fix 复现——develop 基线 test-all 把失败测试输出丢到 /dev/null，AT 静态+行为断言必然失败。

## Unit
- acceptance_target: 源码不再吞输出 + 日志落盘逻辑
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT 静态断言
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 断言 bin/test-all 执行循环不再含 `>/dev/null 2>&1`。
  2. 断言有独立日志目录与失败时打印输出的实现。

## Integration
- acceptance_target: 失败测试断言可见 + 成功 SUMMARY 不变
- testing_layer: integration
- target_environment: test-pre-merge-20261124T054201Z-test-all-failure-diagnostics
- required_evidence: AT 行为断言 + `bash bin/test-all --ci` 全绿
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 构造必然失败的临时测试，跑 test-all 确认输出含其断言文本。
  2. 跑 `bash bin/test-all --ci` 确认 SUMMARY 格式不变且全绿。

## End-to-End
- acceptance_target: CI 日志可诊断
- testing_layer: end-to-end
- target_environment: test-pre-merge → develop merge chain
- required_evidence: 失败诊断输出 + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 合并后 PR 触发 CI，若失败则日志含断言细节（由 AT 行为断言等价覆盖，CI 实测为 after-merge followthrough）。
  2. 验证 SUMMARY 行仍被 test-gate 正常解析。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本轮改动是 test-all 自身输出行为，fix/test 工位真机执行即为真实环境验证；不改变任何运行时产品行为。
