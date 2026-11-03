---
candidate_id: C-20261103T124003Z-A
status: promoted
source_raw: raw-20261103T124003Z
created_at: 2026-11-03
milestone: M-20261103T124003Z-A
---

# Candidates

## C-20261103T124003Z-A: GitHub open 列表 GraphQL 504 → REST 回退

- candidate_format_version: v2
- status: promoted
- decision_reason: 504 是 GraphQL 侧瞬时/持续故障，REST 正常；在 handler 层重试+回退既修复测试误判，也保护 scan。
- next_action: 写 RED 单测（mock GraphQL 504 + REST 两页），实现回退，GREEN 后 test-pre-merge。
- revisit_trigger: 若 REST 也 504，需要上抛 transport 错误而不是空列表（本次已保留失败时返回 {}，后续可再收紧）。
- acceptance_criteria:
  - GraphQL 504 时 list_open_issue_records 返回 REST 数据（过滤 PR）。
  - list_open_issues 与 records 一致。
  - 返回结构不变；单测 RED→GREEN；parity 测试连续通过。
- promotion_gate: 单测 GREEN + test-pre-merge + governance gate
- open_questions: 失败时仍返回 {} 会把 transport error 与“真的没有 open issue”混淆；建议后续 feedback 增加显式 transport 错误。
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 复现 gh GraphQL 504 与 REST 正常，确认 handler 空返回是误判根因
  - verdict: pass
- promoted_issue_id: I-20261103T124003Z-A
- promoted_issue_path: docs/B2-docs/platform/github-rest-fallback/raw-20261103T124003Z/issues/I-20261103T124003Z-A.md
- milestone: M-20261103T124003Z-A
- session_refs: []
