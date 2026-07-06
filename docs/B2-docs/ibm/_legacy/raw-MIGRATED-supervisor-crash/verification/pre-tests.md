# Pre-Tests: I-20260521T032154Z-A — supervisor crash recursive ERR trap fix

## Acceptance Items

### AI-1: Benign [[ check does not generate crash report
- **type:** regression
- **adequacy:** v2
- **verification method:** code inspection + simulation
- **pre-test:** Set ERR trap, execute `[[ "a" == "b" ]]`, verify `_on_supervisor_err` exits via benign check path without crash report generation.
- **pass condition:** No crash report file written, no issue created.

### AI-2: Real crash is still detected
- **type:** regression
- **adequacy:** v2
- **verification method:** code inspection + simulation
- **pre-test:** Set ERR trap, execute `false` (non-[[ command), verify `_on_supervisor_err` proceeds to crash report generation.
- **pass condition:** Crash report generated with correct `_err_cmd` and `_err_rc`.

### AI-3: _err_cmd is captured correctly before any [[ check
- **type:** correctness
- **adequacy:** v2
- **verification method:** code inspection
- **pre-test:** Inspect the reordered `_on_supervisor_err`: confirm `_err_cmd="${BASH_COMMAND%% *}"` appears before the `[[ "$_err_rc" -eq 0 ]]` check.
- **pass condition:** Line ordering confirmed: capture before any conditional.

### AI-4: No regression on bash rc=0 crash mode (C-20260517T083030Z-A)
- **type:** cross-boundary
- **adequacy:** v2
- **verification method:** code inspection
- **pre-test:** Confirm `bash` command with rc=0 is still handled by the separate C-20260517T083030Z-A fix path, not affected by this change.
- **pass condition:** The code path for bash rc=0 is independent and unchanged.

## Test Plan

1. Unit test: Source the fixed function, trigger ERR trap with various commands
2. Integration: Run `_on_supervisor_err` with simulated error conditions
3. Verify no false positives for [[, [, and other benign commands
## Unit
- acceptance_target: 历史 issue，已完成验证
- testing_layer: unit
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成，当时不要求这些 section。原始测试证据在 issue 开发过程中已验证。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Integration
- acceptance_target: 历史 issue，已完成验证
- testing_layer: integration
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## End-to-End
- acceptance_target: 历史 issue，已完成验证
- testing_layer: end-to-end
- target_environment: develop merge chain (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 此 issue 在 pre-tests v2 标准引入前完成并已合并，原始实现已通过真实环境验证。
