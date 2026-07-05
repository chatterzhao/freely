# Progress - Live-status Already-Running-Attach Regression

## Metadata
- candidate_id: C-20260330-2318-A
- phase: needs_research
- worktree: 20260330-231827-feature-live-status-already-running-attach-regression
- branch: feature/live-status-already-running-attach-regression-20260330-231827
- started: 2026-03-31

## Current Status

**Phase**: Trigger proven from real dogfood evidence; narrow attach-gating repair in progress

**Last Update**: 2026-04-01T08:20:00-07:00

## Work Completed

### 1. Candidate Promotion to Milestone ✓
- Added `C-20260330-2318-A` to `M-20260306-workspace-routing-foundation` candidate queue
- Status: `needs_research`
- Priority: P1

### 2. Root Cause Analysis Complete ✓
- Created `docs/B1-docs/20260330-2318--live-status-already-running-attach-regression/root-cause-analysis.md`
- Confirmed the optimistic attach write path in `start_project_runtime()`
- Confirmed `live-status` only reconciles upward and does not downgrade stale optimistic state
- Reframed earlier "PID reuse / stale pid file" claims as unproven hypotheses
- Analyzed production evidence showing 17-minute gap between cleanup and false-positive write
- Identified three key code paths and four potential design directions

### 3. Focused Repro Attempt ✓
- Created `test-live-status-attach-false-positive-repro` script
- Attempted to reproduce the false-positive by exercising real `runtime/freely` attach path
- Encountered complexity in setting up isolated test project with full Freely structure
- Decision at the time: Defer complex repro harness until next real occurrence provides more trigger evidence

### 4. Code Path Analysis ✓
Identified three key functions in the problematic path:
- `start_project_runtime()` (line 5435): Writes optimistic state without verification
- `ensure_no_active_supervisor_conflict()` (line 5394): Returns 10 for attach success
- `resolve_active_supervisor_pid_for_start()` (line 5370): Resolves PID from file or discovery

### 5. Existing Contract Coverage Verified ✓
- `test-freely-project-command-semantics` passes and confirms attach reuse is an intentional contract
- `test-freely-status-pid-ownership` passes and confirms stale foreign supervisor PIDs are filtered elsewhere

### 6. Real Trigger Proven on `develop` ✓
- Live validation of the multi-tool fallback lane produced a valid `tool_auto_switch_selected previous_tool=kiro-cli active_tool=codex`
- Immediately after that valid selection, manager bootstrap emitted `supervisor_attach_reuse ... ai_pid_state=missing role_hint=manager`
- `live-status` then showed the false optimistic truth: `desired_runtime_state=running`, `last_supervisor_state=up`, `last_ai_state=up`, `last_exit_reason=already_running_attach`
- This proves the regression is not generic PID reuse; it is the manager attach-reuse path accepting a live supervisor without a confirmed running AI child

### 7. Narrow Repair Chosen ✓
- Keep worker attach-reuse semantics unchanged
- Restrict manager attach reuse so it only succeeds when `ai_pid_state=confirmed_running`
- When manager sees `ai_pid_state=missing` or stale, fall back to project-local repair instead of writing optimistic `already_running_attach`
- Add focused regression coverage in `test-freely-project-command-semantics`

## Root Causes Identified

1. **Optimistic State Write**: Attach success writes `up/up` without any stronger health/observability gate
2. **One-Way Reconciliation**: `live-status` intentionally preserves historical state when no live PID is found
3. **No Runtime Event**: Attach-only path doesn't emit runtime event for observability

## Next Steps

### Immediate (Before Promotion to Issue)
1. **Finish Focused Regression**: Keep worker attach-reuse coverage green while the manager-only missing-AI repair-path test lands
2. **Drive the Materialized Owner**: The candidate is now materialized as `I-20260330-2318-A`; keep execution and verification on that issue chain
3. **Rerun Live Validation**: Validate on `develop` that manager no longer lands in `already_running_attach` after the valid fallback handoff

## Promotion Gate

This candidate should be promoted to a milestone-owned issue when:
- [x] A focused repro or equivalent real trigger demonstrates the exact attach path that writes false-positive state
- [x] The trigger mechanism is confirmed as manager attach reuse with `ai_pid_state!=confirmed_running`
- [x] A narrow fix strategy is selected against the confirmed trigger
- [ ] The fix preserves existing valid worker attach-reuse contract and passes regression tests

## Blocker

Current blocker: **Repair still needs merge and one protected live verification pass**

## Fix Proposal

Chosen fix:

1. **Manager-only write-side hardening**
   - Gate manager attach reuse more strictly
   - Avoid writing `last_ai_state=up` without a confirmed manager AI PID
   - Preserve worker attach reuse so the earlier valid contract does not regress

## Next Actions

### Immediate (Current Session)
- [ ] Build a focused repro that hits the real `start_project_runtime()` attach path
- [x] Distinguish same-project short-window attach from broader PID validation failures
- [x] Decide whether repair belongs in write-side attach semantics, read-side downgrade, or both
- [ ] Keep existing attach and stale-ownership tests green
- [x] Materialize owner issue
- [ ] Rerun live validation

### Follow-up
- [ ] Verify fix prevents regression
- [ ] Ensure existing valid attach cases still work
- [ ] Update documentation for attach semantics
- [ ] Consider if `live-status` should also reconcile `already_running_attach` state

## Open Questions

1. Should `live-status` still treat `already_running_attach` as soft/stale unless current PIDs confirm, even after the manager write-side fix?
2. Should attach-only writes use a different exit reason like `attach_pending_verification`?
3. Are there any non-manager roles besides worker that should share the stricter attach gate?
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
- `2026-04-01 08:03:14 PDT`: `tool_auto_switch_selected previous_tool=kiro-cli active_tool=codex`
- `2026-04-01 08:03:14 PDT`: immediate `supervisor_attach_reuse ... ai_pid_state=missing role_hint=manager`
- `2026-04-01 08:03:xx PDT`: `live-status` again reports `running/up/up/already_running_attach` with no surviving project-owned AI PID

## Related Work

- `I-20260328-0745-A`: Fixed the opposite direction (active PIDs reconcile stale `down` upward)
- This regression is the inverse: persisted state is stale optimistic, needs reconciliation downward

## Commit History

1. `c0af4ed`: Add live-status already-running-attach regression to milestone and create root cause analysis
   - Added candidate to milestone
   - Created root cause analysis document
   - Created minimal repro script
   - Documented write/read contract gap
