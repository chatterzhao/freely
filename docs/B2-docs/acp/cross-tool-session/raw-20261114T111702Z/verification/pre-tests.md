# Pre-Tests: freely comment 根路径变量修复
- issue_id: I-20261114T111702Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: cmd_comment 的 ACP 通知段不再引用未定义的 PROJECT_ROOT，统一复用 SELF_ROOT，且能力保留、行数不增
- acceptance_target: raw-20261114T111702Z 期望 1-5 与边界
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261114T111702Z-comment-project-root-unbound
- required_evidence: develop 基线 RED、工位 GREEN，逐断言 ok/FAIL 与 SUMMARY 日志
- evidence_level: integration
- artifact_ref: docs/B2-docs/acp/cross-tool-session/raw-20261114T111702Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-comment-root-variable.py
- expected_output: SUMMARY: N ok, 0 failed（cmd_comment 内无 PROJECT_ROOT、通知段用 SELF_ROOT、ACP 与平台写调用仍在、语法通过、行数 <= .size-budget）
- expected_RED_output: SUMMARY: <N-M> ok, M failed — 基线 cmd_comment 命中 ${PROJECT_ROOT} 且通知段未用 ${SELF_ROOT}
- actual_RED_output: "SUMMARY: 8 ok, 2 failed — develop 基线 cmd_comment() 命中 2 处 ${PROJECT_ROOT} 且通知段无 ${SELF_ROOT}（证据 acceptance-1-red.log）"
- actual_output: "SUMMARY: 10 ok, 0 failed；cmd_comment 无 PROJECT_ROOT、通知段 4 处 SELF_ROOT、ACP 与平台写均保留、bash -n rc=0、行数 27166/27166（证据 acceptance-1.log）"
- evidence_file: docs/B2-docs/acp/cross-tool-session/raw-20261114T111702Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: fix 复现——对 develop 源码跑同一 AT（--source-dir <develop>），cmd_comment 内两处 ${PROJECT_ROOT} 必然被断言命中，证明 bug 存在；不做平台写。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: A1-A5
- case_design: 源码逐字断言 + bash -n 语法 + 行数预算，覆盖变量引用、能力保留、门禁约束三个维度

## Unit
- acceptance_target: AT 逐断言验证变量引用与源码结构
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: 每条 check 打印 ok/FAIL，SUMMARY 汇总
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 断言 `cmd_comment()` 函数体内不出现 `${PROJECT_ROOT}`。
  2. 断言通知段 `agent_working` 两处 import/调用使用 `${SELF_ROOT}`。
  3. 断言 `SELF_ROOT` 在文件头部全局定义。
  4. 断言 `run-acp-prompt.py` 调用与 adapter `comment` 写调用仍存在。
  5. 断言 `wc -l <= .size-budget` 且 `bash -n` 通过。

## Integration
- acceptance_target: 变量替换后 ACP 通知与平台写两条路径共存
- testing_layer: integration
- target_environment: test-pre-merge-20261114T111702Z-comment-project-root-unbound
- required_evidence: AT 集成断言 + bin/test-all --ci 全绿
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 跑 AT-001 确认所有断言 GREEN。
  2. 跑 `bash bin/test-all --ci` 确认全绿、AT 已接入 CORE/CI_CORE。

## End-to-End
- acceptance_target: 完整 guarded 流程不因本改动破损
- testing_layer: end-to-end
- target_environment: test-pre-merge → develop merge chain
- required_evidence: test-gate completed + dry-run merge gate rc=0 + 合并后重刷 test-gate
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. test 工位 merge dev 提交后 `freely test-gate run` 通过。
  2. develop 上 `freely pr-merge-guarded --dry-run` rc=0；合并后重跑 test-gate。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT 不对平台发写（避免测试污染）；平台评论写成功由 raw 中连续 3 次吃狗粮实测记录承接，合并后再用真实 `freely comment` 复验 rc=0 与 stderr 干净。
