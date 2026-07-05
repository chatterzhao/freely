# Brainstorm - 20260407-1036--human-interruption-source-governance-boundary

## Context

- This follow-up line exists because the umbrella source-governance pre-research has now contracted durable source families.
- `human interruption` is no longer a catch-all dogfooding bucket.
- In the formal product model, it means only real human/operator input through chat, CLI, or input-box style intake.

## Problem

Freely needs a clean product and runtime contract for real human interruptions after source-family contraction.

The main risk is semantic pollution:

- if AI-discovered problems continue to masquerade as interruptions, the human intake model will drift
- if human intake absorbs GitHub/publication concerns, the runtime contract will become overcomplicated

So this line should answer only the human-intake responsibilities.

## Responsibility Boundary

This line owns:

- what counts as a real human interruption
- the local interruption record shape before and after consumption judgment
- unresolved human-interruption visibility for manager routing
- claim / resolve / absorb transitions at runtime level
- how a consumed interruption points to `pre-brainstorm`
- how direct-answer or runtime-only interruption handling avoids fake canonical materialization
- how delegated continuation / cleanup / runtime followthrough remains in the runtime family instead of being misread as source-inbox lifecycle truth

This line does not own:

- AI-discovered problem publication
- GitHub issue creation
- external issue identity or label taxonomy
- milestone/public progress sync
- generic source-family schema for every other durable family

Hard boundary:

- AI-discovered problems never become `human interruption`
- if AI-discovered problems need durable source formalization, that belongs only to the `external issue` family

## Runtime Truth To Preserve

Current runtime truth is already richer than a raw inbox.

Today, human interruption/local intake already provides:

- durable local records under `.freely/intake/<intake_id>/meta.env` and `message.txt`
- persisted statuses `new | classified | delegated | absorbed | dropped`
- persisted routing fields such as `CLASSIFICATION`, `REACTION`, `LINKED_ARTIFACT`, `ABSORPTION_TARGET`, `DELEGATED_WORKTREE`, `SESSION_REFS`
- separate resolution artifacts under `.freely/run/interruption-resolution/<intake_id>/`
- manager-first claim and routing through the interruption dispatcher
- stale-claim recovery
- delegated continuation re-entry and later absorption into new manager continuity

That means this family is not starting from a missing capability. It is already a runtime-owned durable intake family with tested lifecycle behavior.

So the design problem here is narrower:

- contract clarification
- boundary cleanup
- possible adapter/overlay refactor for unresolved source visibility

not:

- inventing a brand new interruption lifecycle

## Concrete Runtime Inventory

Current implementation evidence is concrete enough to name the family-local durable shapes more precisely.

### 1. Intake metadata fields already persisted

Current tests and fixtures show `.freely/intake/<intake_id>/meta.env` already persists fields such as:

- `INTAKE_ID`
- `CREATED_AT`
- `AUTHOR`
- `CHANNEL`
- `STATUS`
- `CLASSIFICATION`
- `REACTION`
- `LINKED_ARTIFACT`
- `DELEGATED_WORKTREE`
- `SESSION_REFS`
- `CLAIMED_BY`
- `CLAIMED_AT`
- `ABSORPTION_TARGET`
- `RESOLUTION_ARTIFACT`

So the first slice does not need to invent a durable intake envelope. It needs to decide what smaller source-facing subset, if any, should be derived from this richer runtime truth.

### 2. Resolution artifacts are already separate durable records

Current tests and skills also show `.freely/run/interruption-resolution/<intake_id>/` already stores:

- `meta.env` with `RESOLVED_BY`, `REACTION`, `CLASSIFICATION`, `ABSORPTION_TARGET`, `LINKED_ARTIFACT`, `DELEGATED_WORKTREE`, `STATUS`
- `resolution.md` with human-readable rationale, handoff summary, and absorption recommendation

This separation matters:

- intake truth is not the same object as resolution truth
- any source-facing overlay must avoid collapsing those two durable records back into one fake generic document

### 3. Tested closure paths already cover multiple runtime outcomes

Current test evidence already proves several distinct closure or handoff paths:

1. discovery -> pre-brainstorm absorption

