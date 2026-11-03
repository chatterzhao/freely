# pre-tests：dsh-freely E2E driver

## Unit
- acceptance_target: driver 创建 worker/reviewer session、派 task、验证 commit/gate
- testing_layer: unit
- target_environment: node --test + fake ctx
- required_evidence: test log
- blocker_taxonomy: execution_pending_or_failed
1. `node --test packaging/dsh-freely/e2e/test/driver.test.mjs`

### acceptance-1：driver 角色编排
- id: DE-1
- requirement: 创建 worker/reviewer session，task 非空，result 含 sessions/commit
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/e2e/driver.js
- test_command: node --test packaging/dsh-freely/e2e/test/driver.test.mjs
- expected_output: pass
- actual_output: 1 test pass (driver.md)
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T124657Z/verification/test-evidence/driver.md

## Integration
- acceptance_target: 真实 DSH web profile 跑 E2E
- testing_layer: integration
- target_environment: dsh 0.2.1-rc.5 + freely-e2e profile
- required_evidence: result.json
- blocker_taxonomy: execution_pending_or_failed
1. `dsh plugin --profile freely-e2e add packaging/dsh-freely`
2. 跑 profile，断言 result.json committed=true。
### acceptance-2：真实 Worker commit
- id: DE-2
- requirement: Worker session 写 DONE 并 commit，result committed=true
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/e2e/driver.js
- test_command: dsh --profile freely-e2e
- expected_output: committed=true
- actual_output: committed=true, reviewerVerdict=pass, gateExitCode=0 (slice I-A)
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T124657Z/verification/test-evidence/e2e-result.json

## End-to-End
- acceptance_target: PR 是 lifecycle merge step，不是代码测试
- testing_layer: end_to_end
- target_environment: Freely PR
- required_evidence: 本 slice PR
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: E2E 代码链由 DE-1/DE-2 覆盖；PR/merge 由 pr-create/pr-merge lifecycle 验证，不在 pre-tests 里循环。
- replacement_evidence: test-evidence/e2e-result.json

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 真实 DSH 0.2.1-rc.5 freely-e2e profile 跑通：committed=true, reviewerVerdict=pass, gateExitCode=0；见 test-evidence/e2e-result.json。

## Acceptance Items
### acceptance-1
- id: DE-1
- requirement: driver 角色编排
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/e2e/driver.js
- test_command: node --test packaging/dsh-freely/e2e/test/driver.test.mjs
- expected_output: pass
- actual_output: 1 test pass (driver.md)
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T124657Z/verification/test-evidence/driver.md
### acceptance-2
- id: DE-2
- requirement: 真实 Worker commit
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: packaging/dsh-freely/e2e/driver.js
- test_command: dsh --profile freely-e2e
- expected_output: committed=true
- actual_output: committed=true, reviewerVerdict=pass, gateExitCode=0 (slice I-A)
- evidence_file: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T124657Z/verification/test-evidence/e2e-result.json
