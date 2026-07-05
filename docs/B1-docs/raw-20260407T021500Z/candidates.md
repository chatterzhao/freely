# Candidates

### C-20260407T021500Z-A: legacy issue
- candidate_format_version: v2
- title: Runtime self-host continuity gap and status truth followthrough
- status: promoted
- milestone: `M-20260306-workspace-routing-foundation`
- source_brainstorm: `docs/B1-docs/raw-20260407-0215/brainstorms.md`
- problem: On canonical `develop`, Freely self-host supervision can generate a fresh manager prompt that explicitly requires a new continuity file, yet the latest generated continuity remains older and status surfaces previously did not make that gap explicit. `live-status` was also brittle enough to exit blank when PID hint validation failed under `set -e`, which hides the self-host stall instead of describing it.
- why_now:
  - the user explicitly wants this class of failure to become Freely capability rather than manual repo cleanup
  - canonical `develop` currently shows `current_prompt_has_delegated_continuation: 1` together with a missing prompt-required continuity path
  - the active CLI contract lane is out of scope for runtime supervision, so the regression needs a correct owner before more self-host work accumulates around it
- acceptance_criteria:
  - `live-status` does not blank out when PID hint validation fails; it degrades to a readable status surface
  - status logic no longer depends on `rg` being present in PATH just to choose the project workspace root
  - `live-status` and `fleet-status` surface a machine-readable continuity-gap signal when the latest prompt requires a manager continuity path that has not been materialized
  - focused regressions cover the PID-hint failure path, the `rg`-missing fallback, and the continuity-gap status surface
- promotion_gate:
  - freeze this as a new self-host followthrough under the blocked-intake / continuity family, not as a continuation of the CLI lane
  - materialize an IBM issue that can absorb the current code and test changes in the dedicated feature worktree
  - record the real canonical evidence from `live-status` / `fleet-status` showing the missing continuity path
- open_questions:
  - whether the same owner should also make runtime auto-materialize blocked truth for prompt-required continuity gaps while the AI process is still active
  - whether missing-worktree references in the active milestone progress should be repaired in the same owner or split into a sibling governance followthrough
- acceptance_reviews:
  - reviewer: `runtime-observability-review`
    verdict: `supports`
    note: `The system must at least expose prompt-required continuity gaps and survive degraded PID truth before broader self-healing can be trusted.`
- decision_reason:
  - this is the narrowest reusable capability gap exposed by current self-hosting
  - it sits directly on the completion boundary of `runtime-blocked-intake-and-continuity-truth` and its closeout already instructs future recurrences to reopen as a new owner
- promoted_issue_id: `I-20260407T021500Z-A`
- promoted_issue_path: `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
- depends_on:
  - `docs/B2-docs/runtime/runtime-blocked-intake-and-continuity-truth-governance/issues/runtime-blocked-intake-and-continuity-truth-governance.md`
  - `docs/B2-docs/ibm/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action: Candidate mirror only. `I-20260407T021500Z-A` is now the canonical owner for the self-host continuity-gap status truth followthrough; keep the worker lane on bounded verification evidence and continuity only, and let manager-side `completion_verification / cleanup_governance` decide closeout unless canonical replay reopens an owner-scoped status gap.
- revisit_trigger: Revisit only if canonical `develop` proves the continuity-gap signal disappears without needing a new owner, or if the family is instead reabsorbed by an already-open runtime supervision owner.
