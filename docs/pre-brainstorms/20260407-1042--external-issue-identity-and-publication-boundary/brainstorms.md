# Brainstorm - 20260407-1042--external-issue-identity-and-publication-boundary

## Context

- This follow-up exists because the repo has contracted the default durable source families to `human interruption` and `external issue`.
- `external issue` must now cover two bounded inputs:
  - user-created GitHub issue style inputs
  - AI-discovered problems that should formalize into the external-issue flow
- The older `20260403-1000--external-issue-integration-and-self-evolution` line already explored scan/create/sync/mapping, but it predated the newer source-family contraction and mixed unrelated concerns into one package.

## Problem

Freely needs an external-issue model that is governance-compatible with the current three-loop lifecycle and does not overload one GitHub object with three different jobs:

1. durable source identity
2. internal canonical owner truth
3. public progress publication

If those jobs stay collapsed:

- user-created issues and AI-discovered problems will enter with different hidden rules
- GitHub labels will be forced to carry identity, routing, and status all at once
- repo docs may drift toward “GitHub is the truth source”
- runtime and manager lanes may start assuming GitHub writeback automation already exists

## Strict Boundary

This line owns only the external-issue family pre-research:

- external-issue identity after source-family contraction
- source-loop intake rules for user-created GitHub issue style inputs
- source-loop formalization rules for AI-discovered problems that deserve external issue treatment
- mapping among source object, optional public-tracking object, and internal owner
- publication policy, writeback boundaries, and label taxonomy dimensions

This line does not own:

- human interruption semantics
- generic unresolved-index or source-ledger implementation
- milestone / issue / progress as internal canonical truth
- runtime automation that assumes GitHub create/sync already ships today
- broad self-evolution scheduling beyond the external-issue family

## Loop Separation

### 1. Source loop

Purpose:
- answer “what durable external object caused this problem to enter the system?”

Canonical responsibilities:
- identify the external source object when one already exists
- decide when an AI-discovered problem qualifies for external-issue formalization
- capture minimum external lineage without claiming that GitHub is the owner of the work
- hand the problem into `pre-brainstorm`

Source-loop truth should answer:
- `source_kind`
  - `user_external_issue`
  - `ai_formalized_external_issue`
- `source_platform`
  - `github` first
  - future external trackers only as siblings, not mixed into the same first slice
- `source_locator`
  - stable repo / org / number / url style identity if an external object already exists
- `formalization_reason`
  - only for AI-discovered problems that are being turned into external-issue lineage

Hard boundary:
- source-loop intake does not decide internal owner phase beyond “enter pre-brainstorm”

### 2. Owner loop

Purpose:
- answer “what is the canonical internal owner and phase?”

Canonical responsibilities:
- `pre-brainstorm -> candidate -> milestone -> issue -> progress/recovery`
- carry actual owner truth, acceptance, implementation, verification, and cleanup state

Hard boundary:
- owner loop remains repo-doc-native
- GitHub issue state must never replace `candidates.md`, `milestones.md`, issue docs, `progress`, or `recovery`

### 3. Publication loop

Purpose:
- answer “what, if anything, should be mirrored back to external public surfaces?”

Canonical responsibilities:
- decide whether an external source issue gets comments, labels, closeout, or no writeback
- decide whether a separate public tracking issue should exist
- define what internal transitions are quiet, summarized, or externally visible

Hard boundary:
- publication loop mirrors internal truth; it does not become internal truth

## Re-review Of 20260403-1000

### Useful parts to preserve

The older line was directionally useful in several ways:

- it correctly noticed that source issue identity and a Freely-created tracking issue may be different objects
- it usefully explored explicit mapping rather than assuming one GitHub issue can do every job
- it identified that labels need dimensions, not one flat overloaded status string
- it treated candidate/pre-brainstorm as internal and not automatically public

Those are still good inputs for this family.

### Parts that are now too broad or unsafe

The older line also bundled decisions that should no longer stay together:

- it mixed user-created external issues, AI-discovered problems, and Freely self-evolution scheduling into one owner family
- it treated “create milestone issue on GitHub” as if that were the default next step once an internal owner is accepted
- it assumed broad GitHub status mirroring as if external publication were always on
- it implied GitHub labels could stand in for lifecycle ownership and consumption control
- it proposed `.freely/github-issue-mapping.json` too early, before proving what minimum local durable mapping is actually required
- it widened the family to Gitee / multi-platform abstraction before the GitHub-first boundary was stable

### Fair conclusion

The old line should be preserved as exploratory input, not treated as discarded noise. But its conclusions are not yet governance-safe enough to promote directly.

## Identity Model Draft

The external-issue family should distinguish three identities:

1. `source issue`
- the external durable object that originally exposed the problem
- may be user-created
- may be absent for AI-discovered problems

2. `internal owner`
- the canonical repo-native owner in `pre-brainstorm / candidate / milestone / issue / progress`
- always required once the problem becomes durable inside Freely

3. `publication target`
- the external object used for public progress mirroring
- may be:
  - the same as the source issue
  - a separate Freely-created public tracking issue
  - absent when publication policy says “internal only”

