# Pre-tests: manager-supervision-quiet-period-stall-signal-governance

## Acceptance Structure

### Pre-merge acceptance

- acceptance target: `manager delegated-supervision quiet-period stall signal`
- testing layer: `focused regression + integration`
- target environment: `feature worktree`
- required evidence: quiet-period regressions, delegated-continuation regressions, verification artifact
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. quiet-period lawful wait 不得直接触发 recovery。
2. 无关 active worker 或 non-busy worker 不得误 suppress recovery。
3. 更强 stall evidence 出现时 recovery 仍必须成立。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `manager delegated-supervision quiet-period does not trigger false-positive recovery`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-quiet-period-does-not-recover`

### PT-2
- id: `PT-2`
- requirement: `unrelated active workers and nonbusy workers do not mask real recovery decisions`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-unrelated-active-worker-recovers`

### PT-3
- id: `PT-3`
- requirement: `existing delegated-continuation true-positive recovery boundaries remain intact`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-busy-and-stale-prompt-recovers`
