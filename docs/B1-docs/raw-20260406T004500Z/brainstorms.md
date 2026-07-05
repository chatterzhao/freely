# Brainstorm: governance-check protected-merge history source policy

- started_at: `2026-04-06`
- problem_type: `governance-regression`
- trigger: `post-merge followthrough on develop`

## Context

- `develop` accepted guarded merge `8e0985b` from `test-pre-merge-20260406-0035-cli-wrapper-regression-closeout`.
- Running `./bin/governance-check` immediately afterward failed on nested merge commit `ab7a9b8`, even though that commit belongs to the temporary `test-pre-merge-*` batch rather than a direct `develop` merge.
- The failure path shows `governance-check` is scanning protected merge history without constraining it to the branch's first-parent lineage.

## Why This Matters

- This is a real false negative on canonical `develop`, so it blocks normal post-merge followthrough and makes successful guarded promotion look invalid.
- The bug specifically hits the new test-pre-merge family promote model, so it directly undermines the governance the repo just froze.

## Direction

1. Materialize a narrow owner for `governance-check` protected-merge history scanning.
2. Change protected-branch receipt auditing to use first-parent merge history for each audited branch.
3. Add a regression that reproduces `feature/* -> test-pre-merge-* -> develop` ancestry and proves `develop` only validates its own canonical merge receipt.
