# Candidates - 20260331-1837--worker-first-hop-role-boundary-regression

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260331T183700Z-A: legacy issue
- candidate_format_version: v2
- title: Worker first-hop role boundary regression in prompt generation and follow-on reentry
- problem: On a live dogfood worker lane, the delegated feature-worktree session completed its assigned verification-closeout task and then re-entered a new cycle that behaved like a manager session. The worker prompt still routed through `lead-agent` despite `MANAGER_MODE=false`, and the follow-on worker session began reading root `develop` live-status and writing a `manager-continuity-*` artifact from the worker worktree. This violates the frozen manager/worker boundary and risks letting worker lanes perform project-level supervision, merge-prep judgement, and cleanup disposition outside the canonical manager runtime.
- why_now: This was reproduced on an active canonical lane rather than in a synthetic prompt-only check. The repro shows the defect can appear precisely after a successful worker task completion, which means it can silently distort project governance even when the delegated business work itself succeeds.
- acceptance_criteria:
  - worker first-hop prompts for `MANAGER_MODE=false` / `feature/*` clearly hand off to `worker-agent` semantics rather than manager-style patrol semantics
  - a completed worker lane does not automatically drift into project-level supervision on the next cycle unless the manager explicitly delegates a new manager-owned handoff
  - worker worktrees stop emitting manager-only artifacts such as `manager-continuity-*` when the lane is only delegated for issue execution or verification evidence
  - the eventual repair preserves legitimate worker continuity / blocker writeback without preventing runtime-owned recovery or resume
  - focused regressions cover both prompt-generation truth and the live follow-on reentry boundary
- promotion_gate:
  - confirm whether the primary bug is prompt generation, reentry lifecycle semantics, or a two-part contract split
  - keep the first repair narrow: worker role routing and artifact boundary only
  - avoid widening into a general redesign of merge-prep, verification closure, or manager patrol
- open_questions:
  - should the fix land entirely in `docs/system/workspace/scripts/start-lead-agent.sh`, or also in runtime relaunch logic
  - should worker follow-on sessions be forced through `worker-agent` explicitly, or should `lead-agent` stay as the universal first-hop with stronger branch-aware routing
  - what is the minimum artifact contract that lets a worker report `merge-ready evidence` without self-promoting into manager cleanup judgement
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The live repro is incompatible with the frozen worker-agent contract. The behavior should be treated as a bug, but the first repair must stay narrow until prompt-generation and reentry ownership are separated cleanly.`
    verdict: `needs_more_research`
- priority: P1
- status: needs_research
- decision_reason: This is not a mere UX polish item. The feature-worktree worker crossed a frozen role boundary and produced manager-only artifacts. However, the exact repair owner is still ambiguous between prompt-generation and worker reentry semantics, so the safe next step is a focused research lifecycle rather than an immediate code patch.
- promoted_issue_path: `pending://issue-materialization`
- milestone: `M-20260306-workspace-routing-foundation`
- next_action: Trace the worker prompt-generation path and the worker follow-on relaunch path together, then decide whether this becomes a same-family focused repair issue or two narrower runtime-facing fixes.
- revisit_trigger: Revisit immediately if another worker lane writes manager-only artifacts, performs project-level patrol after completing delegated work, or if `MANAGER_MODE=false` prompts continue entering `lead-agent` without a clean worker-only second-hop boundary.
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
