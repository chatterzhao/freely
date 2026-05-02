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

### Keep / Split / Reject Table

| Legacy idea from `20260403-1000` | Current disposition | Why |
| --- | --- | --- |
| Distinguish externally created source issue from Freely-created public tracking issue | Keep | This remains necessary to avoid collapsing source identity and publication target into one GitHub object by default. |
| Treat candidate / pre-brainstorm as internal rather than automatically public | Keep | This matches the current owner-loop boundary and prevents GitHub from becoming canonical owner truth too early. |
| Use labels with separate dimensions instead of one overloaded status word | Keep, but narrow | Dimensions remain useful, but only as publication/identity surfaces after loop separation is explicit. |
| Model explicit mapping among external object(s) and internal owner | Keep, but storage-agnostic first | The conceptual mapping survives, but `.freely/github-issue-mapping.json` is not frozen yet. |
| Scan open external issues and decide whether they are already consumed | Split | Family identity/intake rules stay here, but polling automation and concrete scan mechanics belong to a later GitHub-first owner once the contract is stable. |
| Mirror internal lifecycle to GitHub labels/comments/closeout | Split | Publication policy belongs here conceptually, but concrete sync timing and automation should wait until public-status vocabulary and writeback boundaries are stable. |
| Always create or update a GitHub milestone/tracking issue once an internal owner is accepted | Reject as default | Publication is policy-gated, not implied by internal acceptance. |
| Treat GitHub labels as lifecycle ownership or consumption truth | Reject | GitHub remains publication/source lineage, never canonical internal owner truth. |
| Bundle user-created external issues, AI-discovered problems, and Freely self-evolution scheduling into one family | Reject | Source-family contraction and three-loop separation now require these concerns to be separated. |
| Generalize immediately to Gitee / multi-platform abstraction | Reject for first slice | The bounded first slice is GitHub-first; broader platform generalization would freeze abstraction too early. |

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

### GitHub-first Minimal Field Contract Draft

The first bounded owner should not start with an abstract multi-platform schema. It should start with the smallest field contract that still lets policy and dedupe decisions be audited.

#### 1. `source_ref` minimum fields

For a GitHub-first source issue, the minimum source identity should be enough to answer “which external object was this?” without freezing storage format:

- `source_platform`
  - `github`
- `source_repo`
  - stable `owner/name` repository identity
- `source_number`
  - issue number
- `source_url`
  - canonical issue URL

Optional until later:

- source title snapshot
- source labels snapshot
- source author snapshot

Why this minimum is enough:

- `source_repo + source_number` gives a stable dedupe key
- `source_url` keeps human-auditable linkage simple
- delaying snapshots avoids freezing sync/cache behavior too early

#### 2. `internal_owner_ref` minimum fields

Once the problem is canonical inside Freely, the first bounded contract only needs:

- `owner_kind`
  - initially `pre_brainstorm`
- `owner_path`
  - canonical repo path to the consuming owner artifact

Later owner expansion into candidate / issue / progress can remain downstream truth rather than source-family requirements.

#### 3. `publication_ref` minimum fields

Only required when publication exists:

- `publication_platform`
  - initially `github`
- `publication_repo`
  - stable `owner/name`
- `publication_number`
  - issue number
- `publication_url`
  - canonical URL

If `publication_mode = none`, no placeholder fields should be invented.

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

## Formalization Decision Table Draft

The next bounded step should freeze decision cases before any storage or automation choice.

