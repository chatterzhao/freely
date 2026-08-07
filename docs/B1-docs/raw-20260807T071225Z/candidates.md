---
candidate_id: C-20260807T071225Z-A
status: promoted
source_raw: raw-20260807T071225Z
created_at: 2026-08-07
milestone: M-20260807T071225Z-A
---

# Candidates

## C-20260807T071225Z-A: scan parse_frontmatter 嵌套 YAML 解析修复

- candidate_format_version: v2
- title: 修复 scan parse_frontmatter 嵌套 platform_ids 解析
- status: promoted
- decision_reason: 简单行解析无法处理嵌套 YAML，strict raw 误报；yaml.safe_load 优先 + fallback 兼容双格式。
- next_action: B2 物化 + 测试（test-scan-frontmatter-nested.py）→ dev 修复。
- revisit_trigger: 无。
- acceptance_criteria:
  - strict raw frontmatter 的 platform_ids 解析为 dict
  - 字段顺序与 RAW_METADATA_FIELDS 一致
  - validate(fm) 通过（base_dir 项目根）
  - bullet/混合格式 I-* 仍可解析（fallback 不回归）
- promotion_gate: B2 物化 + 测试设计。
- open_questions: []
- acceptance_reviews:
  - reviewer: cli
  - mode: independent-readonly-review
  - summary: 根因明确（嵌套解析缺陷），方案兼容双格式
  - verdict: pass
- promoted_issue_id: I-20260807T071225Z-A
- milestone: M-20260807T071225Z-A
- session_refs: []
