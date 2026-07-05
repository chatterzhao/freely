# 候选：historical-completed-queue-identity-followthrough

- id: `C-20260412-1230-A`
- candidate_format_version: `v2`
- title: Normalize historical completed-queue entries to canonical issue identities
- source_brainstorm: `docs/B1-docs/raw-20260412-1230/brainstorms.md`
- reopen_of_issue: `docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/issues/milestone-completed-queue-closeout-governance.md`
- reopen_reason: `a real guarded develop replay still warns because the completed watchdog owner is listed in docs/milestones.md by legacy candidate identity C-20260324-0405-A instead of canonical issue identity I-20260324-0405`
- problem: `The completed milestone queue still carries one historical legacy candidate identity, which keeps governance warnings alive even though the owner issue itself is already completed and canonical.`
- why_now:
  - `the warning is live on canonical develop and surfaced again during guarded merge replay`
  - `the underlying completed-queue policy is already frozen, so this should land as a narrow historical truth followthrough`
  - `leaving the legacy candidate identity in place keeps fleet closeout noisy and obscures real new warnings`
- acceptance_criteria:
  - `the affected completed queue item uses the canonical I-* identity instead of the legacy C-* identity`
  - `the queue entry points to the existing watchdog issue/progress evidence without reopening implementation scope`
  - `guarded develop replay no longer emits the historical legacy-identity warning`
  - `no other milestone queue semantics or watchdog runtime behavior change`
- promotion_gate:
  - `keep the change scoped to historical completed-queue identity normalization`
  - `do not reopen watchdog runtime thresholds, escalation behavior, or live-status surfaces`
  - `do not widen into generic milestone auto-repair or queue format redesign`
- open_questions:
  - `none; the canonical owner identity already exists and only needs to replace the stale completed-queue alias`
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The drift is historical queue truth only. A narrow followthrough owner is smaller and more accurate than reopening either watchdog runtime work or the broader completed-queue governance owner.`
    verdict: `ready_for_ibm`
- priority: `P1`
- status: `promoted`
- decision_reason:
  - `the merge gate correctly requires a candidate -> issue -> progress -> review chain even for narrow completed-family writebacks`
  - `a new followthrough owner makes the historical identity repair explicit without pretending the original completed queue governance or watchdog owner is active again`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/historical-completed-queue-identity-followthrough-governance/issues/historical-completed-queue-identity-followthrough-governance.md`
- promoted_issue_path_role: `primary-owner`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - `I-20260412-1230-A` owns the historical completed-queue identity repair and the minimal develop-bound writeback needed to clear the warning on canonical develop.`
- revisit_trigger:
  - `reopen only if additional completed queue entries are still carried by legacy candidate identities after this narrow followthrough lands`
