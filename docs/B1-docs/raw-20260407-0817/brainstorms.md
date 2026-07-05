# Brainstorm - 20260407-0817--source-ledger-routing-and-manager-audit-boundary

## Context

- Trigger:
  - We are reviewing a proposed redesign around source intake, manager visibility, and protected-root-safe materialization.
  - The motivating pain is real:
    - raw sources currently arrive through different surfaces and are easy to overlook
    - `docs/B1-docs/INDEX.md` is a registry, not a small unconsumed inbox
    - manager supervision can drift from implementation truth when status writeback lags reality
    - protected `develop` cannot write canonical docs, so any durable governance writeback must happen in a dedicated worktree
- User proposals under review:
  - introduce a problem-source directory with subtype subdirectories such as GitHub issue, interruption, review, test
  - keep a small source index that lists only unconsumed items
  - define source consumption as entering pre-research / pre-brainstorm
  - let the manager primarily see the source index and milestone surface, and delegate deeper inspection
  - require worker-side status-vs-reality checking before advancing work
- Independent review inputs used in this pre-research:
  - current intake/runtime state-machine review
  - current merge/gate/source-candidate enforcement review
  - independent critique of `docs/sources/**` as a top-level durable queue
  - independent critique of “all sources must canonicalize via pre-brainstorm”

## Problem Statement

We are trying to solve a real governance gap without creating a second orchestration system.

The concrete pain is:

- unresolved source visibility is fragmented
- `docs/B1-docs/INDEX.md` is a registry, not a small unresolved inbox
- protected-root manager work cannot safely materialize canonical docs directly
- some local source signals should survive runtime restart, but should not automatically become git-tracked governance truth
- doc/runtime status can drift from implementation truth when absorption and writeback are not checked tightly enough

So the real design question is not:

- should everything become a new `docs/sources/**` tree

but:

- where should unresolved source documents live before canonical absorption
- whether any durable family beyond `human interruption` and `external issue` is actually necessary
- when should those records be materialized into git-tracked canonical artifacts
- what minimum gate should verify that absorption writeback actually happened

## Terminology Correction

The most useful unification is not:

- every raw signal must enter the same lifecycle

but:

- every source that is judged to be a real problem to govern should be consumed into pre-brainstorm as the first canonical problem-processing step

This correction matters.

It preserves two important distinctions:

1. `signal` versus `problem`

- not every signal becomes a governed problem
- some signals stay direct-answer, runtime-local, or noise

2. `problem consumption` versus later owner absorption

- once a source is judged to be a problem, pre-brainstorm is the common first consumption point
- later, that pre-brainstorm may promote into milestone/IBM/issue/progress/recovery as appropriate

Under this narrower meaning, GitHub issue and human interruption are conceptually aligned:

- both can begin as `unconsumed` source records
- both become `consumed` when they are absorbed into a pre-brainstorm
- both then continue through the normal pre-brainstorm -> candidate -> milestone / issue lifecycle

So the correct unification target is:

- `problem-source -> pre-brainstorm` as the common consumption start

not:

- `every raw runtime/review/control signal must be forced through one durable queue`

## Responsibility Boundary

This governance line is only about:

- problem-source handling before pre-brainstorm

It is not about:

- pre-brainstorm internals
- candidate / milestone / issue lifecycle after pre-brainstorm
- generic owner progression after a problem has already been digested

So the responsibility boundary should be:

1. source-side governance

- what counts as a source
- which source records enter the unresolved source pool
- how a source becomes a governed problem-source
- how that source is consumed into pre-brainstorm

2. post-consumption governance

- pre-brainstorm analysis
- candidate formation
- milestone / issue materialization
- progress / recovery / review followthrough

This line governs only the first part.

### Boundary Clarification After Source Contraction

Now that durable source families are being contracted, this umbrella pre-research should stay responsible only for shared pre-consumption governance.

It should solve:

- the common definition of durable problem-source
- the common `unconsumed -> consumed` semantics for durable sources that have actually been judged to be governed problems
- the rule that shared `consumed` means absorbed into `pre-brainstorm`
- the rule that family-local runtime closure which never becomes a governed problem-source is not a shared `consumed` transition
- the minimal unresolved-index and writeback invariant
- the anti-loop rule between discovery and current-line absorption
- the manager/worker visibility boundary around unresolved sources

It should not solve family-specific product behavior for either durable family.

Those family-specific questions should move into separate follow-up lines:

1. `human interruption`

- only real human/operator input from chat, input box, or CLI intake
- not AI-discovered problems during dogfooding
- owns intake UX, runtime-local persistence, claim/resolve ergonomics, and absorption writeback for genuine human messages

2. `external issue`

- external tracker items such as GitHub issue
- also the durable external-publication lane for AI-discovered problems that should become externally visible governed work
- owns identity, mapping, publication policy, scan/create/sync/writeback, and public-progress mirroring questions

So this umbrella line is not the place to finish the full GitHub issue model or the full human-intake product contract.

Its job is narrower:

- define the shared source-governance contract those two follow-up lines must satisfy before pre-brainstorm
- define where the common hook/gate backstop attaches for repo-visible governed-problem absorption claims
- define where family-specific behavior must be delegated out

## Source-Type Clarification

After review, this pre-research should explicitly include source-family contraction.

Why:

- schema design becomes much cleaner if durable source families stay minimal
- unresolved index stays small only if it tracks durable problem-sources rather than every discovery mechanism
- review/test happen at many stages, so treating them as default source families would create source inflation and loop risk

So the safer model is:

### 1. Durable problem-source families should default to two

#### A. Human interruption

- human/operator-provided problem input
- local to Freely runtime intake today
- consumed into pre-brainstorm once judged to be a real governed problem
- otherwise resolved by family-local runtime/control/continuity closure without entering the shared source contract

#### B. External issue

- GitHub issue today, with room for future sibling external trackers
- externally supplied problem input
- also consumed into pre-brainstorm once judged to be a real governed problem

These two are conceptually parallel:

- both can expose pre-pre-brainstorm governed problem inputs
- both can be `unconsumed` or `consumed` once the shared source contract applies
- both should freeze after they have been consumed into pre-brainstorm

