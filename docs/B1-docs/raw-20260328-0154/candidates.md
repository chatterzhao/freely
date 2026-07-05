# Candidates - 20260328-0154--manager-stall-reentry-false-positive-supervision-thrash

## Context
- Source brainstorm: `./brainstorms.md`
- Status: absorbed

## Candidates

### C-20260328-0154-A
- title: Add an idle-safe manager supervision contract before runtime triggers local continuation reentry
- problem: 当前 manager stall recovery 把“delegated continuation 已进入 prompt 但没有新 launchable handoff”统一视为可恢复 stall；这会把 `same-lane busy` 的合法监督等待态误判成假活，并持续触发 `runtime-stalled-ai-recovery`。
- why_now: `2026-03-28` 的 `develop` 现场先出现连续 `operator_stop -> local_continuation_reentry -> fresh manager AI`，而 canonical worker 同时真实推进 IBM materialization；随后又进一步恶化为 `QUEUED_WORKER_PROMPTS` 残留、`ACTIVE_RUNNING_WORKER_COUNT="0"`、develop 与 canonical worker 都变成 `desired=running but runtime down`。这说明当前问题已经不是单点 auth failure，也不是单纯 worker 没干活，而是 manager stall recovery 与 manager-worker launch truth 的契约失配。
- acceptance_hint:
  - 冻结 manager `waiting_on_worker` / `same-lane busy wait` 的 canonical runtime truth，或证明现有 `manager-worker-launch-state.env` 已足够承载它
  - 明确该等待态如何抑制或放宽 `manager_ai_stalled_after_delegated_continuation_prompt`
  - 证明 `auth_failure` / intake superseded / 真 stall 仍不会被新的等待态误吞
  - 在脚本测试中补齐负向冻结：`active worker + queued_same_lane_busy` 时不得触发 `recover_stalled_manager_ai_if_needed`
- priority: P0
- status: absorbed
- milestone: M-20260306-workspace-routing-foundation
- promoted_issue_path: `docs/B2-docs/ibm/manager-delegated-continuation-stall-recovery-governance/issues/manager-delegated-continuation-stall-recovery-governance.md`
- decision_reason: 本轮已确认这条 false-positive supervision thrash 不是独立 owner，而是 `manager delegated continuation stall recovery` 家族上的新边界。最新最小修复和 targeted regressions 已经把这个边界冻结，因此本条预研转为 supporting evidence，由正式 issue 接管。
- next_action: 作为 supporting evidence 保留；后续只在正式 issue 需要补充 same-lane busy / stale queue 现场证据时回写，不再单独推进。
- revisit_trigger: 若正式 issue 之外又出现更广泛的 control-plane thrash contract 漂移，再新开 lifecycle，而不是重新激活本 supporting pre-brainstorm。
- session_refs:
  - tool: codex
    session_id: current-thread
    jsonl_path: unavailable://codex-thread-only
    role: author
  - tool: codex
    session_id: current-thread-review-pass
    jsonl_path: unavailable://local-review-only
    role: reviewer
