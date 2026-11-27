# Pre-Tests: 退役门禁删除失效的 freshness check
- issue_id: I-20261126T120834Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: equivalent 放行、stale/not_tested 拦截、自造 HEAD 判据已删
- acceptance_target: 目标 1-3
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261126T120834Z-retirement-gate-equivalence
- required_evidence: develop RED、工位 GREEN，逐断言与 SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/worktree-lifecycle/wt-close/raw-20261126T120834Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-retirement-gate-equivalence.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 8 ok, 1 failed — develop 保留自造 HEAD 判据
- actual_RED_output: "SUMMARY: 8 ok, 1 failed（develop 基线 7873ec0）"
- actual_output: "SUMMARY: 9 ok, 0 failed（三态 fixture 全绿）"
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-close/raw-20261126T120834Z/verification/test-evidence/acceptance-1.log
- red-green-status: red
- status: pending
- red_how: 对 develop（--source-dir）跑同一 AT，自造判据仍在，equivalent 场景必失败。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T2
- case_design: 结构断言 + 隔离 fixture（真实 gate 脚本 + 真实 test-evidence.py + stub pretests-gate）三态行为
## Unit
- test_tasks:
  1. gate 源码无 `pretests_stale` 自造 HEAD 判据且调用 validate --json。
  2. equivalent/stale/not_tested 三态行为断言。