They are still operationally different:

- recording method may differ
- polling/claiming mechanics may differ
- writeback/sync semantics may differ

But those differences do not require separate lifecycle semantics.

### 2. Review / test / runtime anomaly should default to discovery mechanisms, not durable source families

These should not enter the source pool merely because an artifact exists.

Instead, they should be treated as:

- evidence-producing or anomaly-detecting mechanisms
- capable of exposing a new problem
- not themselves default source families

Important distinction:

- a successful review is not a source item
- a passing test is not a source item
- a review artifact is not copied into the source pool just because it exists
- a runtime anomaly is not automatically a source item just because it fired

Only when they expose a new problem that cannot be absorbed inside the current lifecycle line should a new durable source be created.

And when that happens, the new durable source should usually still be represented as one of the two durable families above:

- human interruption style intake
- external issue style intake

Hard boundary:

- AI-discovered problems never become `human interruption`
- if AI-discovered problems need durable source formalization, they route only to `external issue`
- otherwise they stay inside current-line absorption or internal followthrough rather than entering the durable source pool

### 3. Current-line absorption must win over new-source creation

This is the anti-loop rule that the design must preserve.

If review/test happens while consuming an existing source and the finding stays within the boundary of the current source/pre-brainstorm/issue line, then:

- do not create a new source
- absorb it into the current line
- update the current consumption or owner progression path

Only when the finding is genuinely outside the current line's absorbable boundary should a new durable source be created.

This is what prevents:

- source inflation
- review-derived source spam
- dead-loop self-generation during source consumption

## Current Implementation Inventory

This topic is no longer hypothetical. Freely already has partial source-family handling, but it is uneven.

### 1. Human interruption / local intake

Current reality:

- already implemented as durable local intake under project-local `.freely/intake/**`
- runtime supports:
  - `freely intake chat`
  - `freely intake resolve`
  - `ABSORPTION_TARGET`
  - `LINKED_ARTIFACT`
- tests already cover delegated, absorbed, direct-answer, continuation, cleanup-followthrough, and manager continuity closure paths

What is already good:

- there is real machine-readable source-like local state
- absorption writeback already exists
- some closure semantics are already tested

What is still missing for the new design:

- current storage is project/worktree-local, not explicitly project-global across worktrees
- current intake schema is runtime-oriented, not yet the minimal generic source-document contract we are now discussing
- no separate small unresolved source index optimized for manager patrol

## Ordering Correction

The next step should not be:

- freeze a generic source-document schema in isolation
- then require families to conform later
- then bolt on a gate

That order is too abstract for current repo truth.

Why:

- `human interruption` already has richer durable runtime truth than the proposed two-state source layer
- `external issue` is still policy-first and storage-agnostic
- a generic schema chosen too early will tend to overfit imagined symmetry instead of the actual first slice
- a gate chosen too early will be forced to enforce contracts that no family has yet proven workable

So the safer sequencing is:

1. freeze umbrella invariants

- durable source families stay contracted to `human interruption` and `external issue`
- `consumed` means absorbed into `pre-brainstorm`
- review/test/runtime anomaly stay discovery mechanisms by default

2. prove the first family slice

- use `human interruption` as the first proving lane
- derive a minimal provisional source-view contract from existing `.freely/intake/**` and interruption-resolution truth
- keep that contract overlay-oriented and family-validated rather than prematurely generic

3. only then decide what deserves genericization

- if the family-validated contract is truly reusable, promote the reusable subset into a narrow shared source-document / unresolved-index schema
- if not, keep the shared layer at invariant level only and let families remain the primary contract holders

4. place the backstop after the first slice is legible

- gate/backstop should verify a proven absorption/removal invariant
- it should not invent the invariant by itself

This means the umbrella line should treat schema work as:

- derivative of first-slice family validation

not:

- a prerequisite architecture freeze that blocks family-specific refinement

Implementation implication:

- this family is primarily a refactor / narrowing / relocation candidate
- not a greenfield invention

### 2. GitHub issue / external durable issue source

Current reality:

- product/law routing truth explicitly names `github-issue` as a discovery source
- there is already an older dedicated pre-research line:
  - `docs/B1-docs/20260403-1000--external-issue-integration-and-self-evolution/**`
- current repo does not yet show an equivalent durable local source-document layer for GitHub issues
- no evidence yet of a unified source inbox path or generic source document for external issues

What the older pre-research already explored:

- scanning open GitHub issues
- distinguishing unconsumed source issues from Freely-created milestone issues
- using labels such as `status: triaged`
- creating and syncing external milestone issues
- storing issue mapping in project-local `.freely/github-issue-mapping.json`

What is still true today:

- this older line remains pre-research only
- current runtime/supervision docs explicitly warn that GitHub issue create/sync automation must not be assumed as an already-materialized capability
- therefore GitHub issue should not be treated as a blank family, but it also cannot be treated as implemented runtime truth

What is already good:

- routing semantics exist at the doc/skill level
- there is already a research lineage for GitHub-specific lifecycle questions, so current source-inbox work does not need to reopen the entire external-issue problem from zero

What is still missing:

- durable local source representation, if one is needed at all
- exact closure semantics
- exact hook/gate linkage rules
- a decision on whether the 20260403 mapping/sync model should survive, be narrowed, or be replaced before any implementation starts

Implementation implication:

- this is mostly new design work, not just refactoring
- should not be the first implementation slice unless we first prove local summary records are actually needed
- current source-ledger work should explicitly link to the 20260403 pre-research instead of silently reinventing GitHub issue semantics

### 3. Test / review evidence

Current reality:

- product/law routing truth already treats `code-reviews/test` differently from interruption and generic discovery
- issue-bound review artifacts, pre-tests, verification notes, and implementation decision notes already exist widely in canonical docs
- current governance model already expects many test/review findings to route directly into IBM or dev ownership

What is already good:

- canonical evidence homes already exist
- these families already have stronger issue-bound destinations than a generic source inbox

What is still missing:

- a precise statement of when test/review should create a new independent durable source at all, versus just being referenced by an existing owner

