# Candidates: structured closeout gate and fresh review evidence

## Candidate

- id: `C-20260412-0225-A`
- candidate_format_version: `v2`
- title: `Structured closeout gate context and fresh review evidence governance`
- source_brainstorm: `docs/B1-docs/20260412-0225--structured-closeout-gate-and-fresh-review-evidence/brainstorms.md`
- problem: `develop` merge gate already fail-closes on missing owner-scoped staged review artifacts, but runtime/worker closeout state still stores only a weak free-text closeout command and does not carry lane/gate/evidence-policy context. This leaves cleanup replay and human operators unable to recover the full adequacy contract before the final guarded merge blocks.`
- why_now:
  - repeated gate confusion is now backed by fresh field evidence from a real `test-pre-merge-* -> develop` replay, not just theory
  - the remaining misses are not hook absence; they come from partial contract materialization across runtime state, owner `pre-tests.md`, and staged review artifacts
  - this is the smallest follow-on that can improve gate observability without relaxing any protected-branch policy
- acceptance_criteria:
  - freeze machine-readable closeout fields for target lane, promotion gate, adequacy requirement, and review-artifact policy
  - runtime delegated intake and workcell state persist those fields directly rather than only `Closeout-Gate` free-text
  - cleanup/retirement replay consumes structured closeout context without reparsing shell command strings
  - worker/gate guidance explicitly tells operators when guarded develop promote requires a fresh staged owner review artifact
  - existing `pretests-gate` / `governance-merge-gate` protections stay fail-closed with no functional rollback
- promotion_gate:
  - treat this as a follow-on to `verification-contract-and-premerge-adequacy-governance`, not a reopening of launch-time or cleanup owners
  - preserve `implementation-decision-notes-in-issue-review-artifacts-governance` as the upstream source for staged review artifact policy; do not duplicate its scope
  - show at least one real blocked develop-merge trace where lane/gate adequacy existed but fresh staged owner review evidence was still missing
- open_questions:
  - should `closeout_review_artifact_policy` remain a small enum or directly name required artifact classes
  - should closeout-only docs changes always require fresh staged review artifact, or only when the touched owner truth participates in guarded develop promote
  - should the first owner backfill compatibility shims for older `LAST_WORKER_CLOSEOUT_GATE` snapshots, or fail closed and route them to retained continuation
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The gate already works. The repeated confusion comes from not persisting the full closeout adequacy contract in one recoverable place. This should become a narrow follow-on owner instead of more prose in AGENTS or laws.`
    verdict: `ready_for_issue_materialization`
- priority: `P0`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260412-0225-A`
- recommendation: `materialized as a dedicated follow-on owner because verification-contract, review-artifact, and cleanup owners each cover only one slice of the contract and absorbing the structured closeout fields into any one of them would widen scope.`
- dependencies:
  - `verification-contract-and-premerge-adequacy-governance`
  - `implementation-decision-notes-in-issue-review-artifacts-governance`
  - `pre-tests-cleanup-and-retirement-enforcement-governance`
- landing_zones:
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/quality/pretests-retirement-gate`
  - `docs/system/workspace/scripts/quality/pretests-gate`
  - `docs/system/workspace/agents/manager-agent.md`
  - `docs/system/workspace/agents/worker-agent.md`
  - `docs/system/workspace/scripts/tests/`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/structured-closeout-gate-context-and-review-evidence-governance/issues/structured-closeout-gate-context-and-review-evidence-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action: `candidate mirror only. I-20260412-0225-A is now the canonical owner for structured closeout lane/gate/evidence policy followthrough.`
- revisit_trigger: `another guarded develop merge blocks because lane/gate adequacy exists in owner pre-tests but the develop-bound diff still lacks recoverable review-evidence context in runtime state or operator guidance.`
