# PRD: github-first-external-issue-source-governance

## Problem

Freely now has a stable external-issue family contract in pre-research, but the consumer-facing routing truth still uses loose `github issue` language and does not yet freeze how raw external source issues are scanned, deduped, and closed out. That leaves later runtime work without a stable contract and encourages source/owner/publication collapse.

## Product Requirement

1. Freely must treat `external issue` as a first-class durable source family, with GitHub as the first bounded platform slice.
2. Raw external source scan must only consider open and unconsumed source issues.
3. Canonical repo-native linkage must stay the decisive dedupe authority.
4. Canonical docs must freeze discard closeout, accept-and-bind closeout, and policy-gated publication target rules.
5. The first consumer-facing source-routing docs must adopt this contract before runtime automation begins.

## Acceptance

1. Canonical docs freeze GitHub-first raw scan, metadata, dedupe, and closeout rules.
2. Source-routing skill docs and adjacent prompt truth adopt `external issue` terminology and family boundaries.
3. The owner lands as bounded governance truth on `develop` without claiming API automation already ships.
