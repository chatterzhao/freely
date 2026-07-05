# Candidates - 20260424-2230--runtime-target-worker-role-and-starting-stuck-recovery

## Context
- Source brainstorm: `docs/B1-docs/raw-20260424T223000Z/brainstorms.md`
- Status: `absorbed`
- Route: `absorb-into-i-20260421-1200-a-runtime-daemon-self-loop-followthrough-governance`

## Candidates

### C-20260424T223000Z-A: legacy issue
- candidate_format_version: `v2`
- title: `Runtime target worker role and starting-stuck recovery governance`
- research_only: `false`
- implementation_ready: `true`
- status: `absorbed`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_id: `I-20260421T120000Z-A`
- promoted_issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
  - `docs/B2-docs/runtime/runtime-lifecycle-receipt-followthrough-governance/issues/runtime-lifecycle-receipt-followthrough-governance.md`
- problem: Dogfooding on canonical `develop` at `2026-04-24` proved that `freely daemon start` does start its supervisor loop, but delegated targets do not reliably enter the correct worker execution path. Runtime currently treats branch-derived `role_hint_for_project` as the operative role truth, so a worker-contract target under `test-pre-merge-*` can still enter manager control-plane behavior, attempt to launch its own codex AI, conflict with the parent manager codex slot (`~/.codex/slot-switch.lock`), and stay pinned at `LAST_EXIT_REASON=starting` without ever writing `ai.pid`. Parent `manager_worker_launch_state.env` then keeps `ACTIVE_RUNNING_WORKER_COUNT=1` and `LAUNCHED_WORKER_PROMPTS` populated forever because the dispatch path lacks target-liveness reconciliation for a dead/never-up target launch slot, so the manager regenerates the same worker prompt every `context_compacted` rotation while HEAD never advances.
- why_now:
  - this blocker prevents Freely from autonomously selecting, finishing, and closing a single task on canonical `develop`; the daemon self-loop owner cannot reach its acceptance surface until this seam is closed
  - the architecture (PID table + `monitor_ai_pid_for_workcell_state` watchdog + worker/manager exit-contract next-action) is already directionally correct and matches the dogfooding intent; only three narrow runtime seams must be repaired so the existing mechanisms can fire
  - leaving any of the three seams open re-introduces the loop: even if one branch point uses worker contract, later runtime/control-plane calls still misclassify the target; even if the `starting` seam is reclaimed, launch-state consumers can still suppress redispatch if they read stale consumed/active worker state
- acceptance_criteria:
  - delegated target whose workcell-state carries `LAST_WORKER_VERIFICATION_METADATA_PRESENT=true` plus a complete worker contract is treated as `worker` by the relevant runtime control-plane decisions, even when the worktree name resolves to `manager` by default through `role_hint_for_project`
  - a delegated target workcell that stays at `LAST_EXIT_REASON=starting` past the existing startup lifecycle grace without producing `ai.pid` is reclaimed: zombie supervisor / watchdog residue is cleared and the parent `manager_worker_launch_state.env` can release the corresponding launch slot
  - target-ai.pid / target-liveness reconciliation happens in the dispatch-critical path before manager concludes that no unconsumed launchable worker prompt remains; dead or never-up target AI releases its entry from `LAUNCHED_WORKER_PROMPTS` and decrements `ACTIVE_RUNNING_WORKER_COUNT`, with `manager_worker_launch_state_refresh_for_status` staying a projection sync rather than the only recovery site
  - existing watchdog (`monitor_ai_pid_for_workcell_state`), exit-contract (`worker_exit_contract` / `manager_exit_contract`), and `auth_change_wake_fans_out_running_projects` semantics remain unchanged; this owner only adds the missing reclamation passes
  - guarded `feature/runtime-target-worker-role-and-starting-stuck-recovery-20260424 -> test-pre-merge-* -> develop` replay completes with concrete owner evidence
  - on canonical `develop`, `freely daemon start` autonomously selects a task, completes it, retires its worktree, and continues to the next task without manual intervention
- promotion_gate:
  - keep scope on the three named runtime seams; do not widen into role-hint global rename, agent/skill role redesign, slot-lock protocol redesign, or new exit-contract kinds
  - require feature-local pre-tests covering each seam before premerge replay
  - require canonical develop self-host acceptance (one full select -> finish -> retire -> next loop) before declaring completion
- open_questions:
  - whether current startup lifecycle grace already gives a sufficient reclaim boundary for delegated `starting` targets, or needs one additional bounded extension for slow hosts
  - whether the liveness pass should stay limited to `ai never came up after startup grace`, or also cover supervisor-alive-but-ai-dead flapping without weakening existing busy-worker semantics
- acceptance_reviews:
  - reviewer: `claude-opus-4-7`
    mode: `author review`
    summary: `Three same-family runtime seams keep daemon self-loop blocked after the first dispatch on canonical develop. The real gap is not agent/skill role definition but runtime consumption of worker-contract truth, plus a narrow delegated starting-stuck reclaim seam and dispatch-path liveness reconciliation. Owner stays narrow to those three.`
    verdict: `ready_for_issue_materialization`
- next_action: Candidate mirror only. This bounded repair is now absorbed into `I-20260421T120000Z-A`, which owns the manager/worker/runtime self-loop followthrough, guarded replay, canonical `develop` daemon acceptance, and retirement of the temporary feature/test-pre-merge worktrees.
- revisit_trigger: Re-open only if canonical `develop` still cannot autonomously self-loop after this bounded repair, or if a fourth same-family seam emerges during replay.
- decision_reason: `The three seams share one critical path (target supervisor cannot get its AI up before the parent loses confidence). Splitting them into separate owners would either ship partial fixes that still hang or duplicate evidence work for no architectural gain.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
