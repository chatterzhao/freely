# 候选：verification-contract-and-premerge-adequacy

- id: `C-20260408-1205-A`
- candidate_format_version: `v2`
- title: Freeze verification handoff contract and premerge adequacy derivation for Freely-owned work
- source_brainstorm: `docs/B1-docs/raw-20260408-1205/brainstorms.md`
- problem: Freely already defines `pre-tests.md`, canonical test lanes, and completion-gate evidence binding, but manager/worker handoff still lacks a machine-readable verification contract and `test-pre-merge-*` still lacks a stable rule for deriving which issue-bound acceptance items must be rerun before merge. As a result, workers can execute some tests on the correct lane yet still under-test the actual acceptance contract, leaving bugs to surface only during later dogfood or real-environment followthrough.
- why_now:
  - repeated dogfood escapes indicate the remaining problem is adequacy and contract consumption, not absence of test-doc vocabulary
  - `test-pre-merge-*` has a canonical branch/lane model now, so the next gap is what counts as enough verification on that lane
  - manager/worker prompts currently carry scheduling metadata but not the actual verification obligations that should govern dispatch and completion
- acceptance_criteria:
  - define the minimum machine-readable verification metadata that manager continuity and worker prompts must carry
  - define how an issue's `pre-tests.md` maps acceptance items across `feature-local`, `premerge-integration`, and `post-merge-followthrough`
  - define the minimum premerge adequacy rule that prevents `test-pre-merge-*` from collapsing into symbolic smoke-only verification
  - define how wrapper/gate/runtime surfaces should consume the verification contract without requiring full test-orchestration automation in phase one
  - preserve the rule that dogfood and real-environment acceptance remain valid distinct surfaces for Freely-owned capabilities
- promotion_gate:
  - do not reopen `test-lane-routing-and-enforcement-governance`; treat adequacy derivation as a new owner surface beyond lane routing
  - do not reopen `pre-tests-evidence-binding-and-completion-gate-governance`; treat manager/worker handoff and premerge adequacy as earlier lifecycle enforcement
  - show that the problem is repeated under-consumption of existing verification truth, not merely one issue with weak tests
- open_questions:
  - should the first owner focus on handoff metadata only, or also ship a minimal script-side adequacy checker
  - should `Required-Acceptance-Items` reference acceptance item ids, artifact classes, or both
  - should raw-command bypass be handled in the same owner or a later wrapper-adoption follow-on
  - should this pre-brainstorm promote to one owner or split into handoff-contract and adequacy-derivation owners
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The repository already knows what pre-tests and lanes are. The missing slice is forcing manager/worker dispatch and premerge verification to consume that contract concretely enough to stop adequacy drift.`
    verdict: `ready_for_pre_brainstorm`
- priority: `P0`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260408-1205-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`
- decision_reason:
  - repeated bug escape to dogfood is better explained by weak contract consumption than by missing high-level test doctrine
  - manager/worker prompt truth currently carries launch metadata, not verification obligations
  - this gap belongs to Freely's reusable governance/runtime contract because it affects every future self-hosted or hosted issue flow
- next_action:
  - candidate mirror only. `I-20260408-1205-A` is now the canonical owner for verification contract and premerge adequacy governance
  - implementation should first freeze handoff metadata and fallback gate diagnostics before widening into broader automation
- revisit_trigger:
  - another `test-pre-merge-*` round runs the correct lane but still lacks a clear answer for why those commands were sufficient
  - another dogfood acceptance round reveals a bug that should have been covered by earlier issue-bound acceptance but was never explicitly derived into premerge verification
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