- `test-freely-human-chat-intake` proves:
  - intake record creation via `freely intake chat`
  - claim/classification writeback
  - resolution artifact creation
  - final `STATUS="absorbed"` with `ABSORPTION_TARGET` pointing to `docs/pre-brainstorms/**`
- `test-freely-interruption-direct-answer` also proves a nearby but distinct path:
  - discovery may be handed off as `delegated + discovery + handoff://pre_brainstorm`
  - so the family already supports both direct absorption and delegated pre-brainstorm routing, depending on runtime context

2. delegated continuation remains runtime-visible

- `test-freely-delegated-continuation-active-prompt-visibility` proves:
  - delegated continuation is represented as runtime-local intake truth
  - active runtime can show it as already consumed into the current prompt
  - after runtime stop, the same delegated continuation returns to pending visibility

3. delegated continuation can later be absorbed into manager continuity

- `test-freely-manager-delegated-intake-absorption-closure` proves:
  - delegated continuation may first sit at `handoff://continuation`
  - later manager continuity publication can close the intake as `STATUS="absorbed"`
  - final writeback may point to `continuity://manager-supervision` and a continuity artifact rather than a `pre-brainstorm`

4. direct-answer / control handling can close without canonical repo materialization

- `test-freely-interruption-direct-answer` proves:
  - narrow control queries can be answered and absorbed directly by the interruption control plane
  - control/cleanup signals can also become delegated runtime handoff via `handoff://cleanup` without pretending that a new `pre-brainstorm` was created

### 4. `dropped` exists in runtime truth, but is not yet the first validated contract path

Current code already accepts and persists `STATUS="dropped"` at intake-resolution time.

But current family evidence is still stronger for:

- absorbed into `pre-brainstorm`
- delegated continuation / cleanup handoff
- direct-answer absorption
- manager-continuity absorption

So the first slice should acknowledge `dropped` as a real runtime status without overclaiming that its source-facing closure semantics are already as well proven as the other paths above.

Implication:

- this family already has multiple legitimate terminal or transitional outcomes
- the first slice must preserve those distinctions
- any shared source-facing contract must be derived from these tested paths rather than replacing them

## Family Responsibilities By Layer

### 1. Front-door intake layer

Owns only real operator input from:

- `freely chat`
- CLI human message submission
- future local input-box style message submission

This layer decides only:

- was there a real human message
- did it get durable local persistence
- is it still unresolved for manager attention

It does not yet decide:

- whether the message deserves new canonical repo docs
- whether it should become an external/public issue

### 2. Runtime routing layer

Owns:

- claim / classify / delegate / absorb / drop
- interruption-manager triage
- direct-answer handling
- runtime-local continuation or cleanup handoff
- recovery when triage claim or supervision writeback was interrupted

This layer may finish an interruption entirely without creating a source record that survives into repo lifecycle truth.

### 3. Canonical owner handoff layer

Owns only the moment when a human interruption is judged to become a governed problem-source.

At that point the family must write enough linkage to say:

- if this interruption became a governed problem-source, it was consumed by which `pre-brainstorm`
- if it was closed by runtime/control/continuity handling instead, that closure stays family-local runtime truth rather than shared source consumption

After that, candidate / milestone / issue work belongs to the downstream owner, not to this family.

## Lifecycle View

For this family, the relevant loops are:

1. source loop

- human message arrives
- runtime persists a durable local intake record
- manager sees unresolved human-interruption view
- message is judged as governed problem, continuation/control handoff, or noise
- only governed-problem consumption should point to a `pre-brainstorm`

2. runtime loop

- claim / resolve / cleanup / restart recovery
- local durability across runtime restart
- manager-readable unresolved surface without forcing repo writes from protected root
- direct answer and runtime-only closure remain legal terminal outcomes for this family
- delegated continuation / cleanup handoff remains runtime truth until later owner closure

3. owner loop handoff

- once consumed into `pre-brainstorm`, later candidate / milestone / issue work leaves this family line
- if absorbed into manager continuity or runtime control, later closure also leaves this family line without pretending that a new pre-brainstorm was created