Implementation implication:

- likely mostly contract clarification, not major new storage
- probably not a first-slice source inbox family

Correct framing:

- review/test artifacts are not source-pool entries merely because they exist
- only a newly discovered problem derived from review/test should create a source-pool entry
- review pass / test pass must not be copied into the unresolved problem-source pool

### 4. Runtime anomaly / control-plane signal

Current reality:

- routing truth already distinguishes runtime anomaly from ordinary discovery
- runtime/recovery/governance lanes already exist
- many runtime signals are already local/runtime-owned and should not become repo-governed discovery docs by default

What is already good:

- strong route distinction already exists
- there is already a runtime control plane and recovery framing

What is still missing:

- explicit boundary for when a runtime anomaly graduates into a durable source document versus remaining runtime-local

Implementation implication:

- mostly boundary clarification and selective gating
- should not be widened into a catch-all source inbox family

### 5. Unified unresolved source inbox

Current reality:

- does not yet exist as a first-class, small, manager-facing contract
- `docs/B1-docs/INDEX.md` is not that inbox
- current local intake is family-specific and runtime-oriented
- current repo does not yet show `~/.freely/projects/<project-hash>/source-inbox/**`

Implementation implication:

- this would be a new capability layer
- but it should be introduced narrowly and only after contract/schema/boundary decisions are stable

## Current-State Implications

The implementation inventory changes the shape of the problem.

This is not one greenfield redesign. It is a mixed portfolio:

- one partially existing family that needs narrowing and relocation
- several already-owned source families that mostly need contract clarification
- one genuinely new capability layer that does not exist yet

### 1. What is mostly refactor

#### Human interruption / local governance intake

This is the clearest near-term refactor candidate.

Reason:

- Freely already has durable local intake records
- Freely already has source-like writeback fields
- Freely already has interruption resolution artifacts and tests

So the likely first implementation work is not:

- invent a brand-new general source system

but:

- narrow existing interruption/local intake into a cleaner source-document contract
- decide whether project-local `.freely/intake/**` should stay family-local runtime state or be partially rehomed to a project-global local source inbox
- add the missing unresolved-index and absorption-backstop contract around that family

#### Existing candidate / milestone / owner linkage gates

This is also mainly refactor/followthrough.

Reason:

- candidate -> milestone -> owner gating already exists
- absorbed candidate ownership checks already exist
- the missing gap is narrower: source-family absorption backstop and unresolved-index removal, not lifecycle gating from scratch

So the likely work is:

- extend current gate/hook stages
- do not replace the current governance chain

### 2. What is mostly new capability

#### Small manager-facing unresolved source index

This does not exist yet as a clean contract.

Needed work:

- define a minimal source document schema
- define a minimal unresolved index schema
- define how the first schema cleanly supports `human interruption` and `external issue`, and what evidence would justify any later family expansion
- define where the live unresolved records sit before canonical absorption

#### Project-global local source storage

If Freely decides unresolved durable source documents should survive across worktrees, then project-local worktree `.freely/intake/**` is not enough.

That would require new capability in:

- project hashing / project identity
- `~/.freely/projects/<project-hash>/...` discovery and lookup
- local archival / compaction policy

This is new, not just a rename.

### 3. What is mostly boundary clarification, not first-slice implementation

#### GitHub issue

Current truth says this source family exists, but there is no matching local durable raw-source layer yet.

That means the next right move is probably:

- decide whether GitHub issue needs local durable source summaries at all

not:

- immediately build GitHub-specific storage and gates

#### Test / review

These families already have stronger canonical homes than a generic inbox.

So the next right move is:

- clarify when they may optionally emit a source summary
- otherwise keep them issue-bound

not:

- push them into the first unresolved-source implementation slice

#### Runtime anomaly

This family already has runtime/recovery semantics and should not be widened into generic durable source-ledger traffic without strong proof.

So the next right move is:

- tighten the graduation rule from runtime-local anomaly to governed owner

not:

- treat all runtime anomaly signals as unresolved source inbox entries

## Build / Refactor / Do-Not-Build Split

### 1. Build now only if the slice stays narrow

The strongest bounded first slice is:

- one local durable source family:
  - human interruption / local governance signal
- one small unresolved source index:
  - active items only
- one narrow absorption backstop:
  - if a canonical repo artifact claims it absorbed such a source, the source must leave the active index and point back to the absorbing owner

This slice is justified because:

- there is already real runtime implementation to refactor
- the user pain is primarily around overlooked local sources and fake closure
- it gives a proving ground for schema, placement, and gate semantics without dragging in every source family

### 2. Refactor before generalizing

Before any “all source types” rollout, Freely should refactor:

- the current human-intake contract
- the current manager-facing visibility surfaces
- the current source-absorption writeback invariants

This means:

- reduce ambiguity around `ABSORPTION_TARGET`, `LINKED_ARTIFACT`, and final source closure semantics
- define whether current `.freely/intake/**` remains family-specific runtime truth or becomes an adapter into a more general local source inbox
- ensure source closure is checked where canonical owner writeback occurs

### 3. Do not build in the first slice

This pre-research does not support first-slice implementation of:

- blanket `docs/sources/**`
- all-source-family durable inbox rollout
- mandatory physical move semantics
- manager-only-two-files hard contract
- GitHub issue durable local storage before proving it is needed
- review/test/runtime anomaly forced into the same unresolved queue as human interruption

## Likely Follow-On Issue Split

If this pre-research graduates, the safest follow-on issue split is:

### Slice A: source contract and unresolved-index schema

Scope:

- source document shape
- unresolved index shape
- `unconsumed` / `consumed` semantics
- canonical owner linkage fields

Expected nature:

- mostly new capability definition
- little runtime mutation at first

### Slice B: local storage boundary and project identity

Scope:

- `~/.freely/projects/<project-hash>/...` versus project `.freely/**`
- project hashing / canonicalization
- archival / retention / compaction

Expected nature:

- mixed contract + runtime implementation
- new capability layer

### Slice C: human interruption intake refactor

Scope:

- current `.freely/intake/**` alignment with the narrowed source contract
- manager-facing unresolved view
- source resolution writeback consistency

