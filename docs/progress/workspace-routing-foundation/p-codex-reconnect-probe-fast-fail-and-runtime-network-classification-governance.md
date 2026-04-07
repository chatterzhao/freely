# Progress: codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance

- issue_id: `I-20260406-0901-A`
- issue_path: `docs/epics/workspace-routing-foundation/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/issues/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance.md`
- title: `Codex reconnect probe fast-fail and runtime network classification governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/codex-hi-fast-fail-and-runtime-availability`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-codex-hi-fast-fail-and-runtime-availability`
- updated_at: `2026-04-06`
- closure_status: `open`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Materialized `I-20260406-0901-A` as the canonical follow-on owner for reconnect fast-fail and runtime network classification alignment.
- Existing bounded implementation lives in `feature/codex-hi-fast-fail-and-runtime-availability`; canonical doc-loop is now aligned with this execution lane.
- Historical residuals in `feature/fix-codex-apikey-availability-lock` were reviewed; only the runtime signal-filter fragment belonged to this owner, while the remaining current-live apikey/bootstrap changes require a separate follow-on.
- The focused reconnect/status/runtime regression set, runtime signal-filter regression, `pretests-gate`, and `governance-check` now pass in this worktree, so the owner has moved from bounded cleanup into verification.
- Promotion is temporarily blocked by the current Codex sandbox because `.git/worktrees/...` is not writable in this session, so checkpoint commit / `test-pre-merge-*` creation / guarded merge cannot execute yet.

## Current Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-detects-network-failure-before-timeout`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-network-failure-cleans-child-process`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-status-live-apikey-network-failure`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-live-apikey-network-failure`
- `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
- `bash docs/system/workspace/scripts/tests/test-freely-runtime-auth-failure-signal-filter`
- `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-codex-hi-fast-fail-and-runtime-availability --issue docs/epics/workspace-routing-foundation/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/issues/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance.md`
- `./bin/governance-check`
- `git diff --check`
- `docs/epics/workspace-routing-foundation/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/code-reviews/20260406-codex-reconnect-probe-fast-fail-and-runtime-network-classification-verification.md`

## Next Action

- Hold `feature/fix-codex-apikey-availability-lock` in `retire-only` status after extracting the runtime signal-filter fragment; do not continue implementation there.
- Keep this owner in verification until `I-20260406-1829-A` merges first and `I-20260406-1851-A` either merges or proves conflict-free, because this lane overlaps both `watchdog` and `ai-cli`.
- Treat the guarded promotion order as `I-20260406-1829-A` first, `I-20260406-1851-A` second, then `I-20260406-0901-A` last so the reconnect lane rebases onto the smallest stable surface.
- Keep interactive login as a separate Codex-first UX follow-on instead of widening the reconnect lane.
- Once a session with writable `.git/worktrees/...` is available, checkpoint this branch after `1829` and `1851` land, then build a fresh `test-pre-merge-*` batch for the final guarded promotion.
