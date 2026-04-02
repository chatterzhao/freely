# Brainstorms - 20260401-1831--worker-reactivation-reentry-residual-runtime-gaps

## Context

- source lane: `feature/freely-security-baseline-governance-20260401`
- trigger: finishing `freely-tool-autonomy-policy-materialization-governance` left two runtime tests red after the autonomy-consent and project-local Codex config slice was otherwise green
- failing tests:
  - `docs/system/workspace/scripts/tests/test-freely-chat-worker-reactivation`
  - `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`

## Frozen Evidence

### 1. Worker chat/tui reactivation can still land in attach-reuse without a durable AI child

- `test-freely-chat-worker-reactivation` still fails at:
  - `[FAIL] chat-triggered delegated continuation should reactivate stopped worker runtime`
- local repro evidence from the current worktree showed:
  - `chat-reactivation.log` records `recovered live project supervisor after supervisor.pid drift`
  - then `project runtime/control-plane already up; reusing supervisor pid=...`
  - workcell state later reports:
    - `DESIRED_RUNTIME_STATE="running"`
    - `LAST_SUPERVISOR_STATE="up"`
    - `LAST_AI_STATE="up"`
    - `LAST_EXIT_REASON="already_running_attach"`
  - but `.freely/run/ai.pid` is still absent

This is not the old manager-only false attach bug. `I-20260330-2318-A` intentionally preserved worker attach reuse when AI state is missing. Current evidence shows that contract is still too optimistic for worker reactivation after `operator_stop`.

### 2. Active-worker local continuation reentry contract is still under-specified

- `test-freely-interruption-direct-answer` still fails at:
  - `[FAIL] delegated continuation should interrupt current ai pid for local re-entry`
- current runtime path only calls `request_local_continuation_reentry()` when delegated worker launch sees both:
  - a project-owned worker supervisor PID
  - a project-owned AI PID
- the current test fixture seeds only `.freely/run/ai.pid` with a plain `sleep` PID, which no longer satisfies `valid_ai_pid_for_project()`
- a quick fixture experiment that upgraded the PID shape toward project-owned `codex exec` still did not produce local reentry, so the residual is not just a stale test literal

This means the completed owner `I-20260322-0412` is no longer sufficient as written. Either the runtime contract for "active worker" has narrowed and the test/progress claims need to follow it, or there is still a real reentry gap even when runtime truth looks active enough.

## What Is Already True

- the current autonomy-consent / project-local Codex config work did not introduce these two failures
- the following validation is already green in this lane:
  - `bash docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
  - `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
  - `bash docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
  - `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-retained-continuation`
  - `./bin/governance-check`
- existing completed workspace-routing owners already touch this family:
  - `I-20260321-1706` chat-triggered worker runtime reactivation
  - `I-20260322-0412` worker active reentry for manager-delegated continuation
  - `I-20260330-2318-A` manager attach reuse missing-AI repair

## Current Best Hypothesis

1. worker attach reuse remains too permissive after `operator_stop`:
   - a still-live worker supervisor can be reused without a confirmed or quickly-materialized AI child
   - `start_project_runtime()` then writes optimistic `already_running_attach` truth and returns
   - chat/tui caller sees neither a restarted worker loop nor a durable `ai.pid`
2. active-worker local reentry still depends on a stricter "runtime-owned active worker" shape than the surviving test fixture or old progress docs describe
3. these should be treated as one residual runtime family because both defects sit on the worker-side reactivation/reentry boundary, not on the new security/autonomy policy materialization lane

## Open Questions

1. For worker projects, when is missing-AI attach reuse still valid, and when must runtime kill/restart instead of returning `already_running_attach`?
2. Should worker reactivation after `operator_stop` require `ai_pid_state=confirmed_running`, or only require that the reused supervisor proves it can materialize a fresh AI child within a bounded window?
3. What is the canonical minimum truth for `request_local_continuation_reentry()`:
   - live AI only
   - live supervisor + live AI
   - or a broader runtime-owned active-worker predicate?
4. Do the completed verification artifacts for `I-20260321-1706` / `I-20260322-0412` need to be narrowed or superseded once this residual owner lands?

## Boundary

- do not keep expanding `freely-security-baseline-governance` to absorb runtime worker semantics
- carry this as workspace-routing-foundation follow-up
- keep the owner narrow:
  - worker attach-reuse reactivation truth
  - active-worker local continuation reentry truth
- do not reopen manager-only attach repair unless the worker residual proves that manager and worker attach gates must be unified
