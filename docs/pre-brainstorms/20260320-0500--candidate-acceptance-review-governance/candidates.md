# Candidates

- capability: candidate acceptance boundary, independent review, and IBM acceptance deepening
- owner_loop: doc-loop pre-brainstorm and IBM governance
- primary_surface: `docs/pre-brainstorms/**/candidates.md`, `doc-pre-brainstorm-execution`, `doc-ibm-execution`, `governance-check`
- canonical_artifact: `docs/system/workspace/skills/doc-pre-brainstorm-execution/references/candidate-recording.md`
- promoted_issue_path: pending://candidate-acceptance-review-materialization
- milestone: pending://workspace-routing-foundation
- session_refs: []
- key_questions:
  - future candidate 是否应统一进入 `candidate_format_version: v2`
  - `acceptance_criteria` / `promotion_gate` / `open_questions` / `acceptance_reviews` 是否应成为 v2 最小字段
  - promotion 前是否应至少要求一次独立 acceptance review
  - IBM 是否应显式承担 issue-level acceptance deepening
- validation:
  - `candidate-recording` 与 `doc-pre-brainstorm-execution` 已要求 v2 fields
  - `governance-check` 已能强制 future v2 candidate 包含 acceptance boundary
  - `governance-check` 已能强制 promoted v2 candidate 至少有一次 acceptance review
  - `doc-ibm-execution` 与其 references 已表达 acceptance deepening
