# Candidates - 20260331-1830--kiro-cli-monthly-request-limit-runtime-loop-governance

## Context
- Source brainstorm: `./brainstorms.md`
- Status: active

## Candidates

### C-20260331-1830-A
- candidate_format_version: v2
- title: Classify Kiro subscription-limit failures as first-class runtime availability failures
- problem: Freely runtime currently treats `kiro-cli` output like `Unable to verify subscription status: service error` and `Monthly request limit reached` as a normal `ai_exit_rc_0` cycle instead of a canonical availability failure. That leaves `slot_switch_reason=none` and `rate_limit_reason=none`, so the supervisor immediately relaunches into a short loop and hides the real reason the session cannot continue.
- why_now: Recent dogfood runs showed the same Kiro limit message on both root and worker supervisors. The current behavior is not just noisy; it misclassifies a known unusable state as healthy completion, which directly corrupts control-plane truth and creates relaunch churn.
- acceptance_criteria:
  - Freely can name the Kiro monthly-limit / subscription-status failure as a distinct canonical state
  - the runtime no longer records these sessions as plain `ai_exit_rc_0` when the Kiro output already proves the session is not usable
  - relaunch policy stops blind immediate resume on this failure family
  - the classification boundary is documented against existing `ai-cli-availability-manager` and watchdog families
  - focused regressions can prove root and worker supervisors stop treating the failure as a healthy completion
- promotion_gate:
  - first prove that the current runtime truly lacks a Kiro-specific availability classifier
  - keep the research narrow to runtime truth and recovery semantics, not CLI UX polish
  - do not widen this into a generic AI-tool availability redesign until the Kiro failure family is frozen
- open_questions:
  - should the first canonical state be tool-specific (`kiro_subscription_limit`) or shared (`rate_limit`) with tool annotations
  - should a `service error` without the limit string be treated as transient availability loss or as a separate probing failure
  - should root and worker reuse the same recovery path or diverge by role
  - does the existing availability skill already have enough truth to absorb this lane, or is a new issue needed
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The repository already documents Kiro limit patterns in the availability skill, but the live runtime still misclassifies the observed failure. This suggests a real taxonomy-to-runtime gap rather than a documentation-only gap.`
    verdict: `needs_more_research`
- priority: P1
- status: needs_research
- decision_reason: This is a live runtime misclassification with observable churn. It should be researched as an availability/failure-taxonomy bug before any classifier or supervisor change is attempted.
- promoted_issue_path: `pending://issue-materialization`
- milestone: `pending://milestone-binding`
- next_action: Compare the observed Kiro failure path against current runtime classifiers, then decide whether the minimal issue is a Kiro-specific availability bucket or a broader AI-tool recovery contract update.
- revisit_trigger: Revisit immediately if another dogfood run shows the same Kiro limit string being relabeled as a healthy exit and relaunched without a cooldown or block.
- session_refs:
  - tool: `kiro-cli`
  - session_id: `current-thread`
  - jsonl_path: `unavailable://thread-only`
  - role: `author`
