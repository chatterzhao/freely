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
- the local interruption record shape before consumption
- unresolved human-interruption visibility for manager routing
- claim / resolve / absorb transitions at runtime level
- how a consumed interruption points to `pre-brainstorm`
- how direct-answer or runtime-only interruption handling avoids fake canonical materialization

This line does not own:

- AI-discovered problem publication
- GitHub issue creation
- external issue identity or label taxonomy
- milestone/public progress sync

## Lifecycle View

For this family, the relevant loops are:

1. source loop

- human message arrives
- judged as durable governed problem or not
- if yes, it enters unresolved human-interruption view
- if consumed, it points to a `pre-brainstorm`

2. runtime loop

- claim / resolve / cleanup / restart recovery
- local durability across runtime restart
- manager-readable unresolved surface without forcing repo writes from protected root

3. owner loop handoff

- once consumed into `pre-brainstorm`, later candidate / milestone / issue work leaves this family line

## Open Questions

1. What is the minimal human interruption record schema after contraction?
2. Should `.freely/intake/**` remain the family-local truth, with a manager-facing overlay index?
3. Which interruption outcomes remain runtime-local and never become durable sources?
4. When an interruption is absorbed into an existing `pre-brainstorm`, what writeback fields are minimally required?
5. Which gate checks belong here versus the umbrella source-governance backstop?

## Initial Conclusion

- This family should get its own dedicated worktree.
- It should be the first implementation slice, because current runtime truth already exists.
- It must be kept semantically pure: real human interruption only.
