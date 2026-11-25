# Pre-Tests: 元数据等价提交免重测
- issue_id: I-20261125T094413Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: attest-meta 沿袭非敏感 diff，敏感/硬排除路径拒绝，validate 三态
- acceptance_target: 目标 1-4
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261125T094413Z-evidence-equivalence-attest
- required_evidence: develop RED、工位 GREEN，逐断言与 SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/test-evidence-equivalence/raw-20261125T094413Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-evidence-equivalence.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 4 ok, 5 failed — develop 无 attest-meta/三态
- actual_RED_output: "SUMMARY: 4 ok, 5 failed（develop 基线）"
- actual_output: "SUMMARY: 9 ok, 0 failed（strict 断言）"
- evidence_file: docs/B2-docs/gate/test-evidence-equivalence/raw-20261125T094413Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: 对 develop 跑同一 AT（--source-dir develop），attest-meta 不存在必然命中。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T2
- case_design: 结构断言 + 隔离 git 仓库行为断言（基线/metadata/敏感/沿袭）
## Unit
- test_tasks:
  1. attest-meta 存在且计算 tested..HEAD diff。
  2. 硬排除路径无条件拒绝。
  3. 沿袭保留 EVIDENCE_SHA256（不伪造）。
  4. validate 输出 current/equivalent/stale。
