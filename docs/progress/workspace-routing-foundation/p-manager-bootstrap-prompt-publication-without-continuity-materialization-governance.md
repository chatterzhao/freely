# Progress: manager-bootstrap-prompt-publication-without-continuity-materialization-governance

- issue_id: `I-20260404-1405-A`
- issue_path: `docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- title: `Manager bootstrap prompt publication without continuity materialization governance`
- phase_state: `in_verification`
- runtime_state: `in_feature_worktree`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/manager-bootstrap-prompt-publication-without-continuity-materialization-20260404-1405`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260404-1405-feature-manager-bootstrap-prompt-publication-without-continuity-materialization`
- updated_at: `2026-04-04`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Canonical `develop` on `2026-04-04` first reproduced a bootstrap race: `freely start` generated prompt publication, then the watchdog restarted the fresh supervisor during the `supervisor.pid`-before-`ai.pid` window and collapsed the round into misleading `operator_stop` truth.
- The active runtime patch now preserves a bounded bootstrap grace window keyed off `LAST_EXIT_REASON=starting`, and replay on canonical `develop` reached stable `activity_state=ai_active` with authoritative supervisor, watchdog, dispatcher, and AI PIDs.
- Once bootstrap survived, the next replay proved manager continuity artifacts were being written, but runtime status still surfaced `latest_manager_worker_prompts_generated=none` because the latest continuity wrote its delegated prompt under `## Worker Dispatch`, which the parser did not treat as a launchable worker-prompt section.
- The current batch patches that parser gap and verifies against both focused fixture tests and the live canonical root status surface.

## Current Batch Risks

1. `operator_stop` still conflates explicit human stop and some internal stop paths outside this narrow bootstrap and worker-dispatch handoff slice.
2. Canonical root runtime is now hitting `auth_failure / primary_rate_limit_exhausted` restart churn after this lane's worker-handoff truth is restored; that broader account/slot instability remains a separate owner.

## Next Action

1. Merge this verified lane into `develop`.
2. Re-run root `./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely` after merge to confirm canonical manager continuity and worker prompt consumption remain visible.
3. If restart churn persists on canonical root, route the `auth_failure / primary_rate_limit_exhausted` storm into its own owner instead of widening this issue.
