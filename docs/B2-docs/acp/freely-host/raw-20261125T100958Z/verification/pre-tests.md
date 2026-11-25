# Pre-Tests: feedback edit 与 wt-create 解耦
- issue_id: I-20261125T100958Z-A

## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 缺本地文档时 feedback edit 按 raw key 从平台发现 ids 并改双平台单，不创建本地文件
- acceptance_target: 目标 1-3 与非目标边界
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261125T100958Z-feedback-edit-platform-discovery
- required_evidence: develop 基线 RED、工位 GREEN，逐断言 ok/FAIL 与 SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/acp/freely-host/raw-20261125T100958Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-feedback-edit-platform-discovery.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: <N-M> ok, M failed — 基线缺本地文件时直接 return 1
- actual_RED_output: "SUMMARY: 5 ok, 3 failed（develop 基线缺平台发现分支）"
- actual_output: "SUMMARY: 8 ok, 0 failed；函数级单测 5/5（evidence acceptance-1.log）"
- evidence_file: docs/B2-docs/acp/freely-host/raw-20261125T100958Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: 对 develop 源码跑同一 AT，缺平台发现分支必然命中。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T2
- case_design: 源码结构断言 + 行为断言（mock search/update 输入输出）

## Unit
- test_tasks:
  1. edit 分支不再无条件 `[[ -f "$_issue_file" ]] || return 1`。
  2. 存在 platform-adapter search 调用。
  3. 缺本地文件时用发现的 ids 组 platform_ids。
  4. 缺本地文件时不写本地 issue.md。
  5. 空 title/body 不覆盖（adapter handler 语义）。

## Integration
- test_tasks:
  1. mock search 返回双平台 ids → update-issue 被调用。
  2. 0 匹配 → 非零 + 可操作报错。
