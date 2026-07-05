# Verification: manager-bootstrap-prompt-publication-without-continuity-materialization-governance

- issue_id: `I-20260404-1405-A`
- issue_path: `docs/B2-docs/ibm/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- branch: `feature/manager-bootstrap-prompt-publication-without-continuity-materialization-20260404-1405`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260404-1405-feature-manager-bootstrap-prompt-publication-without-continuity-materialization`
- verification_date: `2026-04-04`
- title: `Manager bootstrap prompt publication without continuity materialization governance`
- verifier: `codex`
- scope: manager bootstrap survival plus continuity worker-dispatch parsing on canonical `develop`
- verdict: `pass_for_verification`

## Summary

- Root-cause replay matched the event pattern where a fresh manager supervisor existed before `ai.pid`, so the watchdog misread bootstrap as an idle control plane and restarted it.
- The runtime now keeps a manager supervisor alive during a bounded `LAST_EXIT_REASON=starting` grace window instead of treating missing `ai.pid` as immediate restart evidence.
- A second replay showed that continuity files and worker prompts were in fact written under `.freely/run`, but runtime status still surfaced `latest_manager_worker_prompts_generated=none` because the delegated prompt lived under `## Worker Dispatch`, a heading the parser did not yet treat as launchable worker evidence.
- The current patch extends that parser contract, and live canonical status now surfaces the generated worker prompt path from the latest manager continuity.

## Implementation Decision Note

- see `docs/B2-docs/ibm/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/code-reviews/20260404-manager-bootstrap-prompt-publication-without-continuity-materialization-implementation-decision.md`

## Evidence Read

- `docs/B1-docs/raw-20260404/brainstorms.md`
- `docs/B1-docs/raw-20260404/candidates.md`
- `docs/B2-docs/ibm/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- `docs/progress/workspace-routing-foundation/p-manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
- `docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
- `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/logs/runtime-events.log`
- `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/workcell-state.env`
- `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260404-142916.md`
- `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260404-142916-worker-manager-bootstrap-continuity-materialization-codex.txt`

## Verification

1. `bash -n docs/system/workspace/scripts/runtime/freely`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
3. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
4. `./bin/governance-check`
5. `docs/system/workspace/scripts/runtime/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
6. Inspect `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/logs/runtime-events.log`
7. Inspect `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260404-143843.md`

## Findings

- No finding: the watchdog no longer self-terminates the freshly started manager before the first AI launch on canonical `develop`.
- No finding: current-format manager continuity with a delegated prompt under `## Worker Dispatch` now surfaces that prompt through runtime parser helpers and `live-status`.

## Residual Risks

- canonical root runtime is still experiencing `auth_failure / primary_rate_limit_exhausted` restart churn after the worker-handoff truth repair; that broader slot/account instability remains outside this owner scope
- the recurring `rg: command not found` messages in older historical cycle logs were not part of this fix and may still warrant separate follow-up if they reproduce in a fresh cycle
