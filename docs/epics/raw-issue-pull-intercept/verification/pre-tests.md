# Pre-Tests: raw-issue-pull interception guard
- issue_id: I-20260507T143544Z-A

## Unit
- acceptance target: `raw-issue-pull 在 develop 分支拒绝执行`
- testing layer: `unit`
- target environment: `feature/raw-20260507T143544Z-intercept-guard`
- required evidence: `stderr contains "拒绝: 不能在受保护分支" and exit code 1`
- not_applicable_reason: `no_automated_test_harness_at_this_layer`
- not_applicable_explanation: `Shell script logic tested via direct execution. Verification is behavioral.`
- replacement_evidence: `Manual execution from develop returns exit 1 with expected error message`

## Unit
- acceptance target: `raw-issue-pull 在不匹配分支拒绝执行`  
- testing layer: `unit`
- target environment: `feature/raw-20260507T143544Z-intercept-guard`
- required evidence: `stderr contains "不包含 raw-key" and exit code 1`
- not_applicable_reason: `no_automated_test_harness_at_this_layer`
- not_applicable_explanation: `Shell script logic tested via direct execution.`
- replacement_evidence: `Manual execution with wrong raw-key returns exit 1`

## Unit
- acceptance target: `bin/freely raw-issue-pull CLI dispatch 可用`
- testing layer: `unit`
- target environment: `feature/raw-20260507T143544Z-intercept-guard`
- required evidence: `json output from platform-adapter.py pull`
- not_applicable_reason: `no_automated_test_harness_at_this_layer`
- not_applicable_explanation: `CLI routing tested via direct execution.`
- replacement_evidence: `Execution returns json with local_id`

## Integration
- acceptance target: `governance-merge-gate passes`
- testing layer: `integration`
- target environment: `feature/raw-20260507T143544Z-intercept-guard`
- required evidence: `gate output`
- not_applicable_reason: `no_automated_test_harness_at_this_layer`
- not_applicable_explanation: `Gate itself is the integration verification.`

## End-to-End
- acceptance target: `feature→test-pre-merge→develop merge passes`
- testing layer: `end_to_end`
- target environment: `develop-bound guarded merge chain`
- required evidence: `guarded merge receipts`

## Real-Environment
- real_environment_status: `pass`
- real_environment_reason: `Shell script change. Merge success through guarded chain is verification.`

## Acceptance Items
### AT-001 develop block
- id: `develop-block`
- requirement: `raw-issue-pull blocks on develop/main branches`  
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- evidence_level: `manual`
- status: `pass`
- artifact_ref: `bin/raw-issue-pull line 42-47`

### AT-002 branch mismatch
- id: `branch-mismatch`
- requirement: `raw-issue-pull blocks when branch does not contain raw-key`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- evidence_level: `manual`
- status: `pass`
- artifact_ref: `bin/raw-issue-pull line 49-52`

### AT-003 cli dispatch
- id: `cli-dispatch`
- requirement: `bin/freely raw-issue-pull routes to cmd_raw_issue_pull`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- evidence_level: `manual`
- status: `pass`
- artifact_ref: `freely runtime line 20844`
