# 候选：governance-merge-gate-milestone-status-followthrough

- id: `C-20260404T011900Z-A`
- candidate_format_version: `v2`
- title: Governance merge gate milestone status followthrough
- source_brainstorm: `docs/B1-docs/raw-20260404T011900Z/brainstorms.md`
- reopen_of_issue: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/issues/protected-branch-merge-receipt-hardening.md`
- reopen_reason: `a real develop replay exposed that governance-merge-gate misread nested queue item status lines in docs/milestones.md as the parent milestone status, falsely blocking an unrelated active candidate lane`
- problem: `governance-merge-gate` currently treats nested queue item `- status:` fields inside `docs/milestones.md` as if they were the milestone's own top-level status, so active milestones can be misclassified as `needs_research` and wrongly block develop-bound replay.
- why_now:
  - the runtime bootstrap lane is already implementation-complete and only blocked by this parser bug
  - the false block happens on canonical replay, so leaving it unresolved keeps protected-branch merge policy untrustworthy
  - the correct fix is a tiny parser boundary plus one regression, which is smaller than reopening a broader merge-governance owner
- acceptance_criteria:
  - the reopen is recorded as a narrow followthrough of the completed protected-branch merge receipt hardening owner
  - `parse_milestones()` only records milestone status from top-level milestone fields, not nested queue item fields
  - `test-governance-merge-gate` proves an active milestone is not downgraded by nested candidate item status metadata
  - no milestone scheduling semantics or candidate placement policy are widened in the process
- promotion_gate:
  - keep scope limited to milestone-status parsing in `governance-merge-gate` and its focused regression
  - do not widen this followthrough into runtime `/bin/ps` fallback work or general milestone redesign
  - carry same-line owner issue, progress, and review evidence so develop replay stays lawful
- open_questions:
  - none; the bug is reproduced and the intended parser boundary is already clear
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The replay failure is caused by merge-gate parsing nested queue item status as milestone truth. A narrow parser-bound followthrough is the smallest compliant repair.`
    verdict: `ready_for_ibm`
- priority: `P1`
- status: `promoted`
- decision_reason:
  - this is a residual parser bug in a completed merge-governance family, not a reason to mutate the prior completed owner
  - the develop merge gate correctly insists on a new same-line owner for this replay-bound fix, even though the implementation delta is small
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/gate/governance-merge-gate-milestone-status-followthrough-governance/raw-20260404-0119issues/governance-merge-gate-milestone-status-followthrough-governance.md`
- promoted_issue_path_role: `primary-owner`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - `I-20260404T011900Z-A` owns the parser boundary repair, focused regression, and minimal lifecycle writeback required to unblock canonical replay.
- revisit_trigger:
  - reopen only if active-milestone validation still misreads nested milestone queue metadata after this parser-specific followthrough lands