| Input situation | Does it enter `external issue` family? | `source_ref` expectation | `publication_ref` expectation | Minimum extra evidence to record |
| --- | --- | --- | --- | --- |
| User-created GitHub issue already exists and is accepted as a governed problem | Yes | Required | Optional | Source locator plus pre-brainstorm linkage and a dedupe/consumption marker |
| User-created GitHub issue exists, but the finding is absorbed inside the current owner line and does not create a new governed problem | No new durable source | Existing external object stays outside this family handoff | None by default | Current-line absorption evidence only; do not create duplicate external-source lineage |
| AI-discovered problem should stay internal-only for now | No | None | None | Internal owner evidence plus explicit internal-only formalization reason |
| AI-discovered problem needs durable external-source lineage but no public tracking yet | Yes | Required after formalization | None initially | Formalization reason plus linkage to canonical internal owner |
| AI-discovered problem needs immediate public tracking | Yes | Required after formalization | Required | Formalization reason, canonical owner linkage, and publication-policy basis |

Two hard rules follow:

- entering the `external issue` family is a policy decision, not the default fate of every AI-discovered problem
- publication target creation is a second policy decision layered on top of external-source formalization, not proof that the source family itself owns internal truth

### Formalization Invariants

The first bounded policy slice should freeze these invariants explicitly:

1. User-created external issues

- if an external issue already exists and a genuinely independent governed problem is accepted, the family may carry that object as `source_ref`
- if the finding is still absorbable inside the current owner line, no new external-source formalization occurs
- a reused `source issue` does not automatically become `publication target`

2. AI-discovered problems

- AI discovery alone is insufficient to enter the `external issue` family
- formalization requires an explicit policy basis such as user-visible impact, contract-facing explanation duty, operator request, or standing publication policy
- when the problem stays internal-only, the required evidence belongs on the internal owner side, not as a fake external-source placeholder

3. Publication

- publication policy is evaluated only after or alongside source-family formalization
- publication may stay `none` even when external-source lineage exists
- no publication decision may rewrite canonical internal owner truth

## Consumption / Dedupe Evidence Draft

The old `20260403-1000` line was directionally right that external-source re-scan must avoid repeated consumption. The updated line should keep that requirement, but freeze it as a minimal evidence contract rather than a premature implementation.

What still needs to be made explicit:

- what minimum evidence lets future scan/manager paths conclude that a user-created external issue has already been consumed into `pre-brainstorm`
- whether that evidence lives only in canonical repo docs, only on the external object, or in a bounded combination
- which publication-side comments/labels are optional mirrors versus required dedupe evidence

Current safe direction:

- repo-native owner artifacts remain canonical for internal truth
- external comments/labels may mirror that truth, but should not be the sole evidence that prevents re-consumption
- the first slice should freeze the minimum dedupe/consumption invariant before choosing automation timing or storage layout
- publication remains a policy gate owned by the internal owner loop

### Minimum Dedupe / Consumption Contract

The smallest governance-safe contract currently looks like this:

1. Canonical evidence

- once a user-created external issue is consumed into `pre-brainstorm`, canonical repo-native truth must record:
  - source-family = external issue
  - source locator or equivalent `source_ref`
  - the consuming `pre-brainstorm`

#### Canonical linkage minimum

The smallest repo-native linkage that should count as decisive dedupe authority is:

- `source_family: external_issue`
- a GitHub-first `source_ref` containing at least `source_platform`, `source_repo`, `source_number`, and `source_url`
- `owner_kind: pre_brainstorm`
- `owner_path: <canonical pre-brainstorm path>`

If that linkage exists in canonical owner truth, future scans should treat the source as already consumed even if external mirrors lag.

2. Scan-safe dedupe rule

- future scan/manager paths must treat canonical repo-native linkage as the decisive evidence that the external source is already consumed
- external labels/comments may help operators, but they are mirrors, not the only dedupe authority

3. Optional external mirrors

- comments, labels, or closeout on the external object may mirror one of:
  - entered pre-research
  - linked to canonical owner
  - externally completed
- but omission or delay of those mirrors must not cause the same source issue to be re-consumed if canonical linkage already exists

4. No premature storage freeze

- this contract does not yet require a dedicated mapping file, queue file, or API cache shape
- storage/automation choices stay downstream of the policy invariant

## Raw External Source Scan Contract Draft

The first GitHub-first scan contract should stay narrow and auditable. It should not attempt to ingest every open issue.

