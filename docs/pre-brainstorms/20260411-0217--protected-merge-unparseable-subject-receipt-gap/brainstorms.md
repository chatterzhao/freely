# Brainstorms - 20260411-0217--protected-merge-unparseable-subject-receipt-gap

## Context

- `./bin/governance-check` on `develop` still fails on `2026-04-11` for six historical protected-ancestry merges in the `test-pre-merge-20260410-preferred-auth-fix` batch:
  - `357c18bb39286580a9c07856d0a1858867dd7d58`
  - `8069bced62af4dc1e6c46387fa715613628f291a`
  - `497c474abd9ecb4776462aa9416b59f7cc45a1f8`
  - `c235976621a36a1f89db5dda83676d3b4370278d`
  - `ae09968a60d722deb11e59ca43b1239dab694c5c`
  - `88dd9eaabbcda45b2b7127da7dea9ec3f68e4df2`
- These commits are ordinary merge commits that later became reachable from protected ancestry, but their subjects are generic (`Merge`, `Merge fix`, `Merge updates`, `Merge complete pre-brainstorm`) rather than parseable `Merge branch '<source>' into <target>`.
- Existing owner `I-20260404-0640-A` intentionally narrowed the ordinary receipt-gap contract to subject-matched backfills. Its residual risk explicitly said future ancestry gaps with unparseable merge subjects must fail closed and require a narrower follow-up.

## Problem Shape

- The current receipt-gap ledger can identify a concrete merge commit hash, but `governance-check` still refuses to accept the backfill unless the commit subject is parseable and matches the ledger `target_branch` / `source_branch`.
- That fail-closed behavior was correct for the previous owner boundary, but it leaves canonical `develop` red for a new real history class that now exists in dogfood truth.
- A naive “hash exists in ledger, therefore pass” relaxation would weaken auditability too much:
  - any arbitrary trailerless merge hash could be declared as covered without proving source/target semantics
  - the current guard against mismatched ledger metadata would disappear
  - future normal merge-process regressions could hide behind commit-hash-only entries

## Boundaries

- Keep this follow-on narrow:
  - do not reopen broad protected-branch merge receipt policy
  - do not weaken canonical trailer requirements for future merges
  - do not convert the ordinary receipt-gap ledger into a generic bypass ledger
  - do not mix this with runtime, auth, or preferred-auth implementation scope
- This lane only owns the new ancestry class:
  - historical ordinary protected-ancestry merges whose subject cannot be parsed into canonical source/target branch truth
  - enough canonical evidence to distinguish this class from the already-supported subject-matched receipt-gap class

## Likely Fix Directions

1. Add a stricter second backfill mode for unparseable-subject ancestry merges.
   - It must require more evidence than commit hash alone.
   - Candidate extra truth could include explicit protected batch branch, concrete owner issue, and verification artifact proving the merge family.
2. Teach `governance-check` to validate that stricter mode without pretending it recovered source/target semantics from the commit subject.
3. Keep the current subject-matched mode intact for parseable historical merges.

## 2026-04-11 Assessment

- The six failing commits form an ancestry chain under the trailer-bearing protected merge `aeca22048b2b63e2a5a3a4318e912dd0f71ee368` (`Merge branch 'test-pre-merge-20260410-preferred-auth-fix' into develop`), but the individual trailerless commits only expose parent hashes plus generic subjects.
- Existing owner docs already prove the batch and feature lane existed:
  - `docs/progress/workspace-routing-foundation/p-preferred-auth-method-account-switch-fix.md` records the feature branch and explicitly says the next merge route is `test-pre-merge-20260410-preferred-auth-fix`.
  - `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/pre-tests.md` records that same test-pre-merge batch as the integration target.
  - `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/code-reviews/20260410-preferred-auth-method-account-switch-fix-review.md` proves the bounded owner and verification artifact exist.
- Those artifacts are sufficient to justify a new explicit evidence schema, but not sufficient for the current subject-matched contract because none of them recover per-commit source/target semantics from Git history alone.

## Rejected Directions

