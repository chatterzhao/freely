# Pre-tests: I-20260624T152500Z-A

## Unit

- acceptance target: bash -n syntax verification of pr-create-guarded script
- testing layer: local workstation
- target environment: bash 3.2+ on macOS/Linux
- required evidence: bash -n docs/system/workspace/scripts/worktree/pr-create-guarded exit code 0
- blocker taxonomy: low-risk configuration change

1. Run bash -n on the modified pr-create-guarded and verify exit code 0
2. Run bash -n on wt-close to verify no regression in similar scripts
3. Inspect the added Step 2c section to confirm it appears after Step 2b and before gate-passed marker

## Integration

- acceptance target: pretests-retirement-gate integration with pr-create-guarded
- testing layer: integration
- target environment: fix worktree
- required evidence: pretests-retirement-gate script resolution and error output
- blocker taxonomy: medium-risk integration point
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: This change only adds a gate call; the actual gate logic (pretests-retirement-gate + pretests-gate) is unchanged and already tested by its own unit tests.
- replacement_evidence: docs/B2-docs/pr-create-pretests-check/code-reviews/pretests-gate-call-trace.txt

## End-to-End

- acceptance target: full pr-create-guarded pipeline smoke test
- testing layer: e2e
- target environment: local git worktree with git remotes
- required evidence: E2E test log
- blocker taxonomy: low-risk (additive-only change)
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: The pr-create-guarded script requires git remotes and platform credentials for full E2E, which are not available in the isolated test worktree.
- replacement_evidence: docs/B2-docs/pr-create-pretests-check/code-reviews/design-review-notes.txt

## Real-Environment

- real_environment_status: pass
- real_environment_reason: This is a script change that only affects the pre-PR gate. No real-environment infrastructure, authentication, or networking is involved. The change is purely additive (new gate call) and does not alter any runtime behavior.

## Acceptance Items

### AI-001: Syntax check passes

- id: AI-001
- requirement: bash -n must pass on the modified pr-create-guarded script
- evidence_level: mock
^- status: passed
- artifact_ref: docs/B2-docs/pr-create-pretests-check/code-reviews/syntax-check.txt

### AI-002: Gate structure is correct

- id: AI-002
- requirement: Step 2c must appear after Step 2b and before gate-passed marker in the script flow
- evidence_level: mock
^- status: passed
- artifact_ref: docs/B2-docs/pr-create-pretests-check/code-reviews/design-review-notes.txt

### AI-003: Error message provides clear instructions

- id: AI-003
- requirement: When gate fails, the error message must reference freely-test-execution skill and pr-create-guarded
- evidence_level: mock
^- status: passed
- artifact_ref: docs/B2-docs/pr-create-pretests-check/code-reviews/design-review-notes.txt