### Scan eligibility

A raw GitHub issue is scan-eligible only when all of the following are true:

- the issue is open
- the issue is not already bound by canonical repo-native linkage to a consuming owner
- the issue does not already advertise a canonical milestone/publication handoff that Freely can verify

The practical intent is:

- scan raw source issues that are still open and still appear unconsumed
- do not rescan already-consumed source issues just because external labels/comments are stale
- do not treat all open GitHub issues as fresh intake forever

### Decisive authority versus hints

For scan eligibility, these signals should be interpreted in this order:

1. canonical repo-native linkage
- decisive authority
- if a canonical owner already records the source issue, scanning must treat the source as consumed

2. verifiable external linkage to a canonical milestone/publication target
- supportive evidence only
- useful when canonical linkage is being audited or manually repaired

3. raw labels or human-authored status text on the source issue
- hint only
- must not override canonical truth

### Suspicion rule

Freely should distrust AI-written external status mirrors enough to re-check canonical owner truth before acting.

That means:

- a missing external comment/label does not prove the source is fresh
- an old “triaged” label does not prove the source is still active
- a stale “linked” comment should be revalidated against canonical owner artifacts before skipping or re-consuming the issue

## Canonical Source Metadata Draft

The source family now needs a minimum canonical metadata contract that can survive scan, pre-research, discard, accept, and external publication decisions without forcing a storage file format.

### Minimum canonical fields

These fields should be stable enough to require on the canonical owner side once a source issue is consumed:

- `source_family`
  - `external_issue`
- `source_kind`
  - `user_external_issue`
  - `ai_formalized_external_issue`
- `source_platform`
  - `github` in the first slice
- `source_ref`
  - GitHub-first locator containing at least `source_repo`, `source_number`, and `source_url`
- `source_observed_state`
  - the last observed source-side state relevant to intake, such as `open`
- `source_consumption_state`
  - bounded source-family consumption state, distinct from owner `phase_state`
- `owner_kind`
  - initially `pre_brainstorm`
- `owner_path`
  - canonical repo path to the consuming owner artifact
- `publication_mode`
  - `none`
  - `source_only`
  - `separate_tracking_issue`

### Optional but explicitly non-required in the first slice

- label snapshots
- title/body snapshots
- author snapshots
- API cache timestamps beyond what a later implementation owner may need

### Why `source_consumption_state` is separate

The source family needs a small state word for answering “has this source been consumed and what happened to it?” without overloading:

- owner `phase_state`
- public-status labels
- publication policy

The bounded state set should stay minimal:

- `fresh`
- `consumed_pre_brainstorm`
- `discarded`
- `accepted_bound`

Interpretation:

- `fresh` means scan-eligible if no canonical linkage disproves freshness
- `consumed_pre_brainstorm` means the source has entered pre-research and should not be re-consumed
- `discarded` means pre-research decided not to continue and source closeout should be auditable
- `accepted_bound` means the source has been accepted into a canonical owner/publication handoff and should no longer behave like raw intake

## Source Lifecycle Decision Contract Draft

The family now needs an explicit answer for what happens to the source issue after pre-research.

### 1. Consume into pre-brainstorm

When a raw external issue is first accepted for pre-research:

- create or reuse the canonical `pre-brainstorm` owner
- record canonical source metadata on that owner
- move `source_consumption_state` to `consumed_pre_brainstorm`
- optional external writeback may say the issue has entered pre-research

At this point the source issue remains open, because the triage outcome is not known yet.

### 2. Pre-research discard

When pre-research concludes the problem should not continue:

- update canonical owner truth with discard reasoning
- move `source_consumption_state` to `discarded`
- if the source was a user-created GitHub issue, close that source issue with a reasoned closeout comment

Hard rule:

- discard of a user-created source issue should close the source issue rather than leaving it indefinitely “triaged”

### 3. Pre-research accept into milestone-owned followthrough

