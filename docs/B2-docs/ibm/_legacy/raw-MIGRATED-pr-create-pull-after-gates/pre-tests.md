# Pre-tests: I-20260625T050000Z-A

## Unit

- acceptance target: bash -n syntax verification of pr-create-guarded script
- testing layer: local workstation
- target environment: bash 3.2+ on macOS/Linux
- required evidence: bash -n docs/system/workspace/scripts/worktree/pr-create-guarded exit code 0
- blocker taxonomy: low-risk configuration change

1. Run bash -n on the modified pr-create-guarded and verify exit code 0
2. Inspect the script to confirm pull is at Step 3 (not Step 1)
3. Verify that all gate exits still occur before the pull

## Integration

- acceptance target: gate sequencing in pr-create-guarded
- testing layer: integration
- target environment: fix worktree
- required evidence: script flow inspection
- blocker taxonomy: medium-risk reordering
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: This change only reorders existing logic within the same script; no new gate or external dependency is introduced.
- replacement_evidence: docs/B2-docs/pr-create-pull-after-gates/code-reviews/flow-verification.txt

## End-to-End

- acceptance target: full pr-create-guarded pipeline smoke test
- testing layer: e2e
- target environment: local git worktree with git remotes
- required evidence: E2E test log
- blocker taxonomy: low-risk (reorder-only change)
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: The pr-create-guarded script requires git remotes and platform credentials for full E2E, which are not available in the isolated test worktree.
- replacement_evidence: docs/B2-docs/pr-create-pull-after-gates/code-reviews/design-review-notes.txt

## Real-Environment

- real_environment_status: pass
- real_environment_reason: This is a script change that only reorders an internal step within pr-create-guarded. No real-environment infrastructure, authentication, or networking is involved.

## Acceptance Items

### AI-001: Syntax check passes

- id: AI-001
- requirement: bash -n must pass on the modified pr-create-guarded script
- evidence_level: mock
^- status: passed
- artifact_ref: docs/B2-docs/pr-create-pull-after-gates/code-reviews/syntax-check.txt

### AI-002: Pull is at Step 3, gates all precede it

- id: AI-002
- requirement: git pull origin develop must appear after gate-passed marker and before push, never at Step 1
- evidence_level: mock
^- status: passed
- artifact_ref: docs/B2-docs/pr-create-pull-after-gates/code-reviews/flow-verification.txt

### AI-003: All gate checks still exit early before pull

- id: AI-003
- requirement: Every gate failure path must exit 1 before reaching the pull command
- evidence_level: mock
^- status: passed
- artifact_ref: docs/B2-docs/pr-create-pull-after-gates/code-reviews/flow-verification.txt
