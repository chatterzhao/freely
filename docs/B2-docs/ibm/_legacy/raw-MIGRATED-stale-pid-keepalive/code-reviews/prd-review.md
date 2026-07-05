---
owner_issue: I-20260521T012042Z-A
issue_id: I-20260521T012042Z-A
---
# Code Review: PRD — Manager keepalive kill -0 scanning

- issue_id: I-20260521T012042Z-A

**Reviewer:** B2_IBM (design review mode)
**Artifact:** `docs/epics/stale-pid-keepalive/prd.md`
**Date:** 2026-05-21

## Summary

The PRD correctly identifies the root cause gap: the handoff DB is never updated when a worker process dies, because the existing kill -0 checks only produce a count for keepalive decisions and do not propagate results to the handoff DB.

## Review findings

### 1. Root cause accuracy ★ Correct

The PRD correctly describes both paths (process inspection / degraded) and names the specific gap: the handoff DB record stays `launched` forever. The distinction between `worker_runtime_pid_hint_is_live_for_status` (which does kill -0 but only returns count) and the need to write back to DB is accurate.

### 2. worker_pid column vs. session_id field ★ Correct decision

Using `session_id` to store OS PID would overload the column's semantics. The `session_id` stores Claude Code session IDs (UUID format), not PIDs. A new `worker_pid TEXT DEFAULT ''` column is clean.

### 3. Compatibility with existing mark_stale() ★ Correct

The PRD correctly notes that kill -0 and mark_stale() are complementary:
- kill -0: detects "process is dead" (hard state, fast)
- mark_stale(): detects "process is alive but stuck" (soft timeout, slow)

Both should coexist.

### 4. Integration point location ★ Needs clarification

The PRD suggests two options: injecting the scan as a new `elif` guard, or putting it inside `manager_supervisor_waiting_on_active_workers`. The tasks.md recommends calling it unconditionally at the start of the supervisor loop. **Recommendation**: call unconditionally before the keepalive chain, not as a guard. Reason: the scan should run regardless of which keepalive branch fires, and it may affect state used by multiple branches.

### 5. kill -0 permission assumption ★ Flag

The PRD notes "requires that the manager process has permission to signal the worker process" and acknowledges cross-container scenarios. This is correct, but worth emphasizing: `os.kill(pid, 0)` can raise `OSError` (EPERM) even when a process exists. The scan must treat all `OSError` subclasses the same — "process is not reachable = stale."

### 6. handoff_id resolution at launch ★ Flagged as open question

The PRD flags the exact mechanism to link the worker's PID to the correct handoff record as an open question. The tasks.md T-4 proposes using `prompt_file` to look up the handoff. This is reasonable but should be hardened: a worker worktree may have multiple handoff records over time. The query should use `status IN ('pending','launched')`, ordered by `created_at DESC`, limited to 1.

### 7. What if worker_pid is never set? ★ Edge case

If a worker handoff is inserted but `worker_pid` is empty (because T-4 fails or legacy records), the scan skips it. This is the correct fallback — the existing `mark_stale()` timeout still catches it eventually.

### 8. Return value of scan function ★ Minor

The PRD's sample code returns 0 unconditionally. If integrated as a guard in the keepalive chain, the return value needs to be meaningful. The tasks.md T-6 approach (unconditional call, not a guard) avoids this issue entirely.

## Verdict

**Approved with clarifications.** The design is sound, the changes are minimal and well-bounded. The only recommendation is to prefer the unconditional call approach (T-6) over the guard approach (PRD §4).

### Required fixes before implementation

- [ ] Clarify integration point: unconditional before keepalive chain
- [ ] Ensure all `OSError` subclasses are treated the same in the scan function