When pre-research accepts the problem and a canonical milestone-owned owner is created:

- keep the local milestone/issue docs as canonical truth
- associate the source issue with that canonical owner
- choose `publication_mode`
- if publication policy says the milestone should exist on GitHub/Gitee, create or bind the publication target
- move `source_consumption_state` to `accepted_bound`

For user-created source issues:

- once the canonical owner/publication target linkage is durable, close the original source issue
- the closeout comment should link to the canonical owner and, when present, the public milestone tracking issue

Hard rule:

- the original source issue is intake, not the long-running execution ledger

### 4. AI-formalized external issue

When an AI-discovered problem is intentionally formalized into external-source lineage:

- canonical owner truth must record `source_kind = ai_formalized_external_issue`
- a synthetic or newly created external source/publication target must not be used as a substitute for internal owner truth
- if publication is off, the canonical owner may still carry external-source lineage with `publication_mode = none`

## Publication Target Creation Draft

The first slice should freeze when public milestone/tracking issue creation is allowed.

### When to create a public milestone tracking issue

Creation is justified only when all of these are true:

- pre-research has accepted the problem into milestone-owned followthrough
- publication policy says this work should be externally visible
- the source issue itself is not a good long-running public progress surface

Typical reasons include:

- the source issue should remain the original report rather than a changing implementation ledger
- the external audience needs a stable progress thread for milestone-level followthrough
- Freely needs to aggregate or summarize progress more cleanly than the source issue can support

### Default publication posture

The default should remain:

- no public milestone issue before pre-research acceptance
- no public milestone issue when publication policy is `none`
- no separate public milestone issue when `source_only` is sufficient

### Local-to-public association contract

Once a public milestone tracking issue exists, canonical owner truth should be able to answer:

- which local milestone/issue owns the work
- which external object is the original source issue, if any
- which external object is the public milestone tracking issue, if any

The first slice does not need to freeze a mapping file, but it does need to freeze the association fields conceptually.

### Reuse policy: when `source issue` may equal `publication target`

The GitHub-first rule should be:

- allow equality only when `publication_mode = source_only`
- require an explicit judgment that the source issue is suitable as the public progress surface

Suitability means all of the following:

- the source issue can carry brief progress comments without harming the original report
- there is only one canonical owner thread being presented externally
- no cleaner separate narrative is needed for milestone-level followthrough

If any of those fail:

- keep the source issue as intake lineage only
- choose `publication_mode = separate_tracking_issue` if public tracking is still required

## Minimum Public-Status Vocabulary Decision

The first bounded vocabulary should stay at four states:

- `triaged`
- `in-progress`
- `blocked`
- `completed`

Why this is sufficient:

- `triaged` covers consumed/accepted public acknowledgment without leaking owner internals
- `in-progress` and `blocked` cover the only two externally meaningful execution distinctions needed early
- `completed` covers externally visible closeout

Why nothing else should be added yet:

- anything finer starts shadowing internal `phase_state`
- early automation does not need a richer publication vocabulary to be correct
- a larger set would make stale-mirror handling harder, not easier

## Source Closeout And Comment Placement Draft

### Comment versus discussion

The default external writeback surface should be issue comments, not GitHub Discussions.

Reason:

- the source issue itself is the durable intake object
- comments preserve auditability on that exact object
- discussions are too detached to serve as the default linkage surface for source consumption or closeout

Therefore:

- pre-research consumption notice should go to an issue comment if any writeback occurs
- discard rationale should go to an issue comment before closing
- accept-and-bind closeout should go to an issue comment that links forward to the canonical owner and optional public milestone issue

### What belongs in the comment

The comment should stay summary-level:

- acknowledgement that Freely consumed the source
- discard reason or acceptance/binding result
- link to the canonical owner artifact and optional public milestone tracking issue

The full pre-research document should remain canonical repo-native truth. The external comment links to it; it does not replace it.

## Canonical Metadata Placement Decision

