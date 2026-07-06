# Pre-Tests: test-lane-routing-and-enforcement-governance

## Acceptance Targets

### AT-001 lane truth and enforcement change together

- acceptance target: lane definitions, wrapper behavior, and directly coupled skills/references update in the same owner
- testing layer: governance
- target environment: issue + `AGENTS.md` + `LAWS.md` + skills + wrapper package
- required evidence: `doc and wrapper package`
- blocker taxonomy: `definition_missing`

### AT-002 lane misuse is blocked

- acceptance target: `feature-local` rejects ad hoc writable branches and protected branches while accepting dedicated `feature/*`, `feature/premerge-*`, `release/*`, and `hotfix/*`; the other two lanes enforce their protected contexts
- testing layer: focused regression
- target environment: `./bin/test-lane`
- required evidence: `lane-routing regression`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 wrapper entrypoints are directly executable

- acceptance target: `./bin/test-lane` and `./bin/test-test-lane` run directly without an extra `bash` prefix
- testing layer: focused regression
- target environment: repo wrapper entrypoints
- required evidence: `wrapper executability regression`
- blocker taxonomy: `execution_pending_or_failed`

## Pre-merge acceptance

1. `git diff --check`
   - expectation: docs and scripts remain whitespace-clean
2. `./bin/test-test-lane`
   - expectation: focused lane-routing regression passes through the real wrapper entrypoint
3. `./bin/governance-check`
   - expectation: new candidate, milestone, and owner writeback remain structurally valid

## Post-merge acceptance

1. Agents can no longer run local tests on arbitrary writable branches while claiming `feature-local`.
2. Future lane work cites this owner instead of landing more unowned `test-lane` drift.

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Lane truth, wrapper behavior, and directly coupled docs are synchronized in one owner.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/gate/test-lane-routing-and-enforcement-governance/raw-20260405-1914/issues/test-lane-routing-and-enforcement-governance.md`

### AT-002
- id: `AT-002`
- requirement: `Lane misuse is blocked by focused regression and real wrapper execution.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-test-lane`

### AT-003
- id: `AT-003`
- requirement: `Wrapper entrypoints stay directly executable.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/gate/test-lane-routing-and-enforcement-governance/raw-20260405-1914/code-reviews/20260405-test-lane-routing-and-enforcement-verification.md`
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
