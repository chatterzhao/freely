# Brainstorms - 20260413-0420--real-repo-daemon-gap-and-foreground-double-start-regression

## Context

- This pre-brainstorm captures a deeper review of the real Freely self-hosting runtime on `develop`.
- The initial symptom looked like two separate issues:
  - `freely daemon start` could report success even though the real repo later looked stopped
  - a fresh foreground `freely start` could still materialize multiple same-project startup chains
- After repeated bounded restarts, code inspection, history review, and subagent review, the finding is more precise:
  - these are not isolated bugs
  - they are coupled failures inside the same runtime startup model

## Verified Runtime Evidence

### 1. Foreground and daemon both expose the same startup authority gap

- Foreground repro on the real repo showed duplicated same-project startup chains:
  - `2026-04-13T10:59:12Z event=project_start_lock_acquired owner_pid=98824 reason=freely_start`
  - `2026-04-13T10:59:12Z event=supervisor_started supervisor_pid=98824 entrypoint_mode=foreground`
  - `2026-04-13T10:59:14Z event=project_start_lock_acquired owner_pid=1140 reason=freely_start`
  - `2026-04-13T10:59:15Z event=supervisor_started supervisor_pid=1140 entrypoint_mode=foreground`
  - `2026-04-13T10:59:16Z event=ai_launch_begin supervisor_pid=98824`
  - `2026-04-13T10:59:18Z event=ai_launch_begin supervisor_pid=1140`
- Later real-repo daemon runs could return `daemon_status: running`, but the authoritative state files and later observation still converged to stopped or ambiguous startup truth.

### 2. Manager continuity gap is not daemon-only

- Foreground run on `2026-04-13 04:53:46 PDT` showed:
  - `project_start_lock_acquired`
  - `supervisor_started`
  - `ai_launch_begin`
  - no fresh manager continuity from the AI itself during normal startup
- Stop at `2026-04-13 04:55:54 PDT` then materialized fallback continuity:
  - `event=manager_continuity_fallback_materialized`
  - `gap_age_secs=124`
- This proves the AI launched, but startup success was treated as "AI process spawned" rather than "manager handoff materialized".

### 3. Stop cleanup is not fully trustworthy

- A real stop emitted:
  - `forced hard-kill fallback while repairing project manager watchdog during stop: pid=83094`
- `runtime-events.log` also recorded:
  - `event=supervisor_cleanup_stop_marker_preserved ... other_supervisor_pid=59976`
- Combined with later process inspection, this indicates cleanup can preserve stop markers or branch into repair because the runtime believes another same-project supervisor exists when that belief is not authoritative.

### 4. Fake-supervisor validation is reproducible

- A bounded local reproduction created a fake process whose argv looked like:
  - `runtime/freely daemon-run --project /Users/zhaoyu/Downloads/code/my-freely/freely`
- Current runtime helpers accepted it as a real supervisor:
  - `fake_pid:62004`
  - `discovered:62004`
  - `valid:true`
- This is direct proof that current supervisor discovery or validation is too permissive.

## Code-Level Root Cause

### Root Cause A: supervisor identity is inferred from appearance, not runtime-owned authority

- `discover_supervisor_pids()` in `docs/system/workspace/scripts/runtime/freely:1513-1544` scans `ps` output and matches command-line substrings:
  - `runtime/freely start`
  - `runtime/freely daemon-run`
- `valid_supervisor_pid_for_project()` in `.../freely:1601-1604` delegates to `pid_matches_project()` with those same argv expectations.
- This means the runtime can mistake the following for a real supervisor:
  - launcher shells
  - short-lived wrapper processes
  - diagnostic commands
  - a deliberately faked argv process
- Consequences:
  - daemon ready false positives
  - stop-marker preservation based on ghost supervisors
  - attach or repair decisions made against non-authoritative PIDs

### Root Cause B: the start critical section ends before bootstrap truth is durably published

