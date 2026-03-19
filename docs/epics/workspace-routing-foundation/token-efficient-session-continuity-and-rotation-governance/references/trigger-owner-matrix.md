# Trigger Matrix: token-efficient session continuity and rotation

## Purpose

This matrix keeps `runtime`, `manager`, `worker`, and `watchdog` from solving the same continuity problem in different ways.

## Matrix

| Trigger | Owner | Primary Artifact | Primary Action | Fallback |
| --- | --- | --- | --- | --- |
| `context_ratio >= warn` and current AI still healthy | current session (`manager` or `worker`) | phase-appropriate continuity artifact | update continuity first, then continue current issue | if the session exits naturally later, let runtime carry only continuity + handoff |
| `context compacted`, `context_ratio >= rotate`, repeated degraded resumes | worktree runtime | session handoff + continuity artifact | run `fresh_with_handoff` | if handoff is thin, keep `previous_*_path` references for selective recovery |
| AI process exited but worktree runtime still alive | worktree runtime | session-state + handoff + previous evidence paths | decide `resume` vs `fresh_with_handoff`, then relaunch tool | when resume evidence is insufficient, prefer `fresh_with_handoff` |
| manager or worker runtime missing | outer watchdog / `ensure-manager` | manager bootstrap handoff | relaunch manager entrypoint; do not generate semantic summaries here | manager reads fleet snapshot and decides which workers should be resumed or restarted |
| all candidate accounts unavailable or current account rate-limited | global watchdog | account recovery state + manager bootstrap handoff | probe all accounts, switch to a live one; otherwise sleep until earliest reset | after account recovery, relaunch manager and let manager inspect the fleet |

## Notes

- `manager` continuity is project-level:
  - fleet snapshot
  - expected-running worktrees
  - blocked workers
  - next supervision priority
- `worker` continuity is issue-level:
  - issue state
  - verification status
  - blocker
  - next execution step
- `previous_tool_session_id`, `previous_tool_jsonl_path`, and `previous_cycle_log` are fallback evidence references, not default prompt payload.
- If Codex later exposes an official non-interactive compaction capability, this matrix should be revised to prefer that official path before external fallback handoff logic.
