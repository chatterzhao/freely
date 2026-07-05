# Candidates

### C-20260406-1105-A
- candidate_format_version: v2
- title: Milestone completed-queue closeout
- status: promoted
- milestone: `M-20260306-workspace-routing-foundation`
- source_brainstorm: `docs/B1-docs/raw-20260406-1105/brainstorms.md`
- problem: `docs/milestones.md` still sequences several completed owners under `committed_issues`, and baseline `./bin/governance-check` does not detect that queue drift once the original develop-bound merge is over.
- why_now:
  - the active milestone is Freely's primary scan surface, so stale committed placement distorts sequencing truth
  - this must be machine-audited, not left as manual closeout hygiene
- acceptance_criteria:
  - completed owners in the active milestone move out of `committed_issues` and exist only under `completed_issues`
  - `./bin/governance-check` fails when a milestone `issue_path` points to an issue whose `phase_state` requires a different queue
  - a focused regression proves the failure and the repaired pass path
- promotion_gate:
  - materialize a narrow owner, fix the milestone queue truth, add the baseline audit, and rerun governance-check plus the focused regression
- open_questions:
  - whether future alternate queue artifacts should reuse the same queue/phase audit contract
- acceptance_reviews:
  - reviewer: `milestone-truth-review`
    verdict: `supports`
    note: `Completed owners left in committed_issues pollute the active scan surface and should be closed canonically.`
  - reviewer: `baseline-audit-review`
    verdict: `supports`
    note: `A repo-wide governance-check audit is the right backstop because merge-gate only sees the current develop-bound diff.`
- decision_reason:
  - canonical milestone truth is already inconsistent with completed owner truth
  - the missing contract is a repo-wide audit, not another workflow redesign
- promoted_issue_id: `I-20260406-1105-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/issues/milestone-completed-queue-closeout-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action: Materialize the owner, repair the active milestone queue drift, and bind the missing baseline audit before another closeout silently reintroduces the same mismatch.
- revisit_trigger: Re-open only if canonical governance-check still misses milestone queue/phase drift after this audit lands.
