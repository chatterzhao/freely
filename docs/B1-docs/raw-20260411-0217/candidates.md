# Candidates - 20260411-0217--protected-merge-unparseable-subject-receipt-gap

## Context

- Source brainstorm: `./brainstorms.md`
- Status: `promoted`
- Route: `bounded-governance-followthrough`

## Candidates

### C-20260411-0217-A

- candidate_format_version: `v2`
- title: `Protected-merge unparseable-subject receipt-gap followthrough`
- research_only: `false`
- implementation_ready: `true`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P1`
- promoted_issue_id: `I-20260411-0217-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/protected-merge-unparseable-subject-receipt-gap-governance/issues/protected-merge-unparseable-subject-receipt-gap-governance.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
  - `docs/system/workspace/hooks/protected-branch-merge-receipt-backfills.md`
  - `docs/system/workspace/scripts/quality/governance-check`
- problem: The ordinary protected-merge receipt-gap contract only accepts backfills when a trailerless merge still has a parseable `Merge branch '<source>' into <target>` subject. On `2026-04-11`, canonical `develop` exposed six real ancestry gaps from `test-pre-merge-20260410-preferred-auth-fix` whose subjects are generic (`Merge`, `Merge fix`, `Merge updates`, `Merge complete pre-brainstorm`). Explicit ledger entries for those hashes are still rejected because `governance-check` cannot validate them against subject-derived source/target truth.
- why_now:
  - canonical `develop` is currently red on a real protected-ancestry receipt-gap class, not just a hypothetical edge case
  - existing owner `I-20260404-0640-A` explicitly stopped at subject-matched backfills and said unparseable-subject ancestry gaps need a narrower follow-up
  - simply allowing hash-only ledger matches would weaken auditability and create a silent bypass path for future missing-trailer merges
- acceptance_criteria:
  - freeze a canonical contract for trailerless protected-ancestry merges whose subjects are not parseable into source/target branch truth
  - the contract requires stronger evidence than commit hash alone and remains distinguishable from the existing subject-matched backfill mode
  - `governance-check` still fails closed for malformed or under-evidenced ledger entries in this new class
  - canonical `develop` can pass `./bin/governance-check` for the April 10 preferred-auth batch without loosening trailer-bearing merge or ordinary subject-matched receipt-gap rules
  - focused regressions cover both the new passing case and at least one invalid/underspecified unparseable-subject backfill rejection
- promotion_gate:
  - do not weaken future canonical trailer requirements for protected merges
  - do not accept commit-hash-only ledger entries with no stronger semantic evidence
  - do not reopen broad protected-branch receipt hardening or unrelated preferred-auth implementation scope
  - keep subject-matched receipt-gap behavior intact for already-supported historical merges
- open_questions:
  - should the new contract be a second ledger mode, or a separate canonical ledger for unparseable-subject ancestry gaps
  - what is the minimum stronger evidence set: explicit batch branch, source feature branch, verification artifact, owner issue, or something else
  - can Git topology provide any stable validation signal here, or must the contract stay purely artifact-based once subject parsing fails
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author-review`
    summary: `This is a real new governance class, not a duplicate of the existing subject-matched receipt-gap owner. The new lane should stay narrow and preserve fail-closed audit semantics while defining a stronger fallback contract for unparseable merge subjects.`
    verdict: `ready_for_pre_brainstorm`
- next_action: Execute `I-20260411-0217-A` as a narrow governance followthrough: add the explicit stronger-evidence schema, extend `governance-check` without weakening the parseable-subject path, and land focused regressions for the new pass/fail matrix before touching canonical ledger entries.
- revisit_trigger: Reopen only if canonical `develop` no longer contains this ancestry class, or if a bounded design proves the current subject-matched owner can absorb it without introducing a new audit bypass path.
- decision_reason: `The current receipt-gap owner deliberately stops at parseable merge subjects. The April 10 preferred-auth batch surfaced a new history class that needs a narrower follow-on before any implementation can safely relax governance-check.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
