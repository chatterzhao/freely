# Pre-Tests - manager-delegated-continuation-stall-recovery-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `manager delegated continuation stall recovery`
- testing layer: `focused runtime regression`
- target environment: `feature worktree`
- required evidence: targeted edge regressions plus broader manager/worker regression batch
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. Lawful active-busy wait does not recover
- setup:
  - current manager prompt already contains delegated continuation
  - latest continuity points only to active busy worker prompts
- expect:
  - `recover_stalled_manager_ai_if_needed` stays idle-safe
  - no restart / preemption side effects are emitted

2. Mixed busy and launchable continuity still recovers
- setup:
  - latest continuity contains one active-busy worker prompt and one still-launchable worker prompt
- expect:
  - manager stall recovery still triggers

3. Older continuity cannot suppress current recovery
- setup:
  - current prompt is newer than a still-busy older continuity
- expect:
  - recovery follows the current prompt, not the older continuity

4. Busy worker plus stale prompt target still recovers
- setup:
  - latest continuity mixes one active busy worker prompt with one stale / missing target
- expect:
  - busy-wait helper fails conservatively
  - manager stall recovery still triggers

5. Stale queued worker prompt relaunch
- setup:
  - launch-state still queues a worker prompt, but the target worker is no longer running
- expect:
  - prompt becomes launchable again and is relaunched

### Post-merge canonical truth acceptance

- acceptance target: `develop carries idle-safe delegated continuation recovery truth`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: verification artifact, progress closeout, and develop merge provenance
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. Keep `develop` runtime stopped until merge/writeback is finished
- expect:
  - no live dogfood restart happens from the pre-fix stalled state

2. After merge, resume a focused dogfood round
- expect:
  - `same-lane busy` no longer causes repeated `local_continuation_reentry`
  - genuinely stale queued prompts or launchable followthrough still recover

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `lawful active-busy wait on the latest relevant continuity does not trigger recovery`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-active-worker-wait-does-not-recover`

### PT-2
- id: `PT-2`
- requirement: `mixed busy and launchable continuity still triggers recovery`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-mixed-busy-and-launchable-recovers`

### PT-3
- id: `PT-3`
- requirement: `older continuity cannot suppress current delegated continuation recovery`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-older-busy-continuity-recovers`

### PT-4
- id: `PT-4`
- requirement: `busy worker plus stale prompt target still recovers conservatively`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-busy-and-stale-prompt-recovers`

### PT-5
- id: `PT-5`
- requirement: `stale queued worker prompt becomes launchable again and is relaunched`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-queued-prompt`

### PT-6
- id: `PT-6`
- requirement: `verification artifact records the broader manager and worker regression batch plus merge provenance`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/manager-delegated-continuation-stall-recovery-governance/raw-20260323-1705/code-reviews/20260328-manager-delegated-continuation-stall-recovery-verification.md`
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
