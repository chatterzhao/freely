# Brainstorms - 20260421-1530--scan-owned-patrol-inventory-and-live-status-on-demand-reading

- date: `2026-04-21`
- status: `pre-brainstorm`
- source: `real runtime replay plus live-status / scan semantic boundary audit`

## Context

This round started from a concrete ambiguity inside Freely self-host:

1. `task-source-scan` already exists and is intentionally wired into manager startup / idle / replan patrol.
2. `live-status` already exists and is intentionally the current-state runtime surface.
3. the implementation still carried several prompt lookup paths that treated "latest prompt in run dir" as a broad status anchor.
4. a real protected-root repo replay showed the run dir has grown large enough that accidental "scan history to infer state" logic is both semantically weak and operationally wasteful:
   - `.freely/run` file count: `9342`
   - `prompt-*.txt` count: `6271`
   - `manager-continuity-*.md` count: `3009`
   - total size: `289984512` bytes

The user challenge in this round is narrower than "make status faster":

- decide what `scan` is actually for
- decide what `live-status` is actually for
- decide whether scanning prompt history can ever satisfy `live-status`
- decide how the system should know which files to read without maintaining a heavy prompt lifecycle index

## Evidence Observed In This Round

### 1. Existing three-loop truth already positions `scan` as patrol, not runtime truth

`docs/system/workspace/three-loop-capability-lifecycle.md` states:

1. patrol-driven source intake runs `freely task-source-scan --json`
2. runtime then provides the latest scan JSON to the manager as standing-source first-hop input
3. manager still has to read actual truth and route into doc-loop / dev-loop / recovery

So the authoritative lifecycle already says:

- `scan` is inventory input
- `scan` is not completion proof
- `scan` is not a replacement for runtime truth

### 2. Existing `live-status` owner already positions it as current-state plane

Older observation docs and verification artifacts freeze `live-status` as:

- canonical current-state surface
- first-hop watchdog / manager supervision panel
- deep-ref launcher into prompt / continuity / logs / intake / resolution

That means `live-status` was never supposed to become a global unresolved-work scanner.

### 3. Real runtime tests still confirm the current patrol trigger contract

This worktree reran the bounded scan tests successfully:

- `test-freely-manager-prompt-includes-milestone-patrol-seed`
- `test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`
- `test-freely-manager-prompt-suppresses-broad-patrol-while-worker-active`

These results confirm the current design intent remains valid:

1. startup / idle / replan may use scan
2. active worker rounds should suppress broad patrol
3. scan is already bounded by trigger conditions rather than every-cycle

### 4. Prompt-history lookup is semantically weaker than the system now needs

Manager runtime is no longer a single-threaded "one latest prompt means current truth" system:

1. manager may have its own current prompt
2. manager may have multiple active worker prompts at the same time
3. queued worker prompts and frozen worker prompts can coexist
4. old prompt files remain in history after they are consumed or superseded

Therefore prompt history alone cannot answer:

- which prompt is the current manager execution contract
- which prompts are active worker obligations
- which prompts are only historical residue
- which unresolved surfaces still require follow-up

### 5. A heavy prompt lifecycle index is not the right fix

The obvious opposite design would be "create a full prompt lifecycle ledger and keep it perfectly updated".

This is too heavy for the present boundary because it would need to solve:

1. active / queued / frozen / consumed / retired semantics for every prompt
2. crash-safe updates across manager launch, worker launch, closeout, and recovery
3. stale reference cleanup across deleted worktrees and old continuities
4. compatibility across startup self-heal, restart, and replay

That cost is not justified if the system only needs:

- explicit anchors for current execution contracts
- a patrol inventory for unresolved surfaces
- on-demand reading of referenced files

### 6. Startup itself is not the place for broad semantic expansion

Real runtime replay in this round confirmed a bounded startup shape on an isolated repo:

1. around five seconds after `daemon start`, only control-plane runtime artifacts existed
2. around twenty seconds after start, the visible manager-owned artifacts were still narrow:
   - `ai.pid`
   - `session-state.env`
   - one startup prompt
   - one `manager-task-source-scan-latest.json`
3. prompt size and scan size were modest in that isolated replay:
   - prompt bytes: `18658`
   - prompt lines: `196`
   - scan bytes: `1719`
   - scan lines: `56`

