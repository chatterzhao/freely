# Candidates - 20260411-1417--stale-prebrainstorm-truth-reconcile

### C-20260411-1417-A: legacy issue
- candidate_format_version: `v2`
- title: Stale pre-brainstorm truth reconcile governance
- problem: Multiple active audits still consume pre-brainstorm statements that have already been superseded by owner issues, gate scripts, and regression tests, causing false negatives/false positives in governance decisions.
- why_now: Recent testing-governance reviews repeatedly hit stale statements and spent effort re-validating already-landed behavior instead of focusing on real remaining gaps.
- acceptance_criteria:
  - `A reconcile policy defines exactly when an old pre-brainstorm statement can be marked stale/superseded.`
  - `The policy also distinguishes deferred scope so deferred is never rewritten as implemented or regressed.`
  - `At least three representative stale patterns are reconciled: superseded-by-implementation, deferred-by-owner-boundary, absorbed-and-closed.`
  - `Reconcile edits are minimal and pointer-based, with no broad historical rewrite and no new capability commitments.`
  - `The policy explicitly preserves pre-tests.md as the single evolving success-standard/test-task artifact name.`
- fix_approach: Create a narrow governance owner that updates only clearly superseded pre-brainstorm claims, adds canonical pointers, and records why each reconcile action is safe.
- status: `promoted`
- promoted_issue_path: `docs/B2-docs/runtime/stale-prebrainstorm-truth-reconcile-governance/issues/stale-prebrainstorm-truth-reconcile-governance.md`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260411-1417-A`
- session_refs: []
- next_action: `Candidate mirror only. I-20260411-1417-A is authoritative and now parked at completed; use the owner package for delivered reconcile truth instead of reopening raw pre-brainstorm debate.`
- revisit_trigger: `Any new audit still reports implemented gate/hook behavior as missing because a pre-brainstorm statement remained unreconciled, and current reconcile labels cannot explain the gap.`
- source_brainstorm: `docs/B1-docs/raw-20260411-1417/brainstorms.md`
- promotion_gate:
  - `Owner scope is documentation-truth reconcile only; no runtime/gate behavior changes are mixed in.`
  - `Each reconcile patch includes explicit canonical evidence pointers.`
  - `No shared index/global catalog rewrite is included in first materialization batch.`
- open_questions:
  - `Whether reconcile receipts should be standardized per pre-brainstorm folder or tracked only in owner issue updates.`
  - `How large a reconcile batch is safe before reviewer signal quality starts to drop.`
- acceptance_reviews:
  - reviewer: `codex`
    verdict: `pass`
    rationale: `Narrow owner boundary reduces audit drift without conflating stale text cleanup with runtime hardening work.`

### C-20260411-1417-A: legacy issue
- candidate_format_version: `v2`
- title: Launch-time verification contract hard gate governance
- problem: Runtime launch can proceed with missing verification metadata, so issues surface late at merge/closeout gates.
- why_now: Audit convergence shows this is the primary remaining source of recurring late gate failures.
- acceptance_criteria:
  - `Manager-to-worker launch is blocked when required verification headers are missing.`
  - `Missing fields remain machine-readable for diagnostics and recovery.`
  - `Complete verification metadata path remains launch-compatible without regression.`
- fix_approach: Materialize launch-time hard gate as a separate owner; keep it independent from stale-text reconcile changes.
- status: `absorbed`
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs: []
- decision_reason:
  - the verification-contract / premerge-adequacy owner already materialized the canonical verification metadata contract
  - leaving this candidate as a floating follow-on would duplicate the same owner chain and reintroduce stale-truth drift
- promoted_issue_path: `docs/B2-docs/ibm/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`
- promoted_issue_id: `I-20260408-1205-A`
- promoted_issue_path_role: `absorbed-into-successor`
- next_action: `Do not reopen C-20260411-1417-B; use I-20260408-1205-A as canonical truth for the verification contract and premerge adequacy chain.`
- revisit_trigger: `Never unless the canonical verification-contract owner itself is reopened.`
- source_brainstorm: `docs/B1-docs/raw-20260411-1417/brainstorms.md`
- promotion_gate:
  - `Must be implemented in dedicated runtime owner, not bundled into reconcile-only owner.`
- open_questions:
  - `Whether block should happen at manager prompt parse, runtime intake write, or both checkpoints.`
- acceptance_reviews:
  - reviewer: `codex`
    verdict: `pass`
    rationale: `Separating execution hardening from stale-text reconcile keeps blast radius controlled.`
