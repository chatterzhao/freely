# Candidates

## C-20260508T111130Z-A: reference-transaction delete fix

- candidate_format_version: v2
- title: reference-transaction hook skip aborted txns to allow branch deletion
- status: promoted
- decision_reason: aborted 事务误触发 creation guard，加一行跳过即可修复
- promoted_issue_path: docs/issues/I-20260508T111130Z-A/issue.md
- milestone: M-20260508T111130Z-A
- next_action: B2_IBM → dev-loop → merge
- revisit_trigger: N/A
- acceptance_criteria:
  - git branch -d test-pre-merge-* 不再被误拦截
- promotion_gate: 
  - reference-transaction.sh 修复正确
  - gate check 通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - verdict: pass