- In `start_project_runtime()` at `.../freely:10055-10220`, the sequence is:
  - acquire project start lock
  - run conflict or attach logic
  - write `supervisor.pid`
  - immediately release the start lock
  - only then append `supervisor_started`
  - only then write workcell state as `running/up/down/starting`
  - only then begin dispatcher or watchdog readiness work
- The key lines are:
  - `echo "$$" >"$sup_pid_file"` at `10181`
  - `release_project_start_lock_for_runtime "$project"` at `10182`
  - `append_runtime_event ... supervisor_started` at `10183-10187`
  - `write_workcell_state ... "starting"` at `10188`
- A later same-project starter therefore sees a vulnerable window where:
  - a `supervisor.pid` exists
  - `ai.pid` may still be absent
  - bootstrap truth is not yet durably published
  - control-plane readiness is not yet settled
- That later starter can still classify the first launch as partial and enter repair or restart instead of bounded attach or wait.

### Root Cause C: startup readiness is approximated as "there is a supervisor PID"

- `wait_for_daemon_supervisor_ready_or_fail()` in `.../freely:10598-10617` loops until `manager_supervisor_pid_for_project()` returns any PID.
- `manager_supervisor_pid_for_project()` at `.../freely:8495-8505` trusts either:
  - `supervisor.pid` if `valid_supervisor_pid_for_project()` accepts it
  - or `discover_supervisor_pid()` from process inspection
- This means daemon ready is currently defined as:
  - "some PID looks like a supervisor for this project"
- It is not defined as:
  - "the current launch has published authoritative startup truth"
- That is why daemon control-plane behavior and foreground attach behavior both drift in the same direction.

### Root Cause D: manager continuity is only a prompt requirement, not a runtime launch invariant

- `start-lead-agent.sh:200-227` explicitly requires the manager to materialize runtime-consumable artifacts and at least one continuity file.
- But the runtime does not require continuity materialization before it considers launch successful.
- The current runtime contract is effectively:
  - AI spawn succeeded
  - therefore runtime start succeeded
  - if continuity is still missing later, repair it on stop
- The fallback logic at `.../freely:1328-1435` makes the gap visible and repairs it, but does not close the normal-path startup contract.

## Why The Existing Guards Did Not Close The Problem

### `project_bootstrap_launch_in_flight()` is too late in the lifecycle

- `project_bootstrap_launch_in_flight()` at `.../freely:8445-8469` requires:
  - live supervisor PID
  - missing AI PID
  - `DESIRED_RUNTIME_STATE=running`
  - `LAST_EXIT_REASON=starting`
  - grace window still active
- That check is useful, but it only works after the `starting` truth is already durably present.
- The race window exists earlier than that publication boundary.
- So the current repair narrows one bootstrap ambiguity, but does not make bootstrap authority atomic.

### Attach and repair logic still depend on partial truth

- `ensure_no_active_supervisor_conflict()` at `.../freely:9999-10037` attempts to reuse a healthy runtime when attach is possible.
- The reuse path is still forced to decide based on:
  - current PID files
  - current process inspection
  - bootstrap grace heuristic
  - dispatcher or watchdog readiness probes
- Because startup truth is not yet authoritative when the lock is released, the attach path is asked to reason about a startup that is only half published.

## Historical Change Review

### `3ef222ec` - serialize same-project runtime start and align status truth

- This change introduced the project start lock and improved same-project attach behavior.
- It was directionally correct.
- It did not extend the lock boundary through durable startup truth publication.
- The remaining race is precisely the gap between `supervisor.pid` publication and later `supervisor_started` or `workcell-state=starting` publication.

### `7523cd3d` - tighten same-project supervisor stop followthrough

- This change expanded stop followthrough from singular supervisor handling to plural discovery.
- That is only safe if supervisor discovery is authoritative.
- Because current discovery is argv-based, this change widened the impact of ghost-supervisor false positives into stop-marker preservation and broader cleanup behavior.

### `1d1b33c0` - avoid duplicate manager launch during degraded bootstrap

- This change added degraded bootstrap grace behavior through `project_bootstrap_launch_in_flight_from_unverified_supervisor_hint()`.
- It reduced one specific double-launch path.
- It did not solve:
  - supervisor identity
  - early lock release
  - authoritative startup publication

