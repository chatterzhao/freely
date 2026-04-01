# Progress - Live-status Already-Running-Attach Regression

## Metadata
- candidate_id: C-20260330-2318-A
- phase: needs_research
- worktree: 20260330-231827-feature-live-status-already-running-attach-regression
- branch: feature/live-status-already-running-attach-regression-20260330-231827
- started: 2026-03-31

## Current Status

**Phase**: Root cause analysis complete, focused repro attempted but not yet successful

**Last Update**: 2026-03-31T18:00:00-07:00

## Work Completed

### 1. Candidate Promotion to Milestone ✓
- Added `C-20260330-2318-A` to `M-20260306-workspace-routing-foundation` candidate queue
- Status: `needs_research`
- Priority: P1

### 2. Root Cause Analysis Complete ✓
- Created `docs/pre-brainstorms/20260330-2318--live-status-already-running-attach-regression/root-cause-analysis.md`
- Confirmed the optimistic attach write path in `start_project_runtime()`
- Confirmed `live-status` only reconciles upward and does not downgrade stale optimistic state
- Reframed earlier "PID reuse / stale pid file" claims as unproven hypotheses
- Analyzed production evidence showing 17-minute gap between cleanup and false-positive write
- Identified three key code paths and four potential design directions

### 3. Focused Repro Attempt ✓
- Created `test-live-status-attach-false-positive-repro` script
- Attempted to reproduce the false-positive by exercising real `runtime/freely` attach path
- Encountered complexity in setting up isolated test project with full Freely structure
- Decision: Defer complex repro harness until next real occurrence provides more trigger evidence

### 4. Code Path Analysis ✓
Identified three key functions in the problematic path:
- `start_project_runtime()` (line 5435): Writes optimistic state without verification
- `ensure_no_active_supervisor_conflict()` (line 5394): Returns 10 for attach success
- `resolve_active_supervisor_pid_for_start()` (line 5370): Resolves PID from file or discovery

### 5. Existing Contract Coverage Verified ✓
- `test-freely-project-command-semantics` passes and confirms attach reuse is an intentional contract
- `test-freely-status-pid-ownership` passes and confirms stale foreign supervisor PIDs are filtered elsewhere

## Root Causes Identified

1. **Optimistic State Write**: Attach success writes `up/up` without any stronger health/observability gate
2. **One-Way Reconciliation**: `live-status` intentionally preserves historical state when no live PID is found
3. **No Runtime Event**: Attach-only path doesn't emit runtime event for observability

## Next Steps

### Immediate (Before Promotion to Issue)
1. **Wait for Next Real Occurrence**: Rather than force a complex repro, wait for the next time this false-positive appears in real dogfooding
2. **Collect More Trigger Evidence**: When it occurs again, capture:
   - Exact timeline of `ensure-manager` bootstrap attempts
   - Process table snapshot showing what owned the "reused" PID
   - Whether concurrent `start` attempts were racing
   - Whether the PID was truly a short-lived supervisor or something else

### After Trigger is Confirmed
3. **Choose Fix Strategy**: Based on confirmed trigger, select from:
   - Option 1: Make attach writes less optimistic (verify supervisor health)
   - Option 2: Downgrade attach state to soft/stale (defensive read-side)
   - Option 3: Always emit runtime event for attach (observability)
   - Option 4: Combination of above

4. **Implement and Test**: Once fix strategy is chosen, implement with focused regression test

5. **Promote to Issue**: Only promote to full issue once:
   - Trigger mechanism is confirmed
   - Fix strategy is validated
   - Regression test passes

## Promotion Gate

This candidate should be promoted to a milestone-owned issue when:
- [ ] A focused repro successfully demonstrates the exact attach path that writes false-positive state
- [ ] The trigger mechanism (concurrent start / short-lived supervisor / stale PID discovery) is confirmed
- [ ] A fix strategy is validated against the confirmed trigger
- [ ] The fix preserves existing valid attach-reuse contract

## Blocker

Current blocker: **Trigger mechanism not yet reproduced in isolation**

The symptom is real and the code paths are identified, but the exact sequence that causes the false-positive write is not yet proven. Rather than speculate with a complex repro harness, we should wait for the next real occurrence and collect more evidence at that time.
4. **Trigger Mechanism Still Unproven**: earlier "random PID reuse / stale pid file" explanations are not yet demonstrated by a focused repro

## Fix Proposal

Do not choose a fix yet. First reproduce the real trigger in a focused harness, then decide between:

1. **Write-side hardening**
   - Gate attach reuse more strictly
   - Avoid writing `last_ai_state=up` without a confirmed AI PID

2. **Read-side downgrade for attach-specific history**
   - Treat `already_running_attach` as a softer persisted hint
   - Let `live-status` downgrade when no current owned runtime remains

3. **Attach observability**
   - Emit an explicit runtime event for attach-only success

## Next Actions

### Immediate (Current Session)
- [ ] Build a focused repro that hits the real `start_project_runtime()` attach path
- [ ] Distinguish same-project short-window attach from broader PID validation failures
- [ ] Decide whether repair belongs in write-side attach semantics, read-side downgrade, or both
- [ ] Keep existing attach and stale-ownership tests green

### Follow-up
- [ ] Verify fix prevents regression
- [ ] Ensure existing valid attach cases still work
- [ ] Update documentation for attach semantics
- [ ] Consider if `live-status` should also reconcile `already_running_attach` state

## Open Questions

1. Should `live-status` treat `already_running_attach` as soft/stale unless current PIDs confirm?
2. Should attach-only writes use a different exit reason like `attach_pending_verification`?
3. Is the real trigger a same-project concurrent start boundary rather than generic PID reuse?
4. Should attach-only success ever write `last_ai_state=up` without a valid AI PID?

## Evidence Trail

### Production Symptom
- `fleet-status` correctly reports `sup=none ai=none`
- `live-status` incorrectly reports `last_supervisor_state=up last_ai_state=up last_exit_reason=already_running_attach`
- `.freely/run/ai.pid` is absent
- `.freely/run/workcell-state.env` mtime is 17 minutes after last runtime event

### Timeline
- `2026-03-30 23:00:25 PDT`: Last runtime event (supervisor_cleanup)
- `2026-03-30 23:17:30 PDT`: workcell-state.env rewritten to `running/up/up/already_running_attach`
- No runtime event emitted for this state change

## Related Work

- `I-20260328-0745-A`: Fixed the opposite direction (active PIDs reconcile stale `down` upward)
- This regression is the inverse: persisted state is stale optimistic, needs reconciliation downward

## Commit History

1. `c0af4ed`: Add live-status already-running-attach regression to milestone and create root cause analysis
   - Added candidate to milestone
   - Created root cause analysis document
   - Created minimal repro script
   - Documented write/read contract gap
