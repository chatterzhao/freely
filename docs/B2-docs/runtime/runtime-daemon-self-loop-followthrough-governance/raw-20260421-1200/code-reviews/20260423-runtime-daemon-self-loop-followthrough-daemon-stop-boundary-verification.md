# Verification: runtime-daemon-self-loop-followthrough-governance daemon stop boundary refresh

- issue_id: `I-20260421-1200-A`
- date: `2026-04-23`
- scope: `Refresh the manager operator-stop freshness boundary on explicit daemon stop so startup patrol cannot reuse pre-stop continuity as current queue truth.`

## Findings

- `FAIL`: canonical restart observation showed startup was generating a fresh `manager-task-source-scan-latest.json`, but patrol still treated the older cleanup continuity as current because the staleness boundary only refreshed for `operator_stop`.
- `FAIL`: `daemon stop` persisted `LAST_EXIT_REASON=operator_daemon_stop`, so the next startup patrol could legally re-anchor on a pre-stop continuity and bypass the fresh scan-selected queue.
- `PASS`: runtime now treats `operator_daemon_stop` as the same explicit operator-stop freshness boundary used by manager continuity filtering.
- `PASS`: this remains narrow: runtime-owned restarts and other non-operator exits still do not rewrite the freshness boundary.

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-daemon-stop-refreshes-manager-operator-boundary`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-ignores-pre-stop-manager-continuity-focus`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-command-semantics`

## Status

- `PASS`: explicit daemon stop now invalidates pre-stop continuity for the next startup patrol, so fresh scan-selected work can take precedence after restart.
- `PENDING`: guarded promote plus canonical `develop` replay still must prove the daemon now chooses from fresh scan JSON, closes the selected task lawfully, retires the relevant worktree, and continues to the next task.

## Implementation Decision Note

- decision: `Extend the existing explicit operator-stop freshness boundary to cover daemon stop, rather than inventing a second patrol-reset marker.`
- why_this: `The regression was not a new scheduling policy problem; it was a mismatch between the already-authoritative patrol boundary and the explicit daemon-stop exit reason.`
- alternatives_considered: `Teach patrol to special-case operator_daemon_stop in prompt assembly only; ignore pre-stop continuity whenever any scan json exists; clear all continuity artifacts on daemon stop.`
- boundary_non_goals: `No scan-priority redesign, no cleanup-governance rewrite, and no relaxation of the existing distinction between explicit operator stops and runtime-owned restarts.`
- residual_risk: `Canonical replay may still expose another narrower followthrough seam after startup picks from fresh scan JSON, but it should no longer be pinned to pre-stop continuity just because the stop came from daemon control-plane entrypoints.`
