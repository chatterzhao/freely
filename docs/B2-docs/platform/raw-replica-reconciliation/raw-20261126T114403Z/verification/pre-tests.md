# Pre-Tests: close-orphans 批量模式复用平台读取
- issue_id: I-20261126T114403Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 一次平台读取 + 终态筛选 + rc 0/3/1 透传 + 可操作 retry
- acceptance_target: 目标 1-3
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261126T114403Z-close-orphans-batch
- required_evidence: develop RED、工位 GREEN，逐断言与 SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261126T114403Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-close-orphans-batch.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok, 16 failed — develop 无批量入口/子命令
- actual_RED_output: "SUMMARY: 2 ok, 16 failed（develop 基线 7873ec0）"
- actual_output: "SUMMARY: 18 ok, 0 failed（stub adapter 全路径）；单 id 回归 13 ok, 0 failed"
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261126T114403Z/verification/test-evidence/acceptance-1.log
- red-green-status: red
- status: pending
- red_how: 对 develop（--source-dir）跑同一 AT，批量入口/子命令不存在必然命中失败断言。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T3
- case_design: 结构断言 + 隔离 fixture stub adapter（记录平台读取次数）+ 终态筛选 + rc 透传 + retry 命令
## Unit
- test_tasks:
  1. dispatcher 与 commands.md 登记 `--all-completed`。
  2. adapter 子命令存在且命令层无 adapter import。
  3. stub 平台读取计数 = 1；非终态 id 不关闭；0/3/1 透传与 retry 命令。
