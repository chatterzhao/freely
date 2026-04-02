# Pre-Tests: default-autonomy-activation-consent-and-tool-policy-governance

## Story-Level Acceptance Items

1. `id: activation-consent-contract`
- requirement: issue artifacts clearly define what activation consent must present, what it blocks on, and how accepted boundary should be recorded
- evidence_level: `doc-read`
- status: `done`
- artifact_ref: `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/issues/default-autonomy-activation-consent-and-tool-policy-governance.md`

2. `id: safeguard-guidance-nonblocking`
- requirement: issue artifacts clearly state that sandbox / VM / isolated device / restricted network are strongly recommended and supported, but not default activation blockers
- evidence_level: `doc-read`
- status: `done`
- artifact_ref: `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/prd.md`

3. `id: tool-policy-layering`
- requirement: issue artifacts clearly distinguish product-owned posture truth from the sibling owner that will materialize adapter injection and tool-local config details
- evidence_level: `doc-read`
- status: `done`
- artifact_ref: `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/prd.md`

4. `id: current-truth-split-reproduced`
- requirement: issue artifacts point to the current split between launcher/tools auto posture and project-level Codex guarded config, while assigning detailed closure to the sibling materialization owner
- evidence_level: `doc-read`
- status: `done`
- artifact_ref: `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/brainstorms/b-default-autonomy-activation-consent-and-tool-policy-governance.md`

5. `id: autonomy-escalation-contract`
- requirement: issue artifacts clearly define autonomous escalation ladder, security-focused reviewer / committee participation, and minimal risk state as the last-resort runtime path
- evidence_level: `doc-read`
- status: `done`
- artifact_ref: `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/prd.md`

6. `id: surface-contracts-explicit`
- requirement: issue artifacts clearly distinguish what `init`, `doctor`, runtime, `baseline-status`, and `live-status` each must own in the autonomy/safety contract
- evidence_level: `doc-read`
- status: `done`
- artifact_ref: `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/issues/default-autonomy-activation-consent-and-tool-policy-governance.md`

## Acceptance Items

### activation-consent-contract-frozen
- id: `activation-consent-contract-frozen`
- requirement: the owner defines a blocking activation consent contract for Freely default autonomy without ambiguity about what users must explicitly acknowledge
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/issues/default-autonomy-activation-consent-and-tool-policy-governance.md`

### safeguards-are-guidance-not-prerequisites
- id: `safeguards-are-guidance-not-prerequisites`
- requirement: the owner makes sandbox and related safety environment guidance explicit while keeping safeguard completeness non-blocking by default
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/prd.md`

### ai-first-runtime-escalation-contract
- id: `ai-first-runtime-escalation-contract`
- requirement: the owner freezes AI-first runtime escalation and minimal risk state semantics so later runtime work does not renegotiate the product posture
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/code-reviews/20260401-default-autonomy-activation-consent-verification.md`

## Pre-merge Focused Regression / Smoke

1. environment:
   - feature worktree
2. required evidence:
  - `./bin/governance-check`
  - wording readback across issue / prd / pre-tests / tasks stays consistent
3. failure signal:
   - `definition_missing`
   - `commands_only`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
4. failure handling / replay expectation:
  - fix the IBM artifacts in the feature worktree before claiming issue materialization is complete
5. current verification result:
   - `./bin/governance-check` passes in this feature worktree

## Post-merge Integration Acceptance

1. acceptance target:
   - `freely init`, `freely doctor`, runtime, and status surfaces can be reviewed against this contract without ambiguity about default autonomy posture
2. testing layer:
   - contract review against canonical `develop`
3. target environment:
   - `develop`
   - protected verification worktree
4. required evidence:
  - issue artifacts are merged
  - follow-on implementation can reference one stable owner instead of the pre-brainstorm
5. blocker taxonomy:
   - `definition_missing`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
6. failure handling / replay expectation:
   - if the contract still reads ambiguously after merge, reopen from a feature worktree and repair the owner issue artifacts rather than adding ad hoc wording elsewhere

## Post-merge Application-Native Real-Environment Acceptance

1. acceptance target:
   - later runtime implementations can present non-blocking safeguard guidance, blocking activation consent, and runtime escalation/minimal-risk behavior without conflicting product signals
2. testing layer:
   - future runtime replay against this owner
3. target environment:
   - live Freely runtime on `develop`
4. required evidence:
   - future implementation work cites this owner as the contract source
5. why_not_applicable:
   - this IBM slice only freezes contract; it does not yet change live runtime behavior
6. replacement_evidence:
  - issue / prd / pre-tests / tasks fully define the future runtime contract

## Post-merge End-to-End Dogfood Acceptance

1. acceptance target:
   - future dogfood sessions no longer need conversational renegotiation of whether Freely is autonomy-first, whether safeguards are mandatory prerequisites, or whether runtime should escalate internally before stopping
2. testing layer:
   - future dogfood replay against canonical owner
3. target environment:
   - `freely chat` against canonical `develop` runtime
4. required evidence:
   - follow-on work references this owner for posture and activation semantics
5. why_not_applicable:
   - this IBM slice does not yet modify dogfood runtime prompts or flows directly
6. replacement_evidence:
   - stable owner contract exists for the next implementation slice
