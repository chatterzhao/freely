# Progress: runtime-selfhost-continuity-gap-and-status-truth-governance

- issue_id: `I-20260407-0215-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
- title: `Runtime self-host continuity gap and status truth governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-live-status-and-manager-continuity-followthrough-20260407`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260407-feature-runtime-live-status-and-manager-continuity-followthrough`
- updated_at: `2026-04-07 21:35 PDT`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- `I-20260407-0215-A` remains a bounded verification owner, not a reopened implementation lane and not a cleanup-ready closeout.
- The dirty feature-worktree entrypoint still exits `0` and stays machine-readable against the root project, so the bounded repair in this worktree remains intact.
- The direct tracked root `develop` entrypoint again reproduces the canonical failure mode in this replay window: empty stdout with `exit 1`, so tracked-root absorption still has not happened.
- The worker worktree briefly drifted out of its own recorded verification truth because `manager_ai_pid_hint_for_project()` still returned non-zero on a dead `ai.pid`; this round repairs that stale-`ai.pid` path and refreshes the verification evidence.
- The root project has generated a newer manager prompt without yet materializing its required continuity file, and the patched feature entrypoint still surfaces that renewed gap machine-readably instead of exiting blank.
- The current route remains `continuation -> committed_issues -> completion_verification -> target_owner=manager`.

## Implemented Slice

- Guarded PID-hint fallback paths so status commands degrade to readable output instead of exiting before their first line.
- Extended that degrade guard to `manager_ai_pid_hint_for_project()` so a stale `ai.pid` no longer collapses `live-status` under `set -euo pipefail`.
- Replaced the `rg`-only workspace-root probe with a fallback that also works with plain `grep`.
- Added continuity-gap detection keyed to the latest prompt's required manager continuity path and surfaced it through status commands, with named `manager_continuity_gap_*` fields in `live-status` and a bounded fleet-summary row in `fleet-status` for follow-on runtime decisions.
- Extended continuity-gap status with age and writer-state truth so self-host followthrough can tell whether the manager is still in startup grace or has stayed missing too long; `live-status` carries the full machine-readable writer-state while `fleet-status` keeps the summarized fleet view.
- Tightened `start-lead-agent.sh` manager prompt guardrails so same-lane handoff stays anchored to the active feature worktree and avoids `zsh` `status` variable collisions.
- Added focused regressions for continuity-gap surface and pid-hint / `rg`-missing degrade behavior.
- Reworked blocked-supervision and delegated-continuation reads so status discovery pulls candidate truth from interruption-resolution artifacts instead of rescanning the full intake pool on every call.
- Wrote the implementation decision note under `verification_artifact_dir` and kept the owner conclusion bounded: status truth is fixed in this worktree; auto-materializing missing continuity remains a separate future owner if needed.

## Current Verification

- Re-ran the bounded verification set at `2026-04-07 21:35 PDT`: `bash -n docs/system/workspace/scripts/runtime/freely`, all focused regressions, `git diff --check`, and `./bin/governance-check` all pass in this dirty feature worktree.
- From `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260407-feature-runtime-live-status-and-manager-continuity-followthrough`, direct execution of `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260407-feature-runtime-live-status-and-manager-continuity-followthrough/bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely` now exits `0` with machine-readable output again. The refreshed replay shows `activity_state=stalled_without_runtime`, `last_exit_reason=execution_network_persistent`, and the continuity-gap surface still present instead of blank exit.
- From `/Users/zhaoyu/Downloads/code/my-freely/freely`, the tracked root entrypoint `/Users/zhaoyu/Downloads/code/my-freely/freely/bin/freely` still exits `1` with empty stdout (`0` bytes, `0` lines), so canonical root still does not emit the repaired status surface for the same project state.
- The current contrast is therefore narrower and more current than the stale 20:13 note: this feature worktree again survives dead pid-file evidence, including stale `ai.pid`, while tracked root still crashes before any consumable status body and still has not absorbed this worktree's runtime-status helpers.

## Verification Evidence

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-manager-continuity-gap-surface`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-pid-hint-and-rg-degrade`
- `bash docs/system/workspace/scripts/tests/test-freely-discover-supervisor-pid-sigpipe-guard`
- `bash docs/system/workspace/scripts/tests/test-start-lead-agent-manager-feature-owner-doc-anchor`
- `bash docs/system/workspace/scripts/tests/test-start-lead-agent-manager-zsh-status-guard`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-blocked-supervision-status-surface`
- `./bin/governance-check`
- `git diff --check`
- `/usr/bin/time -p ./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
- `cd /Users/zhaoyu/Downloads/code/my-freely/freely && /usr/bin/time -p ./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
- `docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/code-reviews/20260407-runtime-status-truth-verification-replay.md`

## Next Action

- Treat `I-20260407-0215-A` as a bounded status-truth owner that remains in active verification until the tracked root `develop` entrypoint absorbs this worktree's repair. Current manager handoff state remains `still_waiting_on_absorption`. As of `2026-04-07 21:35 PDT`, the patched feature entrypoint at `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260407-feature-runtime-live-status-and-manager-continuity-followthrough/bin/freely` again exits `0` while keeping canonical root-project status machine-readable, but tracked root `/Users/zhaoyu/Downloads/code/my-freely/freely/bin/freely` still exits `1` with empty stdout for the same project state. The refreshed read-only contrast now shows one more absorbed-by-feature-only guard than the stale verification note captured: root still leaves `manager_ai_pid_hint_for_project()` unguarded under `set -euo pipefail` alongside the remaining unabsorbed continuity-gap snapshot/output helpers, while this worktree now guards the stale-`ai.pid` path too. Canonical tracked-root absorption is therefore still missing even though this owner remains bounded and status-only. The authoritative route evidence still stays worker-scoped and unchanged after the fresh rerun: `source_class=continuation`, highest-priority pool `committed_issues`, `route_kind=completion_verification`, `target_owner=manager`, `selected_tool=codex`, and `workspace_action=reuse_current_worktree`. The next manager judgment should therefore remain merge-prep / absorption, not cleanup. Keep the separate research-only pre-brainstorm around runtime evidence provenance / canonical absorption gate / manager continuity materialization visible as its own lane; do not silently fold it into this owner. Worker-local next prompt for traceability: `Manager route only. Consume I-20260407-0215-A as a bounded verification owner, not a reopened dev loop. Use the current issue/progress plus the 2026-04-07 21:35 PDT verification replay to judge merge-prep / absorption against tracked root develop. The feature entrypoint again survives dead pid-file evidence, including stale ai.pid, and still surfaces root-project status machine-readably, while tracked root still returns exit 1 with empty stdout for the same project state; keep the owner in manager-owned completion_verification and prepare absorption, not cleanup.`

## 2026-04-08 Boundary Recheck

- Review of stale mixed branch `feature/manager-continuity-gap-and-worker-recovery-guard-20260408` confirmed it does not widen `I-20260407-0215-A`.
- Current `develop` had already absorbed that branch's retire-ready recovery and multiline dispatch-metadata repairs through `I-20260322-0445`.
- The only residual carried forward is worker `live-status` / `fleet-status` authoritative intent fallback from manager continuity when a worker-local prompt lacks machine-readable intent headers.
- Boundary judgement:
  - keep `I-20260407-0215-A` status-only and continuity-gap scoped
  - route the residual worker intent fallback to `I-20260322-0445` instead of splitting a new issue or widening this owner
