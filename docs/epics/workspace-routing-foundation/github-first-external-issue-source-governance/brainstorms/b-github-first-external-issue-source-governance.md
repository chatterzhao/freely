# Brainstorm: github-first-external-issue-source-governance

## Goal

Materialize the bounded GitHub-first owner for external-source intake without widening into runtime API automation or multi-platform abstraction.

## Frozen Conclusions

1. `external issue` is the durable source-family term; `github issue` is only the first platform slice inside that family.
2. Raw source scan must cover only open and unconsumed source issues.
3. Canonical repo-native linkage is decisive dedupe truth; external labels/comments are mirrors or hints.
4. `source issue` is intake lineage and may equal `publication target` only when `publication_mode = source_only` and the source issue is suitable as the public progress surface.
5. Discard closes a user-created source issue with a reasoned issue comment.
6. Accept-and-bind closes the original source issue once canonical owner/publication linkage is durable.
7. The first consumer-facing truth should land in `context-source-skill` and adjacent prompt docs before runtime implementation begins.

## Rejected Alternatives

1. Keep the older loose `github issue` wording and defer family cleanup to runtime code later.
2. Treat all open GitHub issues as scan candidates forever.
3. Let external labels/comments become the only dedupe or closeout truth.
4. Open a multi-platform/Gitee abstraction owner before the GitHub-first contract is stable.

## Implementation Shape Chosen For Follow-On Owner

1. Freeze policy and language in `pre-brainstorm`, issue owner, and source-routing truth.
2. Update `context-source-skill`, `source-classification`, and lead-agent prompt truth to consume the `external issue` family.
3. Keep runtime/API automation explicitly deferred.
4. Open a later implementation owner for scan persistence, canonical metadata writing, and external closeout/writeback behavior.

## Guardrails

1. This owner does not claim external API behavior already exists.
2. This owner does not change whole-app three-loop semantics.
3. This owner keeps GitHub publication subordinate to canonical repo-native owner truth.