### `9ed550ad` - fix manager continuity gap observability

- This change did not create the continuity bug.
- It surfaced the gap and added fallback repair materialization.
- It proves the runtime already knew continuity could go missing after startup.
- It does not change the normal-path definition of launch success.

### `f379de15` - add explicit daemon runtime control plane

- This change made daemon entrypoints first-class.
- It inherited the same supervisor identity and readiness assumptions.
- As a result, daemon start widened the externally visible surface area of the existing startup-authority bug.

## Final Diagnosis

- This is not one bug.
- It is a three-layer model problem:
  - launch identity is heuristic, not runtime-owned
  - bootstrap authority is published too late
  - manager-ready is not part of the startup contract
- The runtime currently approximates all of these with one weaker idea:
  - "there exists a PID that looks like the project supervisor, and the AI process has started"
- That approximation is no longer sufficient for self-hosted Freely startup behavior.

## Product-Intent Review

### 1. The current startup model violates Freely's product identity

- `docs/PROJECT_INTENT.md` defines Freely as a self-hosting autonomous loop runner:
  - AI takes the owner role after startup
  - the loop should continue until explicit stop or a major unrecoverable incident
  - runtime exceptions discovered during dogfooding should be turned into reusable Freely capability findings
- `docs/CONSTITUTION.md` also fixes several engineering principles that are directly relevant here:
  - status must stay explicit and inspectable on disk
  - deterministic behavior is preferred over hidden magic
  - each running loop instance must have isolated PID or session or state truth
- The current startup implementation violates that contract in two ways:
  - it cannot authoritatively answer which process is the current runtime owner
  - it can report startup success before the owner loop has materialized its first required handoff artifact

### 2. This is not just a daemon bug or a foreground bug

- `docs/B1-docs/20260413-0208--foreground-background-runtime-entrypoint-semantics/brainstorms.md` already established a product-level distinction:
  - `freely start` is foreground-attached runtime
  - `freely daemon start` is the explicit detached runtime contract
- That entrypoint distinction is still correct.
- The new finding is deeper:
  - both entrypoints are currently backed by the same weak startup authority model
  - so the product has two command surfaces, but not two trustworthy runtime contracts
- In other words, the bug is not that Freely supports both foreground and background.
- The bug is that both modes currently depend on PID resemblance instead of launch authority.

### 3. The runtime is collapsing semantic surfaces that Freely intends to keep separate

- `PROJECT_INTENT.md` explicitly separates:
  - Freely core
  - semantic surfaces such as `start`, `chat`, `live-status`, `fleet-status`
  - external AI tooling such as `codex`
- The startup code currently blurs these boundaries:
  - process inspection is used as if it were the source of truth for ownership
  - AI process spawn is treated as if it were equivalent to manager-ready
  - status projection is asked to stand in for launch identity
- This is the opposite of the intended Freely shape.
- In Freely's own architecture, runtime should own:
  - authoritative launch identity
  - startup ordering
  - status publication
  - recovery boundaries
- External AI tooling should only supply execution of the manager or worker task, not define runtime truth.

### 4. The current behavior weakens the dogfooding loop

- Freely's intent is not merely to run an AI process.
- It is to run an autonomous ownership loop that can continue from evidence and write back new evidence.
- When startup succeeds without a first manager continuity, the product loses the minimum handoff surface that lets the next round:
  - resume ownership
  - audit prior decisions
  - recover after interruption
- That means the failure is not just "continuity file delayed".
- It is a failure of Freely's self-hosting control loop to materialize its own first-cycle governance artifact.

### 5. The current model also conflicts with CLI-first and unified-status principles

- `CONSTITUTION.md` requires CLI-first behavior and explicit status on disk.
- The product-level consequence of the current bug is:
  - `daemon start` can say `running`
  - while `live-status` and runtime events do not yet support that claim as authoritative truth
- That is precisely the kind of hidden magic or ambiguous state the constitution rejects.
- A valid Freely runtime contract should let every shell consume the same truth:
  - CLI
  - future TUI
  - future GUI