Key rule:
- equality among these three identities must be a policy decision, never a default assumption

Recommended invariants for the first bounded model:

- one canonical `internal owner` may map to zero or one `source issue`
- one canonical `internal owner` may map to zero or one `publication target`
- a `source issue` may exist without any public-tracking split
- a `publication target` may exist without any original source issue when the problem was AI-discovered first
- no external object may become the canonical owner truth for milestone routing, `phase_state`, or progress evidence

## Mapping Model Draft

The family should research a minimum conceptual mapping first, before freezing storage:

- `source_ref`
  - nullable only for AI-discovered formalized problems
- `internal_owner_ref`
  - required once the problem reaches candidate
- `publication_ref`
  - nullable when publication is off
- `publication_mode`
  - `none`
  - `source_only`
  - `separate_tracking_issue`

The mapping contract should support these cases:

1. User-created GitHub issue reused as both source and public surface
2. User-created GitHub issue kept as source, while Freely creates a separate public tracking issue
3. AI-discovered problem with no source issue, but later published as a new public tracking issue
4. AI-discovered problem kept fully internal with no GitHub writeback

Boundary implication:

- mapping semantics must be frozen before storage semantics
- the first slice can stay storage-agnostic if the invariants are explicit

## Label Taxonomy Draft

The old line was right that labels need dimensions, but the dimensions should be separated more carefully.

### A. Identity / role labels

These answer “what kind of external object is this?”

- `freely:external-source`
- `freely:public-tracking`
- `freely:source-platform:github`
- future platform labels only after GitHub-first semantics are stable

### B. Publication-policy labels

These answer “why is this object public and what kind of writeback is allowed?”

- `freely:publication:mirror`
- `freely:publication:tracking`
- `freely:publication:internal-origin`
- `freely:publication:restricted`

### C. Public-status labels

These answer “what public-facing progress state is being mirrored?”

- bounded public states such as:
  - `freely:public-status:triaged`
  - `freely:public-status:in-progress`
  - `freely:public-status:blocked`
  - `freely:public-status:completed`

Critical rule:
- public-status labels are a publication surface only
- they must not replace internal `phase_state`

## Publication Policy Draft

The family should not assume that every durable problem gets published.

### Publish by policy, not by existence

AI-discovered problems should enter the external-issue family only when at least one of these is true:

- the problem is user-visible and should be publicly tracked
- the problem affects a published contract and needs an external explanation surface
- the human/operator explicitly requests external publication
- a standing policy for this repo or owner family says that this class of problem must be public

Otherwise:
- keep the canonical owner internal
- preserve the external-issue family semantics as “publication-capable”, not “always publish”

This also means:

- user-created external issue does not imply “separate tracking issue required”
- AI-discovered durable problem does not imply “must publish to GitHub”
- publication remains a policy gate owned by the internal owner loop

### Source issue writeback boundaries

Safe candidates for source-issue writeback:

- “received / triaged into pre-research”
- “accepted into a canonical internal owner”
- “completed / resolved / closed out”

Unsafe by default:

- every internal phase transition
- noisy worktree details
- raw runtime failures
- every intermediate checkpoint

### Separate public tracking issue boundaries

A separate public tracking issue should be considered only when:

- the source issue is user-authored and should remain the original report, not Freely's full progress ledger
- multiple internal owners may roll up into one public progress thread
- Freely needs a cleaner public narrative than the source issue can support

## GitHub Writeback Boundary

Current repo truth does not justify claiming that GitHub issue create/sync is implemented runtime capability today.

Therefore this line should freeze these boundaries:

- allowed in pre-research:
  - define conceptual mapping
  - define publication policy
  - define candidate/issue fields that future implementation would need
- not allowed in pre-research:
  - assume runtime or manager already performs GitHub create/sync/comment/close automatically
  - describe missing runtime automation as if it were an execution bug
  - force storage or API abstraction decisions before first-slice ownership is stable

## Concrete Questions To Settle Before Promotion

1. When an AI-discovered problem becomes `ai_formalized_external_issue`, what minimum evidence justifies that formalization?
2. For GitHub-first, what minimum `source_ref` fields are required before any local storage shape is frozen?
3. When should a source issue be reused as the publication target versus split into a separate tracking issue?
4. Which public-status vocabulary is small enough to stay stable while still useful?
5. Which internal transitions deserve publication, and which should remain invisible externally?
6. Does this family need a durable local mapping artifact at all before implementation, or is the first promotion target still pure policy/schema work?

## Initial Conclusion

- The family should stay pre-research-only for now.
- The next stable outcome should be a GitHub-first policy/schema owner, not immediate multi-platform automation.
- The older `20260403-1000` line should be retained as exploratory input, but its bundled conclusions should be split as follows:
  - keep: source-vs-tracking distinction, dimensional labels, mapping awareness
  - reject for now: default public mirroring, unconditional GitHub tracking issue creation, self-evolution scheduling in the same family, premature local storage freeze
- The most important promotion requirement is to make source loop, owner loop, and publication loop independently legible.
