# Progress: runtime-selfhost-continuity-gap-and-status-truth-governance

- issue_id: `I-20260407-0215-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
- title: `Runtime self-host continuity gap and status truth governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-live-status-and-manager-continuity-followthrough-20260407`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260407-feature-runtime-live-status-and-manager-continuity-followthrough`
- updated_at: `2026-04-08 02:22 PDT`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- `I-20260407-0215-A` remains a bounded verification owner, not a reopened implementation lane and not a worker-granted cleanup closeout.
- `scope_drift=no`: the worktree stays inside the bounded `I-20260407-0215-A` write scope, the tree was clean before this replay, and this round only refreshes same-lane verification truth.
- The feature-worktree entrypoint and the tracked root `develop` entrypoint now both replay machine-readable `live-status` successfully against the root project, so the bounded status-truth surface is absorbed at tracked root.
- The executed entrypoint identity still differs by absolute path and is now recorded explicitly: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260407-feature-runtime-live-status-and-manager-continuity-followthrough/bin/freely` versus `/Users/zhaoyu/Downloads/code/my-freely/freely/bin/freely`.
- The active project no longer has a missing prompt-required continuity file: both entrypoints now surface `manager_continuity_gap_state=none`, `manager_continuity_gap_summary=present`, and the same expected/latest-generated continuity path.
- The remaining live runtime truth is generated-versus-consumed continuity drift on a stalled project: both entrypoints now show `latest_manager_continuity_generated=/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260408-012541.md` while `latest_manager_continuity_consumed=/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260407-221639.md`.
- The current route remains `continuation -> committed_issues -> completion_verification -> target_owner=manager`, and the worker-side handoff state is now `ready_for_manager_completion_verification`.
- `restart_point`: re-run the feature entrypoint and tracked-root entrypoint `live-status` commands against `/Users/zhaoyu/Downloads/code/my-freely/freely`, then compare the bounded manager-continuity and ownership-conflict fields recorded in the verification artifact before asking manager to close verification.

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

- The last full bounded verification set remains the `2026-04-07 21:35 PDT` replay: `bash -n docs/system/workspace/scripts/runtime/freely`, focused regressions, `git diff --check`, and `./bin/governance-check` all passed in this worktree.
- At `2026-04-08 02:22 PDT`, from `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260407-feature-runtime-live-status-and-manager-continuity-followthrough`, direct execution of `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260407-feature-runtime-live-status-and-manager-continuity-followthrough/bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely` exited `0` and emitted `131` lines / `12656` bytes of machine-readable output.
- At `2026-04-08 02:22 PDT`, from `/Users/zhaoyu/Downloads/code/my-freely/freely`, direct execution of `/Users/zhaoyu/Downloads/code/my-freely/freely/bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely` also exited `0` and emitted `131` lines / `12656` bytes of machine-readable output.
- At `2026-04-08 02:22 PDT`, a focused field replay confirmed parity across both entrypoints for the current bounded truth: `activity_state: stalled_without_runtime`, `last_exit_reason: operator_stop`, `manager_continuity_gap_state: none`, `manager_continuity_gap_reason: none`, `manager_continuity_gap_expected_path: /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260408-012541.md`, `manager_continuity_gap_latest_generated: /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260408-012541.md`, `manager_continuity_gap_prompt_file: /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/prompt-20260408-012536.txt`, `manager_continuity_gap_age_secs: 0`, `manager_continuity_gap_age_state: none`, `manager_continuity_gap_writer_state: none`, `manager_continuity_gap_summary: present`, `latest_manager_continuity_generated: /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260408-012541.md`, `latest_manager_continuity_consumed: /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260407-221639.md`, and `manager_pending_ownership_conflicts: none`.
- The current contrast is therefore no longer feature-success versus root-failure. The only live distinction in this replay is which absolute `bin/freely` entrypoint executed; the bounded status surface itself is absorbed at tracked root.

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

- Treat `I-20260407-0215-A` as a bounded status-truth owner that stays in manager-owned `completion_verification` only. Current worker handoff state remains `ready_for_manager_completion_verification`, and this round still concludes `scope_drift=no`. As of `2026-04-08 02:22 PDT`, the feature entrypoint and tracked-root entrypoint both return `exit 0` and surface the same bounded status truth for the same target project, so canonical tracked-root absorption remains present after the current fresh replay. The missing-continuity symptom itself is still inactive: both entrypoints report `manager_continuity_gap_state: none` with the same expected/latest-generated path. The remaining manager-visible runtime truth is generated-versus-consumed continuity drift on a stalled project, still showing `latest_manager_continuity_generated=/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260408-012541.md` while consumption remains at `.../manager-continuity-20260407-221639.md`. The authoritative route evidence stays worker-scoped and unchanged after the fresh rerun: `source_class=continuation`, highest-priority pool `committed_issues`, `route_kind=completion_verification`, `target_owner=manager`, `selected_tool=codex`, and `workspace_action=reuse_current_worktree`. The next manager judgment should therefore be completion verification closeout, not reopened worker implementation and not cleanup delegated from this worktree. Keep the separate research-only pre-brainstorm around runtime evidence provenance / canonical absorption gate / manager continuity materialization visible as its own lane; do not silently fold it into this owner. Worker-local restart_point for traceability: `Manager route only. Consume I-20260407-0215-A as a bounded verification owner, not a reopened dev loop. Re-run /Users/zhaoyu/Downloads/code/my-freely/freely/bin/freely and /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260407-feature-runtime-live-status-and-manager-continuity-followthrough/bin/freely against /Users/zhaoyu/Downloads/code/my-freely/freely, compare the bounded manager-continuity fields captured in the verification artifact, and keep closeout in manager-owned completion verification, not worker cleanup.`
