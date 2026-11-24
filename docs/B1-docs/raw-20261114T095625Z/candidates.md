---
candidate_id: C-20261114T095625Z-A
status: promoted
source_raw: raw-20261114T095625Z
created_at: 2026-11-24
milestone: M-20261114T095625Z-A
---

## C-20261114T095625Z-A: B0 关键词广搜与二元决策
- candidate_format_version: v2
- title: B0 增加关键词广搜 / 多文档交叉 / 继续-dropped 决策
- status: promoted
- design_verdict: 设计不完整
- anchor_refs:
  - `skills/freely-doc-B1_IBM-execution/SKILL.md:49-51` 只要求读锚点
  - `tests/test-b1-design-intent-audit.py` 钉旧 B0
  - raw body「必须靠关键词广搜看全局」
- decision_reason: 扩展 B0 方法论，补广搜/分层/矛盾/二元决策四层；无既有覆盖。
- next_action: B2 物化；改 SKILL.md B0 段 + 自检；新增 AT。
- revisit_trigger: 若关键词广搜被提升为硬门禁或自动脚本，重新评估边界。
- acceptance_criteria:
  - SKILL.md B0 含关键词族（≥3 组）、三类分层、矛盾清单、继续/dropped 二元决策字段
  - dropped 必须给出覆盖者证据，禁止以耗时/复杂度为由
  - brainstorms 模板 §0 含相应结构化表格
  - 完成自检加一项
  - AT 静态断言这些要求存在且"刻意不做硬门禁"
  - develop 基线 RED
- promotion_gate: 自指 P0 判继续；无硬门禁；不动 L0/verdict 契约。
- open_questions: []
- acceptance_reviews:
  - reviewer: self-b1-audit
  - mode: structured-check
  - summary: 关键词广搜自举完成；P0 显式判继续（含自指防护）；三类分层与矛盾清单有实证。
  - verdict: pass
- promoted_issue_id: I-20261114T095625Z-A
- promoted_issue_path: docs/B2-docs/ibm/b0-keyword-broad-search/raw-20261114T095625Z/issues/I-20261114T095625Z-A.md
- milestone: M-20261114T095625Z-A
- session_refs:
  - tool: codebuddy-agent
  - session_id: unavailable://current-session
  - jsonl_path: unavailable://current-session
  - role: worker