Canonical source metadata should have one authoritative write location and one bounded mirror.

### Authoritative location

The consuming `pre-brainstorm` is the first authoritative owner of source metadata:

- it records source family, source locator, source consumption state, and publication mode
- it records the first durable link that proves the raw source issue has been consumed

### Acceptance mirror after milestone binding

After pre-research accepts the problem into milestone-owned followthrough:

- mirror a reduced linkage into the milestone/issue owner
- keep the authoritative intake record on the original `pre-brainstorm`

The reduced mirror should include only what later replay needs:

- source family
- source locator
- source/publication association
- forward link to the original pre-research owner

This gives later replay two safe properties:

- scan and closeout logic can still verify the accepted source from the active owner line
- the pre-research artifact remains the first durable intake truth rather than being rewritten away

## Testable Contract Draft

The candidate is only promotion-ready if later implementation can prove these scenarios without appealing to hidden operator judgment:

1. raw user-created GitHub issue
- scan sees open/unconsumed source
- source is consumed into `pre-brainstorm`
- canonical metadata records source linkage
- source is not re-consumed on the next scan

2. discarded user-created GitHub issue
- pre-research records discard reasoning
- source issue is closed with a reasoned comment
- later scan no longer treats it as fresh intake

3. accepted user-created GitHub issue with separate publication target
- pre-research accepts the problem
- milestone/publication target is bound
- original source issue is closed with forward links
- canonical owner remains the decisive truth

4. AI-discovered internal-only problem
- problem stays outside external publication
- canonical owner records internal-only reasoning
- no fake external-source placeholder is invented

5. stale external mirror
- an outdated label/comment on GitHub does not override canonical repo-native linkage
- scan still avoids re-consuming the source when canonical linkage exists

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

1. Which internal transitions deserve publication, and which should remain invisible externally?
2. Does this family need a durable local mapping artifact at all before implementation, or is the first promotion target still pure policy/schema work?

## Initial Conclusion

- The family should stay pre-research-only for now.
- The next stable outcome should be a GitHub-first policy/schema owner, not immediate multi-platform automation.
- The older `20260403-1000` line should be retained as exploratory input, but its bundled conclusions should be split as follows:
  - keep: source-vs-tracking distinction, dimensional labels, mapping awareness
  - reject for now: default public mirroring, unconditional GitHub tracking issue creation, self-evolution scheduling in the same family, premature local storage freeze
- The most important promotion requirement is to make source loop, owner loop, and publication loop independently legible.

## Bounded Owner Target Draft

The work completed so far is now strong enough to describe the next bounded owner without pretending implementation should start immediately.

### What the next bounded GitHub-first policy/schema owner should own

- GitHub-first `source_ref` minimum field contract
- canonical repo-native owner linkage required for dedupe
- formalization decision rules for:
  - user-created external source accepted as a governed problem
  - AI-discovered problem kept internal-only
  - AI-discovered problem formalized into external-source lineage without publication
- explicit rule that publication is optional and separate from source-family formalization
- the smallest writeback boundary language needed so later automation cannot reinterpret GitHub as internal truth

### What it should explicitly not own yet

- GitHub API automation
- comment/label sync timing implementation
- mapping-file or cache-file storage format
- multi-platform abstraction
- full public-status vocabulary beyond the smallest bounded set needed to avoid blocking policy promotion

### Why the owner is now bounded enough

- source identity, dedupe authority, and internal-owner primacy are now explicit enough to survive promotion
- remaining open questions are mostly publication-policy refinements, not existential uncertainty about source-family shape
- implementation still lacks a safe target unless this bounded owner freezes the policy/schema surface first

### Remaining blockers before promotion

The existential blockers are now mostly closed. What remains is implementation slicing rather than family shape:

- decide whether internal-only AI formalization needs any additional canonical owner field beyond the already-frozen reasoning requirement
- decide whether a first implementation can stay document-driven or needs a dedicated local mapping artifact immediately
