# Code Review: latest-manager-continuity-worker-consumption-governance delegated freshness verification
- issue_id: `I-20260322-0445`

## Scope

- same-family repair under `I-20260322-0445`
- focus: stale delegated continuation backlog must not hijack the current manager round

## Success Criteria

1. fresh delegated governance interruptions enter the current manager prompt without being bundled behind older continuation backlog
2. delegated items older than the latest manager continuity do not auto-reenter the current manager lane unless a newer continuity or fresh claim carries them forward
3. front-door intake queue only shows not-yet-delegated chat items
4. canonical `develop` replay routes the new `成功标准` governance task first instead of silently reusing the older `runtime-lifecycle-validation` lane

## Pre-merge Verification

- `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-filters-stale-delegated-continuations`
- `bash docs/system/workspace/scripts/tests/test-freely-human-chat-intake`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-continuity-resume-focus`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `./bin/governance-check`

All commands passed in worktree `feature/success-standard-governance-20260420`.

## Canonical Replay Evidence

- patched runtime was started against canonical project `/Users/zhaoyu/Downloads/code/my-freely/freely`
- fresh interruption sent with:
  - `freely chat --project /Users/zhaoyu/Downloads/code/my-freely/freely "...成功标准..."`
- after one minute, `freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely` reported:
  - `last_consumed_delegated_continuation_ids: 20260420-020937-pre-brainstorm-owner-1-success-c`
  - `current_prompt_has_delegated_continuation: 1`
  - `intake_snapshot: none`
- prompt file `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/prompt-20260420-021006.txt` contained the fresh intake:
  - `intake_id=20260420-020937-pre-brainstorm-owner-1-success-c message=新治理能力候选任务：把项目治理中的表述统一收敛为‘成功标准’...`
- the same prompt only mentioned `feature/runtime-lifecycle-validation-20260420` inside worktree inventory and did not surface it as the delegated continuation handoff for the current round

## Governance Closeout

- feature commit: `b44b05c8` (`Guard stale delegated continuations`)
- first direct `feature -> develop` merge attempt was correctly blocked by guarded-merge policy
- canonical path for this repair is:
  - `feature/success-standard-governance-20260420 -> test-pre-merge-success-standard-governance-20260420-0215 -> develop`
