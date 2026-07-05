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
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-active-worker-wait-does-not-recover`

### PT-2
- id: `PT-2`
- requirement: `mixed busy and launchable continuity still triggers recovery`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-mixed-busy-and-launchable-recovers`

### PT-3
- id: `PT-3`
- requirement: `older continuity cannot suppress current delegated continuation recovery`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-older-busy-continuity-recovers`

### PT-4
- id: `PT-4`
- requirement: `busy worker plus stale prompt target still recovers conservatively`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-busy-and-stale-prompt-recovers`

### PT-5
- id: `PT-5`
- requirement: `stale queued worker prompt becomes launchable again and is relaunched`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-queued-prompt`

### PT-6
- id: `PT-6`
- requirement: `verification artifact records the broader manager and worker regression batch plus merge provenance`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/manager-delegated-continuation-stall-recovery-governance/code-reviews/20260328-manager-delegated-continuation-stall-recovery-verification.md`