- If daemon readiness depends on argv heuristics, UI shells would inherit the same ambiguity.

### 6. The implementation must preserve product semantics while fixing the runtime

- The right repair is not to collapse foreground and daemon into one mode.
- It is not to move product truth into prompt wording either.
- The repair needs to preserve the existing product intent:
  - foreground mode remains attachable and observable
  - daemon mode remains explicit detached runtime
  - both modes share the same authoritative launch identity and status model
  - manager continuity becomes part of the runtime-governed startup contract, not a best-effort prompt side effect

## Three-Loop And Autonomy Review

### 1. This bug damages the outer `auto-loop`, not only local startup mechanics

- `docs/PROJECT_INTENT.md` and `docs/system/workspace/three-loop-capability-lifecycle.md` define:
  - `auto-loop` as the outer orchestration and governance loop
  - `doc-loop` and `dev-loop` as sibling execution loops
  - `verification`, `recovery`, and `cleanup` as governance routes, not separate loops
- In that model, runtime startup is not just process boot.
- It is the entry gate that allows the outer loop to:
  - patrol
  - classify route
  - materialize continuity
  - delegate workers
  - re-enter after interruption
- If startup truth is ambiguous, the `auto-loop` cannot reliably know whether it is supervising:
  - one authoritative manager
  - two competing startups
  - or no valid startup at all

### 2. Missing manager continuity is a broken artifact chain, not a cosmetic delay

- The three-loop lifecycle document explicitly treats the runtime artifact chain as:
  - `signal -> resolution -> continuity -> worker prompt -> canonical writeback`
- It also states that missing one link makes the downstream loop unable to continue safely.
- In this incident, the manager continuity was not written on the normal path.
- That means the first `auto-loop` handoff artifact was absent.
- So the failure is not merely "the manager was slow".
- It is that Freely failed to materialize the artifact chain required for the next autonomous round.

### 3. The startup bug weakens recovery and resumption semantics

- The constitution and project intent both require recovery-first continuity.
- The three-loop lifecycle further requires that after a runtime interruption, the system can return through:
  - recovery route
  - back into `auto-loop`
  - then back into `doc-loop` or `dev-loop`
- That only works if the runtime can trust:
  - who the current launch owner is
  - which continuity belongs to that launch
  - whether the prior round reached a durable restart point
- When stop fallback creates the first continuity only at teardown time, the system loses:
  - a trustworthy normal-path restart point
  - a clean distinction between successful startup and cleanup repair

### 4. The current defect encourages dead-loop or thrash patterns the product explicitly rejects

- The three-loop lifecycle treats repeated AI restarts, abnormal churn, and prompt or continuity drift as outer-loop supervision signals.
- This startup model currently makes those signals harder to classify because:
  - duplicate startups can be created during bootstrap
  - fake or ghost supervisors can be mistaken for real ownership
  - manager-ready and AI-spawn are conflated
- That raises the risk of the exact anti-pattern Freely is meant to prevent:
  - the system appears active
  - but the outer loop lacks a stable owner, stable route, and stable handoff
- In product terms, that is autonomy theater rather than reliable autonomy.

### 5. The repair must strengthen loop boundaries, not just patch startup symptoms

- For `auto-loop`, the repair must provide a single authoritative launch owner and a trustworthy startup phase.
- For `doc-loop`, the repair must ensure runtime anomalies still land as canonical research or issue material rather than vanishing into logs.
- For `dev-loop`, the repair must provide a durable manager continuity and restart point so implementation work can resume from evidence.
- For recovery, the repair must let the system distinguish:
  - normal startup
  - degraded startup still in progress
  - failed startup requiring repair
  - clean stop after a valid launch

## Design Direction

### 1. Separate launch identity from status projection

- Introduce a runtime-owned launch record for the current authoritative start.
- Suggested fields:
  - `launch_id`
  - `project_root`
  - `entrypoint_mode`
  - `supervisor_pid`
  - `started_at`
  - `bootstrap_phase`
- Suggested storage surface:
  - `.freely/run/startup-truth.env`
  - or `.freely/run/supervisor.identity`
