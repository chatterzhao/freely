# Candidates

## C-20260618T100000Z-A: legacy issue

- candidate_format_version: v2
- title: wt-create chat-inbox ID normalization — pass bare ID to chat-inbox.py
- status: absorbed
- decision_reason: Mechanical bug fix — 4 call sites pass ISO-format `$ts` (with T/Z) to chat-inbox.py but DB stores bare numeric IDs. Fix is `--id "$ts_bare"` where `ts_bare=$(echo "$ts" | tr -d 'TZ')`.
- next_action: B2_IBM → create I-* issue → PR
- revisit_trigger: N/A (absorbed — fix already committed as 1f6a60340)
- acceptance_criteria:
  - Chat-inbox worktree creation works without ID mismatch errors
  - All 4 call sites use `$ts_bare` instead of `$ts`
  - No regression in `--source platform` or `--source local` paths
- promotion_gate: Fix committed, verified in test-pre-merge, merged to develop
- open_questions: []
- acceptance_reviews: []
- promoted_issue_path: docs/issues/I-20260618T100000Z-A/issue.md
- milestone: M-20260618T100000Z-A
- session_refs: []
