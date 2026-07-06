# PRD: protected-branch-ref-only-entrypoint-enforcement-governance

## Problem

Protected branches can still move through ref-only local updates such as `git merge --ff-only`, which bypasses the existing merge-commit-only entrypoint gate and lets a protected branch advance to a non-receipted commit.

## Requirements

1. Protected branch refs must fail closed when the new head is not a canonical receipt-bearing protected merge commit.
2. The gate must run before the protected ref is updated.
3. Existing receipt-bearing protected merge commits must remain valid.
4. The repair must stay at the local ref-transaction boundary instead of widening into a generic protected-branch governance rewrite.

## Out Of Scope

1. Server-side enforcement
2. Push-direction policy redesign
3. Receipt-ledger redesign
4. Non-protected branch ref updates
