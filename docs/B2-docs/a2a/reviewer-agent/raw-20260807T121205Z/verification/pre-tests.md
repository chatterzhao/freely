# Pre-Tests: reviewer assign raw_key 字段传播
- issue_id: I-20260807T121205Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: needs-review 更新在 raw_key 可解析时发出、在缺失时 fail-closed 拒绝，非 review 转换不变
- acceptance_target: raw issue 的 Expected fix 1 + 影响面；candidate acceptance_criteria 全项
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260807T121205Z-reviewer-assign-raw-key
- required_evidence: develop 基线 RED、fix 工位 GREEN；逐条断言输出与 SUMMARY，日志落 evidence_file
- evidence_level: integration
- artifact_ref: docs/B2-docs/a2a/reviewer-agent/raw-20260807T121205Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-reviewer-assign-raw-key.py --source-dir <SRC_ROOT>
- expected_output: SUMMARY: 6 ok, 0 failed
- expected_RED_output: develop 基线出现 failed——合法 raw_key 未进入 PATCH、缺失 raw_key 未被拒绝、显式 --raw-key 未生效
- actual_RED_output: "SUMMARY: 2 ok, 4 failed（develop 基线：raw_key 未进入 SSE payload、缺失 raw_key 未被拒绝、显式 --raw-key 未生效、AT 未接入 bin/test-all）"
- actual_output: "SUMMARY: 6 ok, 0 failed（fix 工位与 test 工位：合法发出 / 缺失拒绝 / 显式优先 / 非 review 不变 / watchdog 断言保留 / 双列表注册）"
- evidence_file: docs/B2-docs/a2a/reviewer-agent/raw-20260807T121205Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: 新写 AT 直接驱动真实 a2a_task.py::_main() 的 a2a-exit 分支；对 develop 根跑同一 AT 复现漏字段 bug
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T3
- case_design: 六条断言——任务记录兜底发出、缺失拒绝、显式参数优先、非 review 不变、watchdog FAIL-CLOSED 保留、bin/test-all 双列表注册

## Unit
- acceptance_target: a2a-exit 字段构造函数的原始输出（raw_key 优先级与 fail-closed 分支）
- testing_layer: unit
- target_environment: fix/raw-20260807T121205Z-reviewer-assign-raw-key
- required_evidence: 辅助函数返回值与抛错行为逐条断言
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 任务记录含 raw_key 时字段含该值。
  2. 参数与记录皆空时抛错。
  3. 显式参数覆盖记录值。

## Integration
- acceptance_target: a2a-exit CLI → A2AClient.update() → PATCH 字段（即 SSE 事件字段）的数据流
- testing_layer: integration
- target_environment: test-pre-merge-20260807T121205Z-reviewer-assign-raw-key
- required_evidence: 通过 fake client 捕获 update 调用，确认字段随事件发出
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. needs-review 更新捕获字段含 raw_key。
  2. 缺失场景没有 PATCH 调用（无 SSE 事件）。

## End-to-End
- acceptance_target: develop 基线 RED → fix 工位 GREEN；reviewer 路由不再因缺 raw_key FAIL-CLOSED
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260807T121205Z-reviewer-assign-raw-key → develop merge chain
- required_evidence: test-gate GREEN + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. AT 在 develop 根失败、在 fix 工位通过。
  2. test-gate run --command 'bash bin/test-all --ci' 全绿。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 真实 a2a_task.py CLI 入口与 SSE 字段契约被 AT 覆盖；watchdog 进程链路不在本地可复现范围，保留其 FAIL-CLOSED 断言作为最终防线