Expected nature:

- mostly refactor of existing runtime behavior
- first plausible dogfooding slice

### Slice D: stage-based absorption gate

Scope:

- pre-brainstorm / issue / merge-time backstop semantics
- unresolved-index removal check
- source-family-specific closure rules

Expected nature:

- refactor / extension of existing gate stack

### Slice E: optional later family-specific expansions

Scope:

- GitHub issue durable summary, if justified
- optional review/test summary emission, if justified
- runtime anomaly graduation contract

Expected nature:

- follow-on only after Slice A-D prove useful

## Candidate Materialization Map

The current umbrella research should not promote directly into one large implementation issue.

Safer promotion shape:

- keep this current candidate as the umbrella boundary and sequencing owner
- materialize follow-on candidates only when each slice becomes independently defensible

Recommended promotion order:

1. source contract and unresolved-index schema
2. human interruption / local intake alignment
3. stage-based absorption backstop
4. storage-boundary deepening only if the first two slices prove project-global local storage is necessary
5. GitHub issue family reconciliation only after the 20260403 line is explicitly re-reviewed against the newer narrowed source contract

This ordering intentionally delays:

- repo-wide storage migration
- GitHub issue automation
- multi-family source-ledger generalization

## Existing Truth

### 1. Current routing truth is already lifecycle-aware, not source-directory-aware

`PROJECT_INTENT` already distinguishes multiple source families and does not force all raw signals through one identical first hop.

But for governed problem intake, the user clarification sharpens the intended model:

- once a source is recognized as a real problem rather than mere runtime/control noise, pre-brainstorm should be the default common consumption start

That means the safe refinement is:

- preserve route plurality for raw signals and operational events
- but align durable problem-source families around `pre-brainstorm` as the first canonical digestion step

- project intent / chat / GitHub issue -> `doc-pre-brainstorm-execution`
- code-reviews / test -> `doc-ibm-execution` or `dev-loop-execution`
- governance drift -> `doc-ibm-execution`
- runtime anomaly -> `doc-pre-brainstorm-execution` or `recovery-subagent-governance`

So the current product truth is:

- source type matters
- but route depends on both source type and current lifecycle context
- not every source should be normalized through a brand-new pre-brainstorm
- there is no existing canonical `docs/sources/INDEX.md` surface today, so any new source-ledger proposal must justify why it deserves to become a new durable surface rather than tightening existing routing and writeback contracts

### 2. Current governance state is richer than two-state source truth

`LAWS` separates:

- `source_class`
- `route_kind`
- `phase_state`
- `runtime_state`

and also requires unresolved work to remain visible in canonical milestone queues with:

- `next_action`
- `revisit_trigger`

So `unconsumed | consumed` can at most describe source-document truth in the raw inbox.
It cannot replace the existing lifecycle truth.

### 3. Current manager contract is wider than “read two files”

`manager-agent` and `auto-loop-orchestrator` already require the manager to inspect:

- `live-status`
- `fleet-status`
- milestone / issue / progress / recovery
- interruption backlog
- relevant pre-brainstorm lifecycle

This means a hard rewrite to “manager only reads source index + milestones” would be a regression.

More precisely:

- `docs/milestones.md` is an orchestration surface, not a raw discovery surface
- manager patrol already starts from runtime and fleet observation, then reconciles documentary truth
- artifact deep-reads can be delegated when route is unclear, but cannot be forbidden to the manager because completion, arbitration, and recovery decisions still depend on them

### 4. Protected-root rule already forbids canonical writeback on manager `develop`

This part of the user proposal is directionally correct:

- the manager may run on protected `develop`
- but canonical `docs/**` writeback cannot happen there
- if a source must become a durable governance artifact, the manager has to dispatch a worker into a dedicated worktree

This also means any future source-ledger design must distinguish:

- contract truth: where the rules live
- live record materialization: where unresolved durable records live
- runtime-local control-plane evidence: what should stay outside git-tracked governance artifacts

## Compatibility Review Against Current Freely Design

This proposal must fit the current Freely architecture, not overwrite it.

### 1. `lead-agent` and `context-source-skill` already assume plural source pools

Current architecture already treats:

- chat / session evidence
- review / test
- github-issue
- milestone
- issue / progress / recovery

as distinct first-hop inputs.

Implication:

- a future source inbox can be an additional patrol surface
- it cannot become the only first-hop source truth
- source-ledger work must preserve route plurality instead of collapsing first-hop routing into one queue

### 2. `manager-agent` already owns patrol, arbitration, and source completeness

Current manager truth already requires:

- `live-status`
- `fleet-status`
- interruption backlog
- milestone / issue / progress / recovery
- pre-brainstorm lifecycle

Implication:

- a small unresolved source index can help the manager notice unresolved raw inputs faster
- but it cannot replace manager patrol of runtime/fleet/recovery truth
- any design that says “manager only reads source index + milestone” would regress current product behavior

### 3. `interruption-manager-handler` is triage, not canonical lifecycle materialization

Current interruption handling already does:

- durable notice / claim of human interruption
- minimal intent understanding
- restart-point routing
- ownership decision

It does not itself promise:

- full canonical lifecycle closure
- generic source-ledger semantics for every source family

Implication:

- first-slice source work should treat current interruption manager flow as a family-specific adapter and triage layer
- do not retrofit it into a universal source-orchestration engine

### 4. Current runtime intake is worktree-local and runtime-oriented

Current `.freely/intake/**` behavior sits naturally in the runtime/control-plane layer.

Implication:

- if unresolved source visibility must survive across worktrees, a project-global local layer may be needed
- but the first slice must preserve the already-working runtime-local intake behavior while deciding whether a higher-level project-global view is additive or migratory

### 5. Current gate stack is already lifecycle-aware

Current gates already reason about:

- candidate -> milestone -> owner linkage
- absorbed-candidate owner truth
- protected-branch merge materialization

Implication:

- the right source-ledger backstop is a staged extension of current lifecycle-aware gates
- not a separate global gate that tries to police all raw source churn

### 6. Existing GitHub issue pre-research is a sibling line, not current truth