So the main startup risk is not that startup always does "too much work".

The main risk is that later status / routing surfaces may keep re-reading historical artifacts in semantically weak ways, or may expand patrol inventory into deep content reads when they should remain on-demand.

## Core Diagnosis

The real mistake is not merely "directory scanning is a bit slow".

The real mistake is mixing two different questions:

1. runtime question:
   - "what is the system doing right now?"
2. patrol question:
   - "what still looks unresolved and may need a next hop?"

Prompt-directory lookup only partially answers the first question and answers the second question badly.

`scan` answers the second question well enough as advisory inventory, but does not answer the first question.

So the architecture should split these questions cleanly instead of making one surface guess the other.

## Proposed Contract

### 1. `scan` becomes an explicit patrol inventory owner

`scan` should remain a standalone method and artifact:

- explicit operator/pre-research action may run it
- `auto-loop` may trigger it at bounded startup / idle / replan conditions
- it produces unresolved patrol inventory, not runtime truth

Its primary job is:

1. find unresolved surfaces
2. classify them by kind
3. point to the canonical file or evidence path to inspect next
4. provide a bounded top-level inventory to the manager

### 2. `live-status` remains a current-state plane

`live-status` should answer:

1. is runtime up / down / degraded / blocked
2. which role is active
3. which current manager prompt is the active execution contract
4. what handoff / continuity / resolution truth is active
5. which active / queued / frozen worker prompt surfaces are known from runtime anchors

It should not try to derive "all unresolved work" by scanning prompt history.

### 3. unresolved follow-up in `live-status` should come from `scan`, not prompt history

When `live-status` wants to surface unresolved follow-up, the flow should be:

1. read runtime truth anchors first
2. load latest scan inventory summary if present
3. summarize unresolved items by kind / count / top refs
4. only inspect the referenced files on demand

That means `live-status` can show:

- current-state truth
- plus advisory unresolved inventory summary

without pretending that prompt history itself is the unresolved-work source of truth.

### 4. file reading should be reference-driven and on-demand

The system should not answer broad questions by scanning "whatever newest file exists".

Instead:

1. runtime anchor says which current-state files matter now
2. scan inventory says which unresolved surfaces are open
3. each unresolved item carries the file path or evidence path to inspect
4. status / manager / pre-research flows then read only those referenced files

This is the lighter alternative to a global lifecycle index.

### 5. startup should stop at inventory, not full semantic expansion

Startup should be allowed to do only the minimum needed to hand the system into a lawful manager round:

1. start control-plane processes
2. publish current runtime anchors
3. create the current manager execution contract if needed
4. regenerate scan only when the idle/replan trigger contract says it should
5. stop at unresolved inventory summary

Startup should not, on the hot path, do all of the following:

1. walk every unresolved doc deeply
2. expand every referenced progress / milestone / pre-brainstorm body
3. reconstruct every historical prompt relationship
4. infer unresolved truth from prompt history

Those belong to later manager reasoning or operator inspection, driven by references.

### 6. capability preservation is mandatory

This architecture change is only acceptable if Freely keeps all currently valuable capabilities that already exist across scan, live-status, manager supervision, and worker launch truth.

The redesign must preserve at least these user-visible abilities:

1. manager can still use `task-source-scan` as a bounded startup / idle / replan patrol seed
2. `live-status` still remains the first-hop current-state supervision surface
3. `live-status` still exposes prompt / continuity / intake / resolution deep refs
4. manager can still see worker-lane truth from runtime anchors rather than losing visibility in the name of simplification
5. startup / self-heal / runtime observation behaviors already covered by existing owners and tests must not regress

So the target is not "simpler architecture at any cost".

The target is "clearer ownership and cheaper reads without reducing existing supervision and routing power".

## Minimal Data Model

### Runtime truth anchors

The minimal runtime-owned anchor set should remain:

- `workcell-state.env`
- `session-state.env`
- `manager-worker-launch-state.env`
- continuity / handoff / resolution artifacts
- current manager prompt anchor

These answer "what is active now".

### Scan inventory record

The minimal scan-owned item model should answer "what still looks unresolved":

- `generated_at`
- `scan_reason`
- `scope`
- `unresolved_items[]`

