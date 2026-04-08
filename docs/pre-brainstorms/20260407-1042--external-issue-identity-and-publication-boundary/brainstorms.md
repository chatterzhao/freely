# Brainstorm - 20260407-1042--external-issue-identity-and-publication-boundary

## Context

- This follow-up line exists because durable source contraction changed what `external issue` must carry.
- `external issue` is now the family that should absorb:
  - user-created GitHub issue style inputs
  - AI-discovered problems that deserve formal external issue handling
- older GitHub issue pre-research already explored scan/create/sync/mapping, but it mixed source consumption, public mirroring, and internal owner truth too broadly.

## Problem

Freely needs a clean external-issue model that separates source identity, internal canonical ownership, and public progress mirroring.

Without that split:

- GitHub issue can become an overloaded object with conflicting roles
- AI-discovered problems can be routed inconsistently
- labels and sync rules can collapse unrelated semantics into one field

## Responsibility Boundary

This line owns:

- what counts as `external issue` after source-family contraction
- how user-created external issues enter the source loop
- how AI-discovered durable problems enter the external-issue flow
- whether source issue, public tracking issue, and canonical internal owner are one object or multiple mapped objects
- mapping, identity, sync, label, comment, and closeout rules for external issue publication

This line does not own:

- generic unresolved-index semantics shared by all durable families
- human interruption runtime UX
- candidate / milestone / issue internal canonical truth itself

## Lifecycle View

For this family, the loops should be separated explicitly:

1. source loop

- external issue exists or is created
- unresolved source is consumed into `pre-brainstorm`

2. owner loop

- internal canonical truth remains `pre-brainstorm` -> candidate -> milestone / issue / progress

3. publication loop

- external source issue writeback
- optional or required public tracking issue
- status/comment/closeout synchronization to external surfaces

## Open Questions

1. Should AI-discovered durable problems always create an external issue, or only when publication policy allows it?
2. Should source issue and public tracking issue be the same GitHub object or distinct mapped objects?
3. Which labels represent identity, which represent publication role, and which represent public status?
4. Which internal owner transitions deserve external writeback, and which are too noisy?
5. How should the old `20260403-1000--external-issue-integration-and-self-evolution` material be retained, split, or superseded?

## Initial Conclusion

- This family must get its own dedicated worktree.
- It should not be solved inside the umbrella source-governance line.
- It should treat old GitHub issue research as input, not as frozen truth.
