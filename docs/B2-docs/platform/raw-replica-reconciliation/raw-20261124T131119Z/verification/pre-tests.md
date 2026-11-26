# Pre-Tests: stale linked 孤儿关闭封装入口
- issue_id: I-20261124T131119Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 封装命令可达，委托 close-local-id，rc 0/3/1 透传，失败回执可操作
- acceptance_target: 目标 1-3
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261124T131119Z-orphan-replica-close
- required_evidence: develop RED、工位 GREEN，逐断言与 SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261124T131119Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-close-orphans-command.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok, 11 failed — develop 无 close-orphans 入口
- actual_RED_output: "SUMMARY: 2 ok, 11 failed（develop 基线）"
- actual_output: "SUMMARY: 13 ok, 0 failed（stub adapter 全路径）"
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261124T131119Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: 对 develop 跑同一 AT（--source-dir develop），cmd_close_orphans 不存在必然命中。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T2
- case_design: 结构断言 + 隔离 fixture 中 stub adapter 的 0/3/1 退出码与回执断言
## Unit
- test_tasks:
  1. dispatcher 与 commands.md 登记。
  2. 无调用方 adapter import。
  3. stub adapter 0/3/1 透传与重试命令。