- Reject raw hash-only backfills: they would turn the ledger into a generic ancestry exception list.
- Reject topology-only recovery: deleted refs and nested batch ancestry make parent-walk inference too unstable to be canonical truth.
- Reject implicit free-text `evidence_refs` interpretation: if the stronger contract depends on batch or owner truth, those fields must become explicit schema rather than informal reviewer convention.

## Current Leaning

- Keep this item in pre-brainstorm until the stronger contract is frozen.
- Prefer one of these two bounded shapes:
  1. a second explicit mode in `protected-branch-merge-receipt-backfills.md` with required fields for unparseable-subject ancestry gaps
  2. a separate ledger dedicated to unparseable-subject ancestry gaps so existing subject-matched semantics remain structurally isolated
- Either shape likely needs explicit fields beyond the current schema, such as:
  - protected batch branch
  - canonical protected merge commit that later absorbed the ancestry chain
  - bounded follow-on owner issue path or id
  - verification artifact that names the same batch/owner boundary

## Parser And Test Reality

- Current parser only understands one receipt-gap shape:
  - one `## Receipt Gap: <merge-hash>` block
  - required `target_branch`, `source_branch`, `canonical_merge_path`, `canonical_bypass_mode`, `follow_on_owner`, `evidence_refs`
  - semantic validation depends on either:
    - canonical trailers on the merge commit, or
    - a parseable subject `Merge branch '<source>' into <target>`
- Existing focused regression `test-governance-check-protected-branch-merge-receipt-backfills` covers:
  - no-backfill fail
  - matching parseable-subject backfill pass
  - feature-target ancestry gap pass when the subject is still parseable
  - trailer-bearing merge cannot use backfill
  - invalid develop `source_branch` rejection
- Existing tests do not cover:
  - generic-subject ancestry merges
  - malformed unparseable-subject backfill entries
  - unparseable-subject entries pointing at the wrong protected batch merge
  - free-text `evidence_refs` that mention the wrong owner/batch

## Recommended Contract Shape

- Prefer a second explicit mode in the existing ledger instead of silently overloading the current block semantics.
- Reason:
  - one file keeps all ordinary protected merge receipt-gap truth in one audit surface
  - an explicit mode field preserves current parseable-subject behavior as-is
  - the parser can reject mixed or incomplete field sets instead of guessing which semantics the author intended
- Recommended minimum fields for the new mode:
  - `validation_mode: unparseable_subject_ancestry`
  - `protected_batch_branch`: the protected batch branch that was later merged with canonical trailers
  - `absorbing_protected_merge`: the trailer-bearing protected merge commit that absorbed the ancestry chain
  - `bounded_issue`: canonical issue id or path that owned the batch
  - `verification_ref`: one canonical verification artifact that names the same batch or owner boundary
- Recommended invariants:
  - `absorbing_protected_merge` must itself be a trailer-bearing protected merge on the scanned branch
  - its `Freely-Source-Branch` must equal `protected_batch_branch`
  - the unparseable merge hash must be reachable on the first-parent ancestry segment immediately below `absorbing_protected_merge`
  - `bounded_issue` and `verification_ref` must be present; generic `evidence_refs` alone are insufficient for this mode
  - the old mode must continue to require parseable subject equality with ledger `source_branch` and `target_branch`

## Rejection Matrix To Preserve Non-Regression

- Reject an unparseable-subject entry when `validation_mode` is omitted.
- Reject an unparseable-subject entry when `absorbing_protected_merge` is missing canonical trailers.
- Reject an unparseable-subject entry when `protected_batch_branch` disagrees with the absorbing merge's `Freely-Source-Branch`.
- Reject an unparseable-subject entry when the claimed merge hash is not on the absorbed ancestry segment.
- Reject an unparseable-subject entry when it only provides the old `evidence_refs` list without explicit bounded owner and verification fields.
- Reject any attempt to use `validation_mode: unparseable_subject_ancestry` for a merge whose subject is already parseable; those must stay on the current contract.

## Risks

- If the new mode is too weak, ordinary missing-trailer merges could bypass semantic validation by claiming “unparseable subject”.
- If the new mode is too strict, every future generic-subject ancestry gap will require manual governance surgery instead of a reusable bounded contract.
- If we try to infer source/target from Git topology alone, deleted branches and nested batch ancestry may produce unstable or misleading answers.
