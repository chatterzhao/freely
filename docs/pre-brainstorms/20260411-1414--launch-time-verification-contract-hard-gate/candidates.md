# Candidates - 20260411-1414--launch-time-verification-contract-hard-gate

## Context
- Source brainstorm: `docs/pre-brainstorms/20260411-1414--launch-time-verification-contract-hard-gate/brainstorms.md`
- Status: proposed
- Scope: freeze launch-time verification contract hard gate as phase-one owner, keep adequacy schema expansion and retirement enforcement as follow-ons

## Candidates

### C-20260411-1414-A
- candidate_format_version: `v2`
- title: Launch-time verification contract hard gate governance
- problem: Freely already has strong verification truth at doc/gate layers, but manager dispatch still launches workers when verification metadata is incomplete. Missing fields are recorded, not enforced, so contract drift is discovered late at completion/merge gates.
- why_now:
  - repeated late-gate misses indicate the urgent gap is launch-time enforcement, not additional policy wording
  - `pre-tests.md` is already the single evolving test source, so dispatch must consume it before execution
  - tightening launch-time contract is the smallest high-impact change with low regression scope
- acceptance_criteria:
  - manager dispatch refuses worker launch when required verification metadata is missing
  - rejection output is machine-readable and enumerates missing fields for fast recovery
  - runtime still persists verification metadata diagnostics for audit/continuity
  - full-metadata prompts continue to launch successfully without behavioral rollback
  - design keeps `pre-tests.md` as the single test truth and does not introduce `tests.md`
- fix_approach: enforce required verification headers at launch boundary in runtime/manager flow; convert existing metadata tests from record-only assertions to hard-gate assertions while preserving success-path tests for complete contracts
- promotion_gate:
  - prove gap location is runtime launch enforcement, not AGENTS/CONSTITUTION/LAWS wording
  - keep owner boundary tight to launch-time contract; defer adequacy schema and retirement gate to later owners
  - include no-regression verification for existing complete-metadata launch flows
- open_questions:
  - should refusal occur before intake persistence, or after intake with explicit blocked status
  - should the required field set be fixed now or configurable by intent kind in phase two
  - should branch-only or natural-language prompts receive a guided remediation template on rejection
- priority: `P0`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- source_brainstorm: `docs/pre-brainstorms/20260411-1414--launch-time-verification-contract-hard-gate/brainstorms.md`
- session_refs: []
- promoted_issue_path: `docs/epics/workspace-routing-foundation/launch-time-verification-contract-hard-gate-governance/issues/launch-time-verification-contract-hard-gate-governance.md`
- next_action: candidate mirror only. `I-20260411-1414-A` is now the canonical owner for launch-time verification contract hard gating.

### C-20260411-1414-B
- candidate_format_version: `v2`
- title: Pre-tests adequacy schema materialization governance
- problem: richer adequacy semantics were defined in governance discussions but executable gate coverage remains at a minimal field subset, allowing under-specified premerge adequacy.
- why_now: should start only after launch-time hard gate lands to avoid mixing contract enforcement and schema expansion in one owner.
- acceptance_criteria:
  - define item-level adequacy schema additions and migration strategy
  - update executable gate consumption with compatibility safeguards
  - provide explicit no-regression plan for existing owners/pre-tests documents
- priority: `P1`
- status: `queued_follow_on`
- milestone: `M-20260306-workspace-routing-foundation`
- source_brainstorm: `docs/pre-brainstorms/20260411-1414--launch-time-verification-contract-hard-gate/brainstorms.md`
- session_refs: []
- next_action: do not materialize until C-20260411-1414-A has merged and stabilized
