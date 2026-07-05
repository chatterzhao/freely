# Brainstorm: runtime-blocked-intake-and-continuity-truth-governance

## Decision

`C-20260404-1545-A` should promote into a dedicated supervision owner. The gap is no longer “do we have a problem”, but “what is the narrow blocked-truth contract when prompt assembly advances but intake claim / continuity materialization does not”.

## Why This

1. Existing network taxonomy already owns classification and bounded retry/cooldown; it does not own intake/continuity truth.
2. Existing bootstrap-continuity materialization owner already closed the startup parser path; this follow-on is about blocked runtime supervision after prompt visibility is recovered.
3. Existing delegated intake absorption owner closes successful manager-owned lifecycle absorption; it does not define what happens when claim/continuity never advances.
4. Latest field evidence combines websocket permission denied, shared slot-switch busy, and local fork exhaustion into one visible false-active pattern: prompts advance while machine-readable supervision truth does not.

## Follow-on Package

The first implementation lane must consume:

1. `issues/runtime-blocked-intake-and-continuity-truth-governance.md`
2. `prd.md`
3. `pre-tests.md`
4. `tasks.md`
5. `docs/B1-docs/raw-20260404/brainstorms.md`
6. `docs/B2-docs/runtime/runtime-network-failure-taxonomy-and-bounded-recovery-governance/issues/runtime-network-failure-taxonomy-and-bounded-recovery-governance.md`
7. `docs/B2-docs/ibm/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`

## Boundary Summary

This owner freezes:

1. when prompt-visible-but-unclaimed supervision becomes a blocked runtime state rather than a generic active loop
2. the minimum machine-readable truth surfaces that must advance:
   - intake state
   - continuity or equivalent blocked handoff artifact
   - live-status / fleet-status blocked reason
3. the current allowed blocked triggers:
   - websocket permission denied
   - slot-switch busy before launch progress
   - local process-capacity exhaustion

This owner does not freeze:

1. generic retry/cooldown policy redesign
2. semantic-loop automation
3. worker-side stall recovery
4. GitHub issue create/sync automation

## Implementation Start Checklist

All of the following must be true before a dev-loop opens:

1. reproduce a prompt-visible-but-unclaimed path in a dedicated worktree or test harness
2. name the blocked truth surfaces to update before touching runtime code
3. keep the first slice limited to blocked-state writeback and status observability
4. keep network classification, slot fallback policy, and generic orchestration behavior unchanged unless a new owner is opened

## Non-Goals

1. no generic watchdog redesign
2. no broad dependency-health scheduler
3. no claim that prompt churn alone equals semantic-loop regression
4. no claim that GitHub issue automation exists today
