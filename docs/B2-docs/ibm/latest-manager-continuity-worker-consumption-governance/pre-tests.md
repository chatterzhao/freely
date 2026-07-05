# Pre-tests: latest-manager-continuity-worker-consumption-governance

## Unit
- acceptance target: `No narrower truthful unit seam is required because delegated freshness only becomes meaningful once intake history, continuity timestamps, prompt composition, and live-status surface are evaluated together.`
- testing layer: `unit`
- target environment: `feature/success-standard-governance-20260420`
- required evidence: `focused integration regressions plus owner verification artifact`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `A fake lower-level seam would miss the exact failure mode: old delegated handoffs being re-presented through both prompt composition and front-door queue rendering.`
- replacement_evidence: `The focused manager prompt, intake, and live-status regressions together are the smallest stable executable boundary for this repair.`

## Integration
- acceptance target: `delegated continuation freshness prevents stale backlog replay while preserving truthful delegated count/status surfaces`
- testing layer: `integration`
- target environment: `feature/success-standard-governance-20260420`
- required evidence: `focused regression output plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-filters-stale-delegated-continuations`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-human-chat-intake`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-continuity-resume-focus`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status`.
5. Run `git diff --check`.
6. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `guarded promote keeps the delegated freshness repair intact across feature -> test-pre-merge -> develop governance`
- testing layer: `end_to_end`
- target environment: `test-pre-merge-success-standard-governance-20260420-0215`
- required evidence: `premerge replay evidence plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge `feature/success-standard-governance-20260420` into `test-pre-merge-success-standard-governance-20260420-0215` through `freely pr-merge-guarded`.
2. Rerun the focused regression set plus `./bin/governance-check` in the pre-merge batch.
3. Use the resulting verification artifact to justify guarded promote into `develop`.

## End-to-End - 2026-04-24 Plain Worker Prompt List Parsing
- acceptance target: `guarded promote keeps current-format plain-list worker prompts launchable across feature -> test-pre-merge -> develop governance`
- testing layer: `end_to_end`
- target environment: `test-pre-merge-20260424-manager-continuity-worker-prompt-plain-list-parser`
- required evidence: `premerge replay evidence plus fresh owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge `feature/manager-continuity-worker-prompt-plain-list-parser-20260424` into `test-pre-merge-20260424-manager-continuity-worker-prompt-plain-list-parser` through `freely pr-merge-guarded`.
2. Rerun `bash docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`, `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`, and `./bin/governance-check` in the pre-merge batch.
3. Use the resulting verification artifact to justify guarded promote into `develop`.

## Real-Environment
- acceptance target: `canonical develop replay consumes the fresh success-standard governance interruption first and does not let the stale runtime-lifecycle-validation continuation hijack the manager round`
- testing layer: `real_environment`
- target environment: `develop`
- required evidence: `one-minute canonical daemon replay, live-status evidence, and prompt excerpt captured in the owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: `pass`
- real_environment_reason: `The truthful production seam was canonical develop itself, because the failure only surfaced when the manager prompt consumed a real delegated governance interruption against durable intake history.`

## Acceptance Items

### Fresh continuity suppresses stale delegated backlog replay
- id: `PT-1`
- requirement: `manager prompt filters delegated continuation backlog older than the latest manager continuity`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#2,tasks.md#5`
- case_design: `Seed stale and fresh delegated continuation items around the latest manager continuity timestamp, then verify only the fresh handoff appears in the current manager prompt while delegated items stay out of the front-door queue.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/code-reviews/20260420-latest-manager-continuity-worker-consumption-delegated-freshness-verification.md`

### Live-status keeps delegated counts without duplicating queue truth
- id: `PT-2`
- requirement: `front-door intake snapshot excludes delegated items while live-status still reports delegated counts truthfully`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#4,tasks.md#5`
- case_design: `Replay a delegated intake item through live-status and confirm the delegated count remains visible while intake_snapshot no longer duplicates the delegated item as untriaged chat.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/code-reviews/20260420-latest-manager-continuity-worker-consumption-delegated-freshness-verification.md`

### Guarded promote preserves delegated freshness adequacy
- id: `PT-3`
- requirement: `the guarded promote path and canonical develop replay consume the fresh success-standard governance interruption instead of reusing the stale runtime-lifecycle-validation continuation`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#4,tasks.md#5,tasks.md#6`
- case_design: `Merge the feature lane into the disposable test-pre-merge-success-standard-governance-20260420-0215 batch, rerun the focused regressions plus governance-check there, then replay patched daemon start and one-minute chat intake on canonical develop to confirm the new success-standard interruption becomes the consumed delegated continuation for the current manager round.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/code-reviews/20260420-latest-manager-continuity-worker-consumption-delegated-freshness-verification.md`

### Guarded promote preserves plain-list worker prompt launchability
- id: `PT-4`
- requirement: `the guarded promote path preserves launchability for plain-list entries under current-format ## Worker Prompts continuity`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#4,tasks.md#6`
- case_design: `Merge the plain-list parser feature lane into the disposable test-pre-merge-20260424-manager-continuity-worker-prompt-plain-list-parser batch, rerun the focused parser and latest continuity consumption regressions plus governance-check, then use the resulting review artifact to justify guarded promote into develop.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/code-reviews/20260424-latest-manager-continuity-worker-consumption-plain-list-prompt-parser-verification.md`