The 20260403 external-issue pre-research already explored:

- scan/create/sync/close semantics
- label-based triage states
- source-vs-milestone issue distinction
- mapping in project-local `.freely`

But current runtime and follow-on docs still treat that line as:

- pre-research only
- not yet materialized capability

Implication:

- current source-ledger research must link to that line
- but must not import GitHub automation assumptions into the first slice

## Problems With The Strong Proposal

### 1. “All sources must be consumed into pre-brainstorm” is too strong if “source” includes every raw signal

If interpreted at raw-signal level, this breaks existing routing truth:

- test / review findings may belong directly to existing issue-bound IBM or dev-loop
- runtime anomalies may belong to recovery
- governance drift may belong directly to IBM/governance repair
- direct-answer interruptions may be resolved runtime-locally without becoming durable governance work

But after the terminology correction above, the stronger and more useful statement becomes:

- every source that has already been judged to be a real governed problem should be consumed into a pre-brainstorm

So the real design line is:

- raw signal level: not universal
- governed problem-source level: pre-brainstorm should be the common first consumption step

### 2. A blanket top-level `docs/sources/**` for every source family is likely over-broad

If `docs/sources/**` becomes a durable catch-all for:

- interruptions
- runtime signals
- tests
- reviews
- governance drift
- GitHub issues

then it becomes a second orchestration truth surface beside:

- `.freely/intake/**`
- `docs/B1-docs/**`
- `docs/milestones.md`
- issue-bound review / verification artifacts

That creates three risks:

- duplicate scanning
- duplicate writeback
- ambiguous canonical ownership

### 3. “Manager only reads two surfaces” is also too strong

It is directionally useful as a patrol simplification heuristic, but not as an absolute contract.

Why:

- manager patrol must still consider live runtime state
- manager patrol must still consider fleet/worktree state
- continuation / recovery truth cannot be hidden behind worker delegation forever
- ownership conflicts, queued lanes, frozen lanes, and stale runtime state all live outside a pure source/milestone pair

So the safe rule is not:

- manager reads only two things

but rather:

- manager begins from a very small priority visibility surface, then delegates deeper inspection whenever route or truth is not already stable

### 4. “Worker always audits before any action” also needs narrowing

The strong form is expensive and can become ritualized.

Audit-first is clearly needed when:

- touching an existing milestone-owned line
- claiming something is already done / blocked / consumed / completed
- consuming a source into an existing canonical owner
- resuming work in a possibly stale worktree
- performing continuation or recovery work where recorded status may be stale

It is less obviously required for:

- brand-new low-risk source capture
- greenfield pre-brainstorm creation where no existing owner is claimed
- tightly scoped worker execution that already received a precise manager-owned route and only needs local readiness checks rather than full project patrol

So the rule should be:

- status-vs-reality audit before state transition, resumption, absorption, or completion claims

not:

- audit absolutely everything before any write

## Refined Direction

### 1. Separate “raw source visibility” from “canonical lifecycle truth”

This pre-research supports the separation, but not the overreach.

Recommended distinction:

- raw source visibility surface:
  - a small inbox / ledger of unresolved source documents
  - optimized for manager patrol and dispatch
- canonical lifecycle truth:
  - pre-brainstorms
  - milestones
  - issue/progress/recovery
  - runtime-local intake / resolution artifacts

The inbox must not pretend to replace lifecycle truth.

### 2. Introduce a source inbox only if it is narrowly scoped

Safe version:

- durable, low-volume, manager-facing raw source documents that still need routing judgment
- a small unconsumed index
- pointer-oriented records, not full duplicated execution truth
- documentary queue surface only for source families whose unresolved state must survive runtime restarts and remain human-auditable

Unsafe version:

- every interruption, runtime signal, test result, and review artifact copied into a git-tracked source tree
- a new top-level queue that competes with milestone, issue, progress, recovery, or runtime intake truth

So if a source directory is introduced, it should likely be constrained to:

- durable discovery summaries that still need routing
- not raw high-churn runtime/control-plane traffic

### 2A. Placement options must be evaluated separately from lifecycle semantics

The durable-source question has two different axes:

- semantic axis:
  - what `unconsumed` and `consumed` mean
  - what canonical owner kinds are allowed
- placement axis:
  - where unresolved source documents live before canonical absorption

Those should not be collapsed into one decision.

### 2B. Placement option review

#### Option 1: git-tracked `docs/sources/**`

Pros:

- human-auditable in the repo
- easy to link from canonical artifacts

Cons:

- too easy to turn into a second orchestration truth surface
- manager on protected `develop` still cannot write there directly
- high risk of mixing unresolved local intake with canonical governance artifacts
- pushes high-churn control-plane state into git history

Assessment:

- reject as the default unresolved-source landing zone
- at most, future git-tracked artifacts should be post-absorption canonical artifacts, not the primary raw-source inbox

#### Option 2: gitignored directory under project `docs/`

Pros:

- path is near governance docs
- does not require immediate `git add` or commit

Cons:

- semantic mismatch: it looks like canonical documentation but is not canonical
- easy to confuse with real `docs/**` truth surfaces
- weakens the protected-root boundary by creating a quasi-document layer inside the repo
- creates a hidden local state surface exactly where users expect governed artifacts

Assessment:

- reject
- this is the worst of both worlds: repo-local enough to look authoritative, but not governed enough to be true

#### Option 3: project-scoped local control plane under `~/.freely/projects/<project-hash>/`

Pros:

- clean separation from git-tracked canonical artifacts
- naturally project-isolated across multiple repos and worktrees
- can persist unresolved local sources across runtime restart without polluting repo history
- matches the semantics of runtime-owned local control-plane state better than `docs/`

Cons:

- requires explicit project hashing / discovery / migration rules
- canonical artifacts must link back by source id/path rather than simple in-repo relative path only
- if overused, it can grow into a second local lifecycle system

Assessment:

- currently the strongest candidate for unresolved durable local source documents
- but only if scoped narrowly as a small local source inbox / ledger, not a parallel lifecycle engine

### 2C. Recommended placement split