Each `unresolved_item` should minimally include:

- `kind`
- `path`
- `status_reason`
- `evidence`
- `priority`
- `needs_followup`
- `suggested_reader`

This is intentionally lighter than a full prompt lifecycle ledger.

### Prompt metadata role

Prompt files may still carry useful metadata such as:

- intent kind
- target worktree
- owner issue
- expected continuity

But prompt metadata is only read when:

1. runtime anchors already point at a current prompt, or
2. a scan item explicitly points at a prompt-related unresolved surface

Prompt files are not the general unresolved-work index.

### Compatibility constraint

Any future refactor must stay compatible with existing observation and patrol consumers:

1. `manager-agent.md`
2. `start-lead-agent.sh`
3. `context-source-skill`
4. watchdog / supervision skills
5. runtime self-heal and startup owners

If a field is renamed or narrowed, compatibility must be staged rather than silently broken.

## Why This Is Better Than Prompt Directory Scanning

### Semantics

Reference-driven reading is more correct because it distinguishes:

1. current manager execution contract
2. active worker prompt surfaces
3. queued / frozen worker prompt surfaces
4. unresolved non-prompt surfaces such as milestone / progress / pre-brainstorm

Prompt-directory scanning collapses all four into one guessed "latest prompt".

### Performance

This round's local timings on the protected-root machine showed:

1. filename-based prompt lookup across the large run dir is not catastrophic by itself
2. per-file `mtime` scanning is much heavier and not suitable as a hot path
3. the real win is not "faster scanning algorithm", but avoiding unnecessary history scans on status hot paths at all

So the target is not micro-optimization for its own sake. The target is eliminating semantically weak repeated work.

### Startup weight

This boundary also clarifies the "is startup too heavy?" question:

1. bounded startup itself is acceptable when it limits itself to control-plane launch plus scan inventory publication
2. startup becomes too heavy only when patrol discovery is mixed with full semantic expansion or historical prompt inference
3. the right fix is architectural narrowing, not a faster version of broad startup scanning

The preferred startup stack is therefore:

1. runtime anchors
2. optional bounded scan inventory
3. manager round
4. on-demand reads of referenced files

not:

1. runtime anchors
2. deep scan of every unresolved file body
3. prompt-history reconstruction
4. synthetic status inference

## Refactor Safety Plan

This boundary should not be implemented as a one-shot rewrite. The safer path is staged replacement with explicit anti-regression checkpoints.

### Stage 1: stabilize current anchors without changing higher-level semantics

Goal:

1. keep current `live-status` output shape working
2. make prompt lookup prefer explicit runtime anchors where available
3. avoid broad prompt-history inference on hot paths

Safety check:

1. existing `live-status` tests still pass
2. daemon detach/shared-status tests still pass
3. startup self-heal tests still pass

### Stage 2: introduce typed scan-summary consumption without removing old deep refs

Goal:

1. let `live-status` read latest scan summary as advisory unresolved inventory
2. keep all current deep refs intact
3. do not yet remove old prompt-derived fields if downstream docs or skills still reference them

Safety check:

1. bounded scan-trigger regressions still pass
2. manager supervision docs still remain truthful
3. scan summary never overrides runtime truth

### Stage 3: split ambiguous fields into explicit current-state names

Goal:

1. replace ambiguous `latest_prompt_file` semantics with explicit fields such as current manager prompt and worker prompt groups
2. preserve backward compatibility during transition, either by dual-writing fields or by updating all direct consumers in one bounded owner

Safety check:

1. `manager-agent` and `start-lead-agent` instructions stay aligned
2. status readers do not lose visibility into active / queued / frozen worker lanes
3. fleet / watchdog surfaces remain consistent with live-status

### Stage 4: only then consider pruning legacy fallback paths

Goal:

1. remove old prompt-history-derived fields only after direct consumers and tests no longer depend on them

Safety check:

1. no current-state capability disappears
2. no patrol capability disappears
3. no startup / recovery owner loses required evidence

## Anti-Regression Requirements

Any follow-on owner implementing this design should treat the following as non-negotiable regression bars.

### Observation capability must not drop

The redesign must not remove:

1. prompt excerpt visibility
2. continuity excerpt visibility
3. deep refs to prompt / cycle log / jsonl / intake / resolution
4. runtime self-heal read-path behavior
5. current worker-lane visibility already sourced from manager launch state and continuity

### Patrol capability must not drop

The redesign must not remove:

1. startup patrol seed generation
2. idle-after-continuity scan regeneration
3. active-worker suppression of broad patrol
4. structured scan input for manager routing

### Recovery and supervision capability must not drop

The redesign must not break:

1. manager first-hop supervision protocol
2. watchdog current-state inspection
3. startup self-heal status readability
4. existing deep-ref-based operator debugging flows

### Cross-platform stability

Any design centered on `mtime` scanning becomes more fragile across:

- macOS / BSD `stat -f %m`
- Linux `stat -c %Y`
- Windows / PowerShell `LastWriteTime`

and across different filesystem timestamp precision / copy / sync behavior.

Reference-driven reading avoids making `mtime` semantics the control-plane truth.

## New Success Criteria

This research slice is only complete if all of the following are frozen clearly.

### 1. Ownership boundary is explicit

The pre-research must clearly state:

1. `scan` owns patrol inventory
2. `live-status` owns current-state observation
3. neither one is allowed to silently impersonate the other

### 2. Reading strategy is explicit

The pre-research must clearly state:

1. runtime truth uses anchors
2. unresolved follow-up uses scan inventory
3. file inspection is reference-driven and on-demand
4. prompt-directory history is only fallback, not primary semantics

### 3. Prompt semantics are narrowed correctly

The pre-research must clearly state:

1. prompts remain execution contracts
2. prompts are not the global unresolved-work index
3. multiple worker prompts can coexist, so "latest prompt" is not a complete status model

### 4. Heavy-index rejection is justified

The pre-research must clearly state why Freely should not, in this slice, introduce a heavy prompt lifecycle index.

### 5. Real evidence is anchored

The pre-research must anchor its claims in real repo/runtime evidence from this round:

1. passing bounded scan-trigger tests
2. current-state `live-status` contract from existing owners
3. large protected-root run-dir scale
4. the anchor-based prompt lookup fix lane already proven by focused regression
5. isolated-repo startup evidence showing startup output remains bounded when the architecture stops at inventory rather than deep expansion
6. existing docs and tests showing `live-status` and `task-source-scan` already have separate owners that must both survive the refactor

### 6. daemon-start autonomous completion remains a required product bar

The architecture is not acceptable if it only preserves observability while weakening autonomous execution.

So any follow-on implementation owner must also prove:

1. after `daemon start`, Freely can still lawfully choose a next task
2. the chosen task still routes through the proper Freely contracts rather than an ad hoc shortcut
3. completion still follows existing Freely norms for doc-loop / dev-loop / verification / closeout
4. the redesign does not strand the system at "startup succeeded and scan exists" without a standards-compliant path to finished work

In other words, the system must preserve:

1. bounded startup
2. correct patrol inventory
3. correct current-state observation
4. successful autonomous task completion under existing Freely governance

### 7. worktree closeout is part of the success standard

This slice is not complete if the design is frozen but the execution lane remains half-open.

So completion also requires:

1. the active worktree contains only in-scope changes for this slice
2. focused regressions and supporting checks have been rerun after the final edits
3. the lane can return to a clean closeout state rather than ending with unresolved local drift

That means the final bar is not only "the design is right".

It is also "the worktree can be lawfully closed with evidence".

## Recommended Next Owners

If this boundary remains stable, follow-on owners should likely split into two narrower tracks instead of reopening one mixed redesign.

### Track A: `scan` inventory enrichment

- expand unresolved item kinds
- tighten per-kind `suggested_reader`
- decide whether recovery / external issue drift should join the same inventory schema

### Track B: `live-status` contract cleanup

- rename status fields away from ambiguous `latest_prompt_file`
- surface `current_manager_prompt`
- surface active / queued / frozen worker prompt groups from runtime anchors
- add a lightweight `scan_summary` section without re-implementing scan

## Non-Goals

This slice explicitly does not:

1. redesign the entire status family
2. build a global JSON API layer
3. create a full prompt lifecycle ledger
4. widen scan into completion proof or canonical owner truth
5. widen live-status into an every-surface patrol scanner
