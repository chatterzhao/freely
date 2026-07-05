# Pre-Tests: agent-execution-safety-review-and-security-decision-support

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `issue artifacts define one reusable execution-boundary review contract across tool flags, project-local config, launch-time injection, and observed posture`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/agent-execution-safety-review-and-security-decision-support/issues/agent-execution-safety-review-and-security-decision-support.md`

### PT-2
- id: `PT-2`
- requirement: `security decision support is defined as internal AI reviewer or committee enhancement rather than user approval replacement`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/agent-execution-safety-review-and-security-decision-support/prd.md`

### PT-3
- id: `PT-3`
- requirement: `safeguard recommendation remains supported output without turning safeguard incompleteness into the default runtime blocker`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/agent-execution-safety-review-and-security-decision-support/prd.md`

### PT-4
- id: `PT-4`
- requirement: `freely doctor fails when auto-mode activation consent remains legacy or when project-level Codex approval posture drifts from Freely policy`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-doctor-execution-boundary-audit`

### PT-5
- id: `PT-5`
- requirement: `baseline observability exposes execution-boundary audit truth so operators do not rely on session memory`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-baseline-status`

### PT-6
- id: `PT-6`
- requirement: `live runtime observability exposes execution-boundary audit truth and advisory security review truth`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-live-status-security-review-surface`

### PT-7
- id: `PT-7`
- requirement: `freely security-review-brief emits machine-readable reviewer and committee guidance derived from execution-boundary truth`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-security-review-brief`

### PT-8
- id: `PT-8`
- requirement: `a reusable product skill exists for consuming the runtime brief and freezing reviewer/committee decision ladder semantics`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-agent-execution-safety-review-skill`

## Pre-merge Focused Regression / Smoke

1. acceptance target:
   - IBM artifacts are internally consistent and clearly separate capability owner from product owner
2. testing layer:
   - shell regression
3. target environment:
   - feature worktree
4. required evidence:
   - `bash docs/system/workspace/scripts/tests/test-freely-doctor-execution-boundary-audit`
   - `bash docs/system/workspace/scripts/tests/test-freely-baseline-status`
   - `bash docs/system/workspace/scripts/tests/test-freely-live-status-execution-boundary-audit`
   - `bash docs/system/workspace/scripts/tests/test-freely-security-review-brief`
   - `bash docs/system/workspace/scripts/tests/test-agent-execution-safety-review-skill`
   - `bash docs/system/workspace/scripts/tests/test-freely-init-ai-default-precedence`
   - `bash docs/system/workspace/scripts/tests/test-freely-hook-gate`
   - `bash docs/system/workspace/scripts/tests/test-freely-live-status-security-review-surface`
   - `./bin/governance-check`
5. blocker taxonomy:
   - `definition_missing`
   - `commands_only`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
6. failure handling / replay expectation:
   - repair IBM artifacts and runtime/skill truth in the feature worktree before claiming materialization complete

## Post-merge Integration Acceptance

1. acceptance target:
   - follow-on implementation can cite one stable owner for execution-boundary review and reviewer committee semantics
2. testing layer:
   - contract review against canonical `develop`
3. target environment:
   - `develop`
   - protected verification worktree
4. required evidence:
   - issue artifacts, runtime brief, and skill truth are merged and referenceable by follow-on capability work
5. blocker taxonomy:
   - `definition_missing`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
6. failure handling / replay expectation:
   - if follow-on work still needs to renegotiate capability boundary, reopen from a feature worktree and repair the owner issue artifacts

## Post-merge Application-Native Real-Environment Acceptance

1. acceptance target:
   - runtime now exposes reviewer or committee guidance without confusing it with user-step approval
2. testing layer:
   - live runtime replay against this owner
3. target environment:
   - live Freely runtime on `develop`
4. required evidence:
   - `bash docs/system/workspace/scripts/tests/test-freely-security-review-brief`
   - `bash docs/system/workspace/scripts/tests/test-agent-execution-safety-review-skill`
5. why_not_applicable:
   - this slice ships machine-readable runtime brief plus skill, but not full multi-reviewer runtime orchestration
6. replacement_evidence:
   - runtime brief and skill materially freeze reviewer or committee semantics for future orchestration

## Post-merge End-to-End Dogfood Acceptance

1. acceptance target:
   - dogfood sessions can escalate to reviewer or committee semantics without conversationally redefining the model each time
2. testing layer:
   - future dogfood replay against canonical owner
3. target environment:
   - canonical `develop` runtime
4. required evidence:
   - `bash docs/system/workspace/scripts/tests/test-freely-security-review-brief`
   - `bash docs/system/workspace/scripts/tests/test-agent-execution-safety-review-skill`
5. why_not_applicable:
   - this slice ships the first runtime helper plus skill, but not full live multi-reviewer execution
6. replacement_evidence:
   - `freely security-review-brief` and `skill:agent-execution-safety-review` provide canonical dogfood entrypoints
