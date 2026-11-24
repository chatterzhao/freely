# Pre-Tests: B0 关键词广搜与二元决策
- issue_id: I-20261114T095625Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: B0 skill 含广搜/分层/矛盾/二元决策/留痕，且不做硬门禁
- acceptance_target: B1 skill B0 段与 brainstorms 模板
- testing_layer: integration
- target_environment: test-pre-merge-20261114T095625Z-b0-keyword-broad-search
- required_evidence: AT 在 develop 基线 RED、工位 GREEN
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b0-keyword-broad-search/raw-20261114T095625Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-b0-keyword-broad-search.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: <N-M> ok, M failed（基线 skill 无广搜/分层/二元决策字段）
- actual_RED_output: "SUMMARY: 2 ok, 7 failed — 基线 B0 无广搜/分层/矛盾/二元决策字段（收紧断言后）"
- actual_output: "SUMMARY: 9 ok, 0 failed；skill B0 + 模板 + 自检五层齐备，无硬门禁"
- evidence_file: docs/B2-docs/ibm/b0-keyword-broad-search/raw-20261114T095625Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: feature 复现——develop 基线 B0 只有"读锚点+四问"，无关键词广搜等新字段，AT 静态断言必然失败。

## Unit
- acceptance_target: skill/模板文本断言
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT 静态断言
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 断言 skill B0 含关键词族（≥3 组）、三类分层、矛盾清单、继续/dropped 二元决策、dropped 覆盖者证据。
  2. 断言 brainstorms 模板 §0 含结构化表格字段、完成自检含新项。
  3. 断言"刻意不做硬门禁"仍保留（防补字段就过）。

## Integration
- acceptance_target: 与既有 B0 AT 与 test-all 兼容
- testing_layer: integration
- target_environment: test-pre-merge-20261114T095625Z-b0-keyword-broad-search
- required_evidence: 新 AT + 既有 test-b1-design-intent-audit 全绿
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 新 AT 接入 CORE/CI_CORE，跑 test-all --ci 全绿。
  2. 既有无硬门禁断言不被破坏。

## End-to-End
- acceptance_target: 方法论自举（本 raw 的 B1 P0 判继续）
- testing_layer: end-to-end
- target_environment: feature worktree
- required_evidence: 本 raw brainstorms.md §0 含关键词广搜记录且结论为"继续"
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. AT 读取本 raw B1 文档，断言存在关键词广搜记录表、三类分层、矛盾清单与"判定：继续"。
  2. 验证 dropped 决策要求覆盖者证据（避免自指误判）。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本轮改的是 skill/模板文档，fix/test 工位静态断言与自举文档核对即为真实环境验证；无运行时行为变化。
