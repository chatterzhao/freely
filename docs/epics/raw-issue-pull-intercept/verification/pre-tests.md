# Pre-Tests: raw-issue-pull interception guard
- issue_id: I-20260507T143544Z-A

## Unit
- acceptance target: `raw-issue-pull 在 develop 分支拒绝执行`
- testing layer: `unit`
- target environment: `feature/raw-20260507T143544Z-intercept-guard`
- required evidence: `拒绝: 不能在受保护分支 'develop' 上执行 raw-issue-pull`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `Shell script logic. Validation is behavior-based.`
- replacement_evidence: `从 develop 执行被拦截，exit code 1`

## Unit
- acceptance target: `raw-issue-pull 在不匹配分支拒绝执行`
- testing layer: `unit`
- target environment: `feature/raw-20260507T143544Z-intercept-guard`
- required evidence: `拒绝: 当前分支 '...' 不包含 raw-key '20260507T999999Z'`
- blocker taxonomy: `execution_pending_or_failed`

## Unit
- acceptance target: `bin/freely raw-issue-pull CLI dispatch 可用`
- testing layer: `unit`
- target environment: `feature/raw-20260507T143544Z-intercept-guard`
- required evidence: `json output from platform-adapter.py pull`
- blocker taxonomy: `execution_pending_or_failed`

## Integration
- acceptance target: `governance-merge-gate passes`
- testing layer: `integration`
- target environment: `feature/raw-20260507T143544Z-intercept-guard`
- required evidence: `gate output`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `./bin/governance-merge-gate --range develop..HEAD`

## End-to-End
- acceptance target: `feature→test-pre-merge→develop merge passes`
- testing layer: `end_to_end`
- target environment: `develop-bound guarded merge chain`
- required evidence: `guarded merge receipts`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge feature into test-pre-merge via merge-guarded
2. Merge test-pre-merge into develop via merge-guarded

## Real-Environment
- real_environment_status: `pass`
- real_environment_reason: `Shell script change. Merge success is verification.`

## Acceptance Items
### AT-001 develop block
- id: `develop-block`
- requirement: `raw-issue-pull blocks on develop/main branches`
- surface_kind: `integration`
- target_lane: `premerge-integration`

### AT-002 branch mismatch
- id: `branch-mismatch`
- requirement: `raw-issue-pull blocks when branch doesn't contain raw-key`
- surface_kind: `integration`
- target_lane: `premerge-integration`

### AT-003 cli dispatch
- id: `cli-dispatch`
- requirement: `bin/freely raw-issue-pull routes correctly`
- surface_kind: `integration`
- target_lane: `premerge-integration`
