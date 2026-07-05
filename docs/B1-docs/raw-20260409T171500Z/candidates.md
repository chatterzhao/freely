# Candidates: runtime-evidence-provenance-research-retirement-followthrough

## Context

- Source brainstorm: `./brainstorms.md`
- Status: `reviewed`
- Route: `ibm`

## Candidates

### C-20260409T171500Z-A: legacy issue

- title: `Runtime evidence provenance research retirement followthrough governance`
- candidate_format_version: `v2`
- research_only: `false`
- implementation_ready: `true`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_path: `docs/B2-docs/runtime/runtime-evidence-provenance-research-retirement-followthrough-governance/issues/runtime-evidence-provenance-research-retirement-followthrough-governance.md`
- summary: `Carry a narrow same-line owner for the develop-bound retirement of dropped candidate C-20260407T060300Z-A so the protected push gate sees concrete issue/pre-tests/review evidence and the obsolete research worktree can be retired without reviving the mixed-owner design packet.`
- why_now: `The cleanup merge already proved the research packet should be retired, but origin/develop correctly rejects a candidate-only develop diff. A narrow followthrough owner is now required to close the lifecycle lawfully.`
- acceptance_criteria:
  - `The original research packet remains dropped and historical; it is not reopened as an active cross-owner governance issue.`
  - `A narrow followthrough issue owns the develop-bound retirement diff, with issue, pre-tests, progress, and verification artifacts all present.`
  - `The obsolete research worktree is explicitly marked for retirement and no longer blocks fleet truth.`
- promotion_gate:
  - `Keep scope limited to lifecycle closeout and obsolete-worktree retirement.`
  - `Do not widen runtime continuity, verification contract, or canonical absorption governance boundaries.`
  - `Provide develop-bound verification evidence instead of relying on candidate-only notes.`
- open_questions:
  - `Should future dropped research packets always materialize a narrow followthrough owner before develop-bound retirement, or only when they produce a guarded merge diff?`
- acceptance_reviews:
  - reviewer: `author-review`
    date: `2026-04-09`
    verdict: `promote`
    note: `The remaining problem is not research content but same-line lifecycle closure and obsolete worktree retirement. That is narrow enough for immediate IBM materialization.`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}
