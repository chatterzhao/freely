# Pre-Tests: batch 范围过滤修复与 daemon 只限定范围
- issue_id: I-20261114T031043Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 工位目录名含 raw key 时其它 raw 零变更；输出 scope；daemon 在 lane 传 key、受保护分支跳过；基线红
- acceptance_target: `--raw-key` 真正生效，且 daemon 不再无参全量同步
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 临时工位（目录名含 raw key）+ 抽取真实 cmd_batch；daemon 段静态断言
- required_evidence: AT-001 GREEN 10/0；基线 2/8
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-batch-scope-filter.py
- test_command: python3 docs/system/workspace/scripts/tests/test-batch-scope-filter.py
- expected_output: SUMMARY: 10 ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok, 8 failed
- actual_RED_output: develop 763248747 上 B2 红（两个 raw 都被 CLOSE）、B3 无 scope、S1–S6 全红（AT-001-RED.log）
- actual_output: SUMMARY: 10 ok, 0 failed；B1 本 raw 被处理、B2 其它 raw 零调用、B3 scope 输出、S3–S6 daemon 已限定（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/platform/issue-sync-modules/raw-20261114T031043Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ''
- task_refs: T1,T2,T3
- case_design: 临时目录命名为 fix-raw-<key>-<slug>（复现工位前缀含 key），放两个 raw 的文档，抽取真实 cmd_batch 并 stub 关闭钩子，断言只处理本 raw；daemon 段用静态断言钉住传参与跳过。
- red_how: fix RED — git archive develop 导出基线树，用 --source-dir 运行同一 AT。

## Unit
- acceptance_target: 过滤语义
- testing_layer: unit
- target_environment: fix/raw-20261114T031043Z-batch-scope-filter
- required_evidence: AT-001 B1/B2/B3
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-batch-scope-filter.py

## Integration
- acceptance_target: 既有同步与 CI 不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End
- acceptance_target: 下一次真实 sync 只影响本 lane
- testing_layer: end-to-end
- target_environment: 下一次 lane 内 issue-sync
- required_evidence: 输出含 scope=<本 raw>，其它 raw 零文档变更
- blocker_taxonomy: execution_pending_or_failed
1. 下一次 lane 内 `issue-sync batch <key>`

## Real-Environment
- real_environment_status: pass
- real_environment_reason: R33.18 与 R34.x 两次真机：scoped batch 处理 288 个跨 raw 文档、daemon 一次改写 100+；R34.x 的 child 在 merge 后 4 分钟才被手工 batch 关闭。