- `workcell-state.env` should remain a status projection, not the only bootstrap truth source.

### 2. Extend the start critical section through authoritative publication

- The project start lock should not be released immediately after writing `supervisor.pid`.
- Minimum publication boundary before unlock:
  - current launch identity written
  - `supervisor_started` event appended for the current launch
  - workcell state written as startup in progress for that same launch
- Better boundary if feasible:
  - dispatcher or watchdog readiness claims written before later starters may attach

### 3. Redefine daemon ready as current-launch truth, not PID presence

- `daemon start` should only report `running` after:
  - the current launch has a stable `launch_id`
  - authoritative startup truth has been published
  - the observed supervisor PID belongs to that launch
- PID discovery may still be useful for repair or diagnostics, but not as the primary ready contract.

### 4. Treat manager continuity as a launch contract, not only a prompt convention

- Runtime should seed the expected continuity contract for the current launch.
- One pragmatic shape:
  - runtime allocates the expected continuity path
  - runtime writes a continuity claim or stub bound to the current `launch_id`
  - AI enriches the semantic body
- Stop-time fallback remains valuable as repair, but should no longer be the normal way continuity first materializes.

## Recommended Implementation Split

### Lane 1: identity and authority

- Introduce `launch_id`
- Introduce startup truth or launch record
- Downgrade argv scanning to diagnostics or stale-process cleanup
- Make `valid_supervisor_pid_for_project()` require launch-owned identity, not just argv or cwd resemblance

### Lane 2: bootstrap serialization and readiness

- Move the lock boundary
- Rework `ensure_no_active_supervisor_conflict()`
- Rework `wait_for_daemon_supervisor_ready_or_fail()`
- Make attach, wait, or repair decisions against the current launch record

### Lane 3: manager continuity contract

- Seed continuity claim or stub from runtime
- Bind continuity expectations to `launch_id`
- Redefine manager-ready and launch-ready separately
- Keep fallback continuity as repair-only

## Success Criteria

- The fix should not be considered done unless all of the following are true:
  - a fake argv process no longer passes supervisor validation
  - foreground and daemon both pass repeated bounded real-repo start or stop cycles
  - same-project concurrent starts produce exactly one authoritative launch
  - `daemon start` does not return `running` until current-launch startup truth is published
  - `freely stop` does not preserve stop markers unless another validated launch truly exists
  - manager continuity is produced on the normal startup path within a bounded SLA
  - `live-status`, `fleet-status`, and `runtime-events.log` agree on the current launch identity and state

## Product-Level Acceptance

- In addition to the technical checks above, the repair should only be considered product-correct if all of the following are true:
  - `freely start` and `freely daemon start` remain distinct semantic surfaces, but converge on the same launch authority model
  - runtime-owned state, not external AI tool behavior, decides whether startup is authoritative
  - a successful manager startup produces a durable first-cycle handoff artifact on the normal path
  - status shown through CLI is suitable to be reused later by TUI or GUI without inventing a parallel truth model
  - the repair strengthens self-hosting recovery rather than merely hiding the symptom behind fallback cleanup
  - the outer `auto-loop` can reliably tell whether it should patrol, recover, reroute, or stop, without guessing from PID resemblance
  - the runtime artifact chain can carry a clean `signal -> continuity -> execution -> writeback` handoff through interruption and restart

## Subagent Review Summary

- Independent review converged on the same split:
  - supervisor identity must be separated from readiness
  - bootstrap truth publication needs its own explicit phase
  - manager continuity must move from soft prompt expectation into runtime contract
- The exact implementation details can vary, but the fix must preserve that separation.

## Relationship To Existing Research Worktree

- The current research worktree diagnosis was directionally right about the foreground double-start regression.
- Its daemon conclusion needs to be tightened:
  - this is not only a "coverage gap"
  - there is also a concrete daemon-facing bug in supervisor identity or ready determination
- Therefore the right next step is not to merge a giant mixed fix.
- The right next step is to carry this research into a split implementation plan with explicit authority boundaries.