The most coherent split so far is:

- `docs/system/**`
  - contract truth
  - naming, semantics, absorption invariants, and gate rules
- `~/.freely/projects/<project-hash>/source-inbox/**`
  - unresolved durable local source documents that still need routing/materialization
- repo `docs/**`
  - canonical git-tracked lifecycle artifacts after materialization in a dedicated worktree

This preserves a clean boundary:

- local unresolved source state stays local
- canonical lifecycle truth stays canonical
- the contract for how the two connect remains governed in Freely capability docs

### 3. Source state should stay two-state and minimal

For source documents themselves, the safest model is:

- `unconsumed`
- `consumed`

This pre-research now supports:

- no intermediate source states such as `claimed`, `in_analysis`, `assigned`, or `materializing`
- retry-by-reread instead of resume-from-midstate
- using source-file existence plus final consumption markers as the durable truth for the source itself

Why:

- AI is better at rereading current truth than maintaining fragile mid-process status
- stale intermediate source states would create false precision and more drift
- interruption/retry should just reopen the same source document and continue toward consumption

### 3A. Consumption should mean “absorbed into pre-brainstorm” for problem-sources

For this proposal, the user's clarified intent is the better narrowing:

- a durable problem-source document is `unconsumed` until it has been absorbed into a pre-brainstorm
- it becomes `consumed` once that pre-brainstorm exists and links back to it

After that point, later lifecycle promotion is no longer source consumption; it is owner lifecycle progression.

So the sequence becomes:

1. source exists as unresolved problem-source
2. source is consumed into pre-brainstorm
3. pre-brainstorm later promotes into candidate / milestone / issue / continuation as needed

This keeps the source model simple while still preserving the broader lifecycle model.

Important boundary:

- this rule is for problem-sources
- direct-answer/runtime-only/noise signals still may never become problem-sources at all

### 3B. Pre-brainstorm is the common problem digestion layer

Under this clarified model, pre-brainstorm is where:

- one or more source documents are digested
- the actual problem statement is formed
- source merging, splitting, or rejection happens
- later candidate promotion is decided

This aligns well with the user's intended semantics:

- source docs stay short
- pre-brainstorm carries the actual analysis
- source index only needs to track unresolved problem-sources

### 3C. Later canonical owner absorption is a different lifecycle step

Once a source has been consumed into pre-brainstorm:

- source index exit has happened
- source lifecycle is effectively done
- later movement into IBM/issue/progress/recovery is no longer “consuming the source”

That later movement belongs to:

- pre-brainstorm/candidate lifecycle
- not raw-source lifecycle

This distinction resolves the earlier ambiguity around `consumed`.

### 3D. Source-family differences now move earlier, not later

With this corrected framing, source-family-specific differences are mainly about:

- whether a raw signal should become a durable problem-source at all
- how that source is recorded
- how it is linked into pre-brainstorm

not about:

- whether problem-sources share pre-brainstorm as their first canonical digestion step

Recommended interpretation for local source documents:

- they should stay short and source-like, not become mini pre-brainstorms
- their canonical consumption target is pre-brainstorm
- after final consumption writeback, the source document should freeze
- physical move is not required; a frozen source document plus pre-brainstorm linkage is cleaner than “move the original file into docs”

### 3B. Source document responsibility must stay narrow

Source documents should be short.

They should answer only:

- what source family this is
- the source id
- when it was created
- the raw signal / original content
- whether it has been consumed
- what consumed it

They should not become:

- brainstorms
- route comparison notes
- milestone planning artifacts
- long-running analysis notes

That work belongs in:

- `docs/B1-docs/**`
- milestone / issue / progress / recovery artifacts

So the split should be:

- source document: short input record
- pre-brainstorm: analysis and digestion of one or more sources

### 3C. “Must move after consumption” is too strong as a universal invariant

The useful invariant is lifecycle closure, not one specific file operation.

What must be true after consumption:

- the source must no longer remain in the unresolved queue
- canonical ownership must become explicit
- the canonical owner must live in a concrete worktree/repo artifact when the route requires durable governance materialization
- the source document must show how it was absorbed

What does not need to be universally true:

- that the original source document file is physically moved into repo `docs/**`

Why not:

- current Freely runtime contracts already prefer `ABSORPTION_TARGET` and `LINKED_ARTIFACT`
- retention of source provenance helps recovery, replay, deduplication, and post-hoc audit
- different source families may need different closure semantics
- a short frozen source document is easier to preserve and audit than a moved-and-mutated hybrid artifact

So the safe rule is:

- active ownership moves
- unresolved queue membership ends
- provenance remains queryable
- the source document freezes after final consumption writeback

not:

- every source file must literally be moved

### 3D. Closure semantics should be source-family-specific

Different source families should not share one identical closure action.

Examples:

- local human interruption / local governance intake
  - unresolved source may begin in `~/.freely/projects/<project-hash>/source-inbox/**`
  - if absorbed into pre-brainstorm/IBM/issue, the unresolved entry must leave the active index and point to the canonical artifact
  - the frozen local source document may remain archived locally instead of being physically moved
- GitHub issue or other external durable issue source
  - there may be no local source file to move at all
  - closure should instead require canonical materialization plus source linkage, for example issue URL/id plus absorbed target
- runtime-local direct-answer/control events
  - many should never enter durable source-ledger flow
  - forcing them through repo-materialization or physical move would be wrong
- test / review evidence
  - may route directly into existing IBM/dev owner
  - closure should mean owner writeback references the evidence correctly, not that evidence files are copied or moved into a new generic source tree

### 3E. Candidate / pre-brainstorm / milestone gates should validate different things

The backstop should be staged.

#### Stage 1: pre-brainstorm / candidate materialization gate

If a pre-brainstorm or candidate claims a source path/reference, check:

- the referenced source exists or is otherwise resolvable for its source family
- the source family is declared correctly
- the source has not already been marked consumed unless the artifact explicitly marks shared/merged ownership semantics

Do not require milestone or issue materialization yet at this stage.

#### Stage 2: milestone / issue materialization gate

If a candidate/issue/IBM artifact claims that a source has now been absorbed, check:

- the source no longer appears in the unresolved source index
- the source document points to the new canonical owner when that source family has a durable local record
- the canonical owner points back to the source reference
- if the source family is external-only, equivalent linkage exists even without a local source file

This is where “consumed” must become enforceable.

#### Stage 3: merge / promotion / governance-check backstop

At protected-branch merge or post-merge governance-check time, only verify repo-visible claims:

- any repo artifact that says it absorbed a source must point to a valid source reference or allowed external reference
- any unresolved-source index that is repo-visible in the proposal path must not still list a source already marked absorbed by merged canonical artifacts
- no milestone/issue/pre-brainstorm artifact may claim canonical absorption while leaving contradictory unresolved-state truth behind

This stage should catch drift, not invent new semantics.

### 3F. Retry semantics should stay simple

When work is interrupted before consumption:

- do not restore an intermediate source state
- reread the source document
- inspect any already-created canonical artifacts
- re-dispatch from current truth

This keeps source management robust:

- source document exists and is still `unconsumed` -> continue from it
- source document is already `consumed` -> do not requeue it
- anything in between should be inferred from actual artifacts, not from a third transient source state

### 4. Manager visibility should be “small first surface”, not “exclusive surface”

The manager should have a deliberately small first-hop patrol surface, but not a blinded one.

Safe interpretation:

- primary visible patrol surfaces:
  - source inbox / unresolved source index
  - `docs/milestones.md`
  - `live-status` / `fleet-status`
- deeper truth:
  - delegated to workers when route or truth is unclear
  - but still available to manager when needed for arbitration or recovery

Unsafe interpretation:

- manager is forbidden from directly checking recovery/progress/pre-brainstorm evidence when deciding completion, resumability, or arbitration

### 5. Worker audit should be attached to truth-changing operations

Recommended worker contract:

- before claiming an existing line is aligned, consumed, completed, blocked, or resumable
- before absorbing new source evidence into an existing canonical owner
- before merge/cleanup/completion writeback
- before resuming a stale or uncertain worktree
- before continuation/recovery writeback that depends on prior documentary truth

the worker must perform a minimal status-vs-reality audit.

That audit should be route-scoped:

- local worktree correctness and delegated target for ordinary feature work
- progress/recovery/session continuity for continuation or recovery work
- canonical owner alignment when absorbing a new source into an existing line

It should not default to a full manager-style project patrol on every worker turn.

## Likely Landing

### A. What this pre-research supports

1. A distinct raw-source visibility concept separate from `docs/B1-docs/INDEX.md`
2. A small unconsumed source queue rather than a growing consumed-history index
3. Manager dispatch from protected root, with canonical writeback delegated to worker worktrees
4. Worker-side reality audit before state-changing or status-claiming actions
5. Hook/gate backstops that verify source consumption writeback stays aligned with canonical artifacts
6. Preserving the distinction between raw-source visibility, orchestration truth, and runtime control-plane truth
7. Favoring project-scoped local unresolved-source storage over repo `docs/`-local ignored storage

### B. What this pre-research rejects

1. Forcing all source types through pre-brainstorm
2. Replacing lifecycle truth with a two-state source model
3. Making `docs/sources/**` a blanket durable home for every raw event type
4. Hard-coding the manager to read only two files forever
5. Requiring every worker to perform a manager-grade full patrol before any mutation
6. Using a gitignored repo `docs/` subdirectory as a quasi-canonical unresolved-source layer

## Minimum Backstop Contract Worth Prototyping

If a durable source-inbox layer is later introduced, the smallest viable enforcement shape is:

1. A canonical artifact that cites a durable source document must point to a real source reference.
2. A source document that has been marked absorbed into canonical governance work must no longer appear in the unconsumed source index.
3. A source document marked absorbed must identify its canonical target.
4. Worker/skill writeback should remove consumed items from the active source index in the same change that materializes the canonical target.
5. Gates should verify these invariants only for durable source-inbox entries, not for every runtime-local interruption/test/review event in existence.
6. Any such gate must preserve existing plurality of routes and must not reinterpret milestone as a raw-source inbox.
7. The gate should validate repo-visible absorption claims, not require every local source document itself to become git-tracked.
8. Source-family-specific closure semantics are allowed, but each family must still satisfy the same high-level invariant: no stale unresolved queue entry after canonical absorption is claimed.

## Recommended Research Split

This topic should not move forward as one repo-wide redesign.

Safer split:

1. First decide boundary and placement:
   - whether a durable source inbox should exist at all
   - if yes, where contract truth lives versus where unresolved source documents live
   - keep `~/.freely/projects/<project-hash>/` and repo `docs/**` responsibilities explicitly separate
2. Then decide one bounded source family:
   - choose only one family whose unresolved state truly needs durable human-auditable routing
   - explicitly reject broad “all source types” rollout for the first slice
3. Only after that define a narrow hook/gate:
   - verify removal from unresolved index when canonical absorption is claimed
   - do not expand the first gate into generic runtime-event policing
4. Keep manager/worker contract refinement separate:
   - manager first-hop visibility simplification
   - worker route-scoped audit duty
   - these should be aligned with the ledger slice, not silently bundled into it

### Concrete Follow-Up Worktrees

Once this umbrella boundary is frozen, the next research should split into separate dedicated worktrees:

1. `human interruption` worktree

- responsibility:
  - real human interruption intake only
  - local runtime record shape
  - unresolved visibility for managers
  - claim/resolve/absorb mechanics
  - how consumed interruption records point to `pre-brainstorm`
- not responsible for:
  - AI-discovered problem publication
  - GitHub issue identity
  - public progress mirroring

2. `external issue` worktree

- responsibility:
  - external issue as durable source family
  - AI-discovered problem formalization into external issue flow
  - source issue versus public tracking issue versus internal canonical owner identity
  - mapping, labels, comments, sync, and closeout semantics
- not responsible for:
  - local human interruption UX
  - generic unresolved-index semantics already owned by this umbrella line

This split is important from a three-loop perspective:

- source loop:
  - unresolved durable source -> `pre-brainstorm`
