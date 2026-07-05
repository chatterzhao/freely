# Code Review: latest-manager-continuity-worker-consumption-governance plain-list prompt parser verification
- issue_id: `I-20260322-0445`

## Scope

- same-family repair under `I-20260322-0445`
- focus: runtime must treat plain-list entries under `## Worker Prompts` as launchable prompts so manager-authored cleanup followthrough can actually launch

## Success Criteria

1. `latest_manager_worker_prompt_paths_from_continuity` includes plain bullet prompts under `## Worker Prompts`
2. `ensure_manager_once` consumes current-format continuity and records the generated/consumed prompt truth instead of leaving launch-state empty
3. frozen prompt handling does not regress

## Pre-merge Verification

- `bash docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
- `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
- `./bin/governance-check`

All commands passed in worktree `feature/manager-continuity-worker-prompt-plain-list-parser-20260424`.

## Canonical Replay Trigger

- canonical root replay before this repair showed:
  - manager continuity `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260424-025646.md` contained `## Worker Prompts` followed by a plain bullet path
  - prompt `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260424-025646-worker-runtime-cleanup-followthrough-resume-hygiene-codex.txt` should have launched the retained cleanup lane
  - `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-worker-launch-state.env` still showed `LAST_MANAGER_WORKER_PROMPTS_GENERATED=""` and `LAUNCHED_WORKER_PROMPTS="none"`
- this proves the break sat on runtime continuity parsing, not on manager task selection or stale worker tooling

## Governance Closeout

- feature commit: `15cc84bf` (`Fix manager continuity plain-list worker prompt parsing`)
- canonical merge path for this repair is:
  - `feature/manager-continuity-worker-prompt-plain-list-parser-20260424 -> test-pre-merge-20260424-manager-continuity-worker-prompt-plain-list-parser -> develop`
