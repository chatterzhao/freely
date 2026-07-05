# PRD: test-pre-merge-family-promotion-gate-enforcement-governance

## Goal

Synchronize governance truth sources and protected-branch promotion gates so Freely executes the new `test-pre-merge-*` family promotion model instead of keeping the old replay-only rules alive.

## Product Requirement

1. Freely must not keep separate truth for promote source semantics in docs and scripts.
2. Freely must make `test-pre-merge-*` the canonical `develop` promotion family while preserving `hotfix/* -> develop`.
3. Freely must block `feature/* -> develop` as a normal route once the new model is activated.
4. Freely must treat single-feature lanes and explicit multi-bundles as one canonical family prefix rather than adding another `test-pre-*` namespace.
5. Freely must keep lifecycle automation out of this owner.
