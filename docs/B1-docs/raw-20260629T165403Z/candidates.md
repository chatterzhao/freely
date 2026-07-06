---
candidate_id: C-20260629T165403Z-A
status: promoted
source_raw: raw-20260629T165403Z03Z
created_at: 2026-06-29
milestone: M-20260629T165403Z-A
---

## C-20260629T165403Z-A: legacy issue

- candidate_format_version: v2
- title: wt-close args unbound + test-pre-merge -D
- status: promoted
- decision_reason: 两个 one-liner bugfix，无替代方案
- next_action: merge to develop
- revisit_trigger: N/A
- acceptance_criteria:
  - --raw-key 正常收口不报 unbound variable
  - test-pre-merge 正常关闭路径分支删除成功
- promotion_gate: 测试通过 + merge
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: in-session
  - verdict: pass
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260307-1201I-20260629T165403Z-A/issue.md
- milestone: M-20260629T165403Z-A
- session_refs: []
