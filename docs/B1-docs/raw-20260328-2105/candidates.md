# Candidates - 20260328-2105--resume-evidence-strength-and-false-positive-resume-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260328-2105-A: legacy issue
- candidate_format_version: v2
- title: Define verified resume evidence governance for false-positive session recovery
- problem: Freely currently treats an observed `session_id` as sufficient `resume_target` evidence for `codex`, even when the same cycle has already proven `jsonl_path=unavailable`. This lets a non-resumable thread id enter persisted recovery state and turns a single failed fresh launch into repeated invalid `resume` attempts and restart-storm churn.
- why_now: This failure was reproduced on canonical `develop`, verified again through direct `codex exec resume <bad-session-id>` reproduction, and is deep enough that a narrow patch without a clarified contract would risk either regressing healthy resume or entrenching a local workaround instead of a reusable Freely recovery rule. Git history also indicates the gap predates the latest auth/watchdog field incidents, so the right response is a contract repair, not blame-shifting to the newest runtime changes.
- acceptance_criteria:
  - Freely defines `resume evidence` for explicit session-addressed tools in terms stronger than `resume_target != empty`
  - `observed session id + missing rollout/jsonl` is no longer eligible for next-cycle `resume`
  - the runtime degrades that scenario to `fresh_with_handoff` or an equivalent non-resume recovery path with an explicit reason
  - healthy explicit `resume` with real rollout/jsonl evidence continues to work
  - `auth_failure` / watchdog slot recovery semantics remain unchanged
  - focused regression coverage exists for the false-positive session-id-only case
- promotion_gate:
  - keep the repair inside continuity evidence / launch-kind selection semantics
  - do not weaken `explicit session-addressed resume` back toward `--last` or PTY-first interaction
  - prove the root cause with a deterministic reproduction and a failing regression before broadening the fix
  - make the final rule explicit about the boundary between `observed`, `persistable`, and `resumable` evidence
  - materialize the first issue as `codex`-scoped unless a same-round audit proves the same gap on other explicit session-addressed tools
  - review only after that whether the final abstraction should be Codex-specific or shared by all explicit session-addressed tools
- open_questions:
  - should rollout/jsonl existence alone be enough for `strong` evidence, or must the resolver also encode tool-specific resumability checks when available
  - should the persisted state explicitly record evidence strength and downgrade reason for operator/debug visibility
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The root bug is not that resume exists; it is that the runtime elevates weak observed session hints into strong recovery truth. The safe fix is to formalize evidence strength and let only verified evidence drive resume.`
    verdict: `ready_for_ibm`
  - reviewer: `codex`
    mode: `reproduction review`
    summary: `The bad session id was reproduced outside Freely with the same no-rollout failure text, which rules out status-surface confusion and justifies a contract-level fix rather than a cosmetic patch.`
    verdict: `ready_for_ibm`
- priority: P1
- status: promoted
- decision_reason: The failure is now concrete and reproducible, and the first owner issue has been materialized narrowly: preserve healthy resume, preserve auth/watchdog recovery, repair only the false-positive resume evidence path on the proven `codex` chain, and defer broader cross-tool generalization until it is separately audited.
- promoted_issue_path: `docs/B2-docs/config/codex-verified-resume-evidence-governance/issues/codex-verified-resume-evidence-governance.md`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- next_action: Complete IBM for the new codex-scoped owner issue, then enter dev-loop with a regression-first repair for false-positive session-id-only resume evidence.
- revisit_trigger: Reopen or widen this line if future field evidence shows other explicit session-addressed tools can also emit session ids without replayable rollout evidence, or if a proposed fix starts downgrading healthy resumable sessions into unnecessary fresh handoffs.
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