## Loop Boundary Clarification

The main governance risk is mixing three different meanings of "unresolved":

1. unresolved human interruption needing manager attention
2. unresolved governed problem-source not yet consumed into `pre-brainstorm`
3. unresolved downstream owner lifecycle after a `pre-brainstorm` already exists

These must not collapse into one file or one status word.

For this family, the safest reading is:

- `.freely/intake/**` remains runtime truth for interruption lifecycle
- a future small unresolved source view, if introduced, should be derived from or linked to that runtime truth
- downstream `pre-brainstorm` / candidate / milestone unresolved state must stay in their own canonical artifacts

## Current Durable Shapes

The current family already stores two distinct local artifact shapes:

1. raw intake item

- path family: `.freely/intake/<intake_id>/`
- durable fields already include author/channel/message/status/classification/reaction/linkage/claim/session/delegation

2. interruption resolution artifact

- path family: `.freely/run/interruption-resolution/<intake_id>/`
- durable fields already include resolved_by/reaction/classification/absorption_target/status plus human-readable resolution content

This matters because any future "source inbox" shape cannot assume there is only one local document per interruption.

## Unresolved Record Shape Questions

If a first-slice unresolved source view is added for this family, the open shape questions should be narrowed to:

1. Which fields are required on the unresolved view itself?

- `source_family`
- `source_id`
- `source_origin`
- `created_at`
- `unresolved_state`
- `consumption_target` or `pending_reason`
- pointer back to runtime truth

2. Which fields must stay only in runtime-local intake truth?

- `claimed_by`
- `claimed_at`
- detailed routing status such as `classified` or `delegated`
- local re-entry / delegated worktree / session-reactivation details

3. Which fields belong only in downstream canonical artifacts?

- substantive analysis
- candidate acceptance boundary
- milestone planning
- issue-level execution state

The guiding constraint is:

- unresolved source shape should be source-like and small
- runtime intake shape can remain richer because it is already carrying routing and recovery truth
- this field set stays family-local and provisional until umbrella validation proves a reusable subset

## First-Slice Direction

The first implementation slice should be deliberately narrow:

1. Keep semantic boundary strict:

- only real human/operator input
- no AI-discovered problems
- no GitHub publication lane

2. Preserve runtime truth:

- keep `.freely/intake/**` as current lifecycle truth for claim / delegate / absorb / recovery
- do not flatten existing statuses into only `unconsumed | consumed`

3. Add only the smallest missing layer:

- either a manager-facing unresolved overlay/index derived from current intake truth
- or a thin adapter document that points back to current intake truth

4. Backstop only the real absorption boundary:

- if a human interruption is claimed to be consumed into a `pre-brainstorm`, unresolved visibility must clear
- if it is direct-answer/runtime-local/control-only, unresolved visibility must also clear without forcing repo doc creation
- any umbrella hook/gate backstop should validate only repo-visible governed-problem absorption claims, not generic runtime-local closure churn

## Preliminary Direction

At current evidence level, this line looks more like:

- adapter / overlay / narrowing refactor

than:

- replacement of current `.freely/intake/**` runtime family

The burden of proof should stay on any proposal that wants to rehome the family completely into a new generic source-inbox storage layer.

## Open Questions

1. What is the minimal unresolved-view shape for this family without duplicating full runtime intake truth?
2. Should `.freely/intake/**` remain the family-local truth, with only a manager-facing overlay index?
3. Which interruption outcomes remain runtime-local/control-local and never become governed problem-sources?
4. When an interruption is consumed into an existing `pre-brainstorm`, what linkage fields are minimally required?
5. What exact unresolved-removal invariant should hold for direct answer, delegated continuation, delegated cleanup, and pre-brainstorm consumption respectively?
6. Which checks belong in this family contract versus the umbrella source-governance backstop, and which must never be promoted beyond family-local runtime closure evidence?

## Initial Conclusion

- This family should get its own dedicated worktree.
- It should be the first implementation slice, because current runtime truth already exists.
- It must be kept semantically pure: real human interruption only.
- The likely first slice is an adapter/overlay over existing runtime intake truth, not a replacement lifecycle.