- owner loop:
  - `pre-brainstorm` -> candidate -> milestone / issue / progress
- publication/runtime loop:
  - family-specific external writeback or runtime-local control-plane behavior

The umbrella line owns only the shared source loop contract.
The two family-specific worktrees should each own only the part of the publication/runtime loop that belongs to that family.

## Recommended Execution Order

If this line continues, the safest forward order is:

1. Freeze the current boundary decisions
   - source document stays short
   - source state stays two-state
   - not all raw signals or discovery mechanisms enter pre-brainstorm, but the contracted durable source families do once they become governed problems
   - not all families enter one inbox
   - manager keeps runtime/fleet patrol

2. Define the narrow source contract
   - minimal source document schema
   - minimal unresolved index schema
   - canonical owner linkage fields

3. Decide the live storage boundary
   - keep contract truth in `docs/system/**`
   - decide whether live unresolved records stay in project `.freely/**`, move to `~/.freely/projects/<project-hash>/...`, or use an adapter path for the first slice
   - explicitly compare against the older GitHub issue mapping/storage pre-research before introducing a second local store

4. Refactor one existing family only
   - use human interruption / local governance intake as the proving ground
   - preserve current runtime behavior while narrowing writeback semantics

5. Add one narrow backstop
   - when canonical repo artifacts claim absorption of a durable source-inbox item, verify unresolved-index exit plus target linkage
   - do not over-gate runtime-local churn

6. Only then reopen family expansion
   - GitHub issue
   - review/test
   - runtime anomaly

This order matters because current Freely already has partial runtime truth for human interruption, while the other families are either issue-bound already or still pre-research-only.

## Source-Family Closure Matrix

This matrix is the current safest framing for future hook/gate design.

### 1. Human interruption / local governance signal

- likely unresolved landing:
  - `~/.freely/projects/<project-hash>/source-inbox/human-interruptions/**`
- common routes:
  - pre-brainstorm
  - existing issue / continuation
  - manager direct answer / runtime-local resolution
- canonical absorption target:
  - `docs/B1-docs/**`
  - `docs/epics/**`
  - `docs/progress/**` / `docs/recovery/**`
  - runtime-local resolution artifact for direct-answer class
- unresolved exit condition:
  - remove from active unresolved index when a canonical owner or allowed runtime-local resolution has been written
- required provenance:
  - source id/path
  - source family
  - absorption target
  - linked canonical artifact or allowed runtime-local resolution artifact
- gate focus:
  - if repo artifact claims absorption, unresolved index must no longer list it
  - if route is direct-answer/runtime-local, do not require repo docs materialization

### 2. External GitHub issue / external durable issue source

- likely unresolved landing:
  - no mandatory local raw file
  - optional local summary record only if Freely decides this family needs durable routing visibility
- common routes:
  - pre-brainstorm
  - existing issue-bound IBM if clearly same owner
- canonical absorption target:
  - `docs/B1-docs/**`
  - then milestone / issue materialization as needed
- unresolved exit condition:
  - external issue is linked to a canonical owner and no longer appears in any unresolved local summary queue, if such a queue exists
- required provenance:
  - external system id/url
  - source family
  - canonical owner path
- gate focus:
  - check linkage correctness, not file movement
  - never require a fake local source file just to satisfy the gate

### 3. Test failure / regression evidence

- likely unresolved landing:
  - usually no generic source inbox
  - stays in test evidence and routes directly
- common routes:
  - existing IBM owner
  - existing dev owner
  - pre-brainstorm only if it exposes a new cross-cutting boundary
- canonical absorption target:
  - issue-bound review / decision note / progress / recovery
- unresolved exit condition:
  - if a local summary record was created, it leaves the unresolved queue once issue-bound owner writeback references it
- required provenance:
  - test command/evidence ref
  - owner issue/progress linkage
- gate focus:
  - ensure evidence is linked by the owner that claims to absorb it
  - do not force copy/move into a generic source tree

### 4. Code review finding

- likely unresolved landing:
  - usually no generic source inbox
  - review artifact itself is already the durable evidence
- common routes:
  - IBM followthrough
  - dev followthrough
  - pre-brainstorm only if review exposes a new governance/product boundary
- canonical absorption target:
  - issue-bound code-review / decision note / progress
- unresolved exit condition:
  - review finding is referenced by the owner that resolves or absorbs it
- required provenance:
  - review artifact path
  - absorbing owner path
- gate focus:
  - verify the owner does not claim closure while orphaning referenced review evidence

### 5. Runtime anomaly / control-plane signal

- likely unresolved landing:
  - runtime-owned local state
  - not automatically part of durable source-ledger flow
- common routes:
  - recovery
  - pre-brainstorm if it reveals a new product/governance gap
- canonical absorption target:
  - `docs/recovery/**`
  - `docs/B1-docs/**`
  - issue/progress only if the anomaly becomes a stable owner-owned problem
- unresolved exit condition:
  - runtime-local signal may simply age out after recovery or after canonical owner creation
- required provenance:
  - runtime event id or artifact ref
  - chosen route
  - canonical owner when one exists
- gate focus:
  - do not over-gate raw runtime churn
  - only validate repo-visible claims once an artifact says the anomaly was absorbed into governance work

## Gate Design Implications

The matrix implies three design rules:

1. Durable unresolved-source handling should default to the two contracted families, not expand blindly to every discovery mechanism.
2. Not every absorbed source needs or even allows physical file movement.
3. Hook/gate should validate lifecycle closure claims at the correct stage, not manufacture artificial sameness between fundamentally different source families.

## Open Questions

1. Should unresolved durable source documents be retained after absorption under `~/.freely/projects/<project-hash>/`, or compacted into a smaller local audit ledger?
2. Is there any durable source family beyond `human interruption` and `external issue` that research can justify, or should all other discovery channels remain non-default mechanisms?
3. How should one source document map to multiple downstream owners, or multiple source documents collapse into one owner?
4. Should the first implementation target only one bounded durable family, such as human-governance interruptions, before reconciling external issue handling?
5. What is the smallest project-hash/project-identity scheme that preserves local project isolation without creating user-hostile path churn?
