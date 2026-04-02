# Pre-Tests: agent-execution-safety-review-and-security-decision-support

## Story-Level Acceptance Items

1. `id: execution-boundary-review-contract`
- requirement: issue artifacts clearly define that tool flags, project-local config, launch-time injection, and observed posture must be comparable under one capability contract
- evidence_level: `doc-read`
- status: `pending`
- artifact_ref: `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/issues/agent-execution-safety-review-and-security-decision-support.md`

2. `id: security-decision-support-contract`
- requirement: issue artifacts clearly define reviewer/committee support as internal AI decision enhancement rather than user approval replacement
- evidence_level: `doc-read`
- status: `pending`
- artifact_ref: `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/prd.md`

3. `id: safeguard-recommendation-nonblocking`
- requirement: issue artifacts clearly state that safeguard recommendation is supported output, but safeguard incompleteness does not automatically block runtime continuation
- evidence_level: `doc-read`
- status: `pending`
- artifact_ref: `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/prd.md`

## Pre-merge Focused Regression / Smoke

1. acceptance target:
   - IBM artifacts are internally consistent and clearly separate capability owner from product owner
2. testing layer:
   - wording / structure review
3. target environment:
   - feature worktree
4. required evidence:
   - `./bin/governance-check`
5. blocker taxonomy:
   - `definition_missing`
   - `commands_only`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
6. failure handling / replay expectation:
   - repair IBM artifacts in the feature worktree before claiming materialization complete

## Post-merge Integration Acceptance

1. acceptance target:
   - later skill/runtime-helper work can cite one stable owner for execution-boundary review and reviewer committee semantics
2. testing layer:
   - contract review against canonical `develop`
3. target environment:
   - `develop`
   - protected verification worktree
4. required evidence:
   - issue artifacts are merged and referenced by follow-on capability work
5. blocker taxonomy:
   - `definition_missing`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
6. failure handling / replay expectation:
   - if follow-on work still needs to renegotiate capability boundary, reopen from a feature worktree and repair the owner issue artifacts

## Post-merge Application-Native Real-Environment Acceptance

1. acceptance target:
   - future runtime can use reviewer/committee support without confusing it with user-step approval
2. testing layer:
   - future runtime replay against this owner
3. target environment:
   - live Freely runtime on `develop`
4. required evidence:
   - follow-on implementation cites this owner
5. why_not_applicable:
   - this IBM slice only freezes capability contract; it does not yet ship live runtime behavior
6. replacement_evidence:
   - stable owner contract exists for the next implementation slice

## Post-merge End-to-End Dogfood Acceptance

1. acceptance target:
   - future dogfood sessions can escalate to reviewer/committee semantics without conversationally redefining the model each time
2. testing layer:
   - future dogfood replay against canonical owner
3. target environment:
   - canonical `develop` runtime
4. required evidence:
   - follow-on implementation points to this owner for reviewer/committee behavior
5. why_not_applicable:
   - this IBM slice does not yet ship the actual skill/runtime helper
6. replacement_evidence:
   - issue / prd / pre-tests / tasks define the contract for the next implementation slice
