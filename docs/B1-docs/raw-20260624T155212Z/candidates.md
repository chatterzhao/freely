---
candidate_id: C-20260624T155212Z-A
status: promoted
source_raw: raw-20260624T155212Z12Z
created_at: 2026-06-24
milestone: M-20260624T155212Z-A
---

## C-20260624T155212Z-A: legacy issue

- candidate_format_version: v2
- title: pretests-retirement-gate fallback for missing workcell-state.env
- status: promoted
- decision_reason: Option C (fallback scan of worktree pre-tests.md) is the minimal change that preserves backward compatibility and adds validation for the manual-execution path
- next_action: code committed in fix/raw-20260624T155212Z12Z-pretests-retirement-gate-fallback; ready for B2_IBM governance and PR
- revisit_trigger: N/A (fix is already implemented and committed)
- acceptance_criteria:
  - pretests-retirement-gate no longer exits immediately when workcell-state.env is missing
  - Fallback scans worktree docs/B2-docs/ for pre-tests.md files and validates via pretests-gate
  - When Worker metadata exists, original behavior is unchanged
  - manually-executed worktrees can be closed without --force
- promotion_gate: code change committed, tested against actual worktree
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-sonnet-4
  - mode: subagent
  - summary: Fallback approach is backward compatible and correctly validates pre-tests for manual worktrees
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260624T155212Z-A/issue.md
- milestone: M-20260624T155212Z-A
- session_refs: []
