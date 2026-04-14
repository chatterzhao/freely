# Pre-Tests: freely-start-auto-recovery-rootcause-governance

## Unit

### Acceptance Items

1. **cleanup_supervisor reads shared runtime state**
   - surface_kind: `unit`
   - target_lane: `feature-local`
   - target: `cleanup_supervisor()` 函数
   - environment: `mock runtime state`
   - evidence: `test-cleanup-supervisor-reads-shared-state`
   - failure signal: `cleanup still uses stale DESIRED_RUNTIME_STATE_VALUE`
   - failure handling: `fix cleanup to read runtime_read_desired_state()`

2. **cleanup exits when replacement supervisor alive**
   - surface_kind: `unit`
   - target_lane: `feature-local`
   - target: `cleanup_supervisor()` 函数
   - environment: `mock replacement supervisor PID`
   - evidence: `test-cleanup-exits-when-replacement-alive`
   - failure signal: `cleanup still kills control-plane when replacement exists`
   - failure handling: `fix cleanup to check replacement supervisor before teardown`

3. **manager recovery uses watchdog instead of one-shot recheck**
   - surface_kind: `unit`
   - target_lane: `feature-local`
   - target: `manager recovery path after failure`
   - environment: `mock failure scenario`
   - evidence: `test-manager-recovery-launches-watchdog`
   - failure signal: `manager still uses one-shot launch_manager_control_plane_recheck()`
   - failure handling: `replace one-shot recheck with continuous watchdog`

## Integration

### Acceptance Items

1. **worker runtime falls through to cross-tool recovery**
   - surface_kind: `integration`
   - target_lane: `feature-local`
   - target: `worker runtime recovery path`
   - environment: `mock tool/slot selection`
   - evidence: `test-freely-worker-runtime-falls-through-to-cross-tool-after-failure`
   - failure signal: `worker recovery gated by failure type label`
   - failure handling: `remove failure type gating from recovery path`

2. **watchdog accepts actual slot without JSON**
   - surface_kind: `integration`
   - target_lane: `feature-local`
   - target: `watchdog slot switch validation`
   - environment: `mock empty switch JSON`
   - evidence: `test-watchdog-switch-to-codex-slot-accepts-actual-slot-without-json`
   - failure signal: `watchdog rejects slot when switch JSON empty`
   - failure handling: `fix watchdog to accept actual slot as evidence`

## End-to-End

### Acceptance Items

1. **freely start watchdog recovers when fallback tool appears late**
   - surface_kind: `end-to-end`
   - target_lane: `feature-local`
   - target: `freely start recovery chain`
   - environment: `mock bin/freely start + mock tools`
   - evidence: `test-freely-start-watchdog-recovers-when-fallback-tool-appears-late`
   - failure signal: `freely start stops recovery when first tool fails`
   - failure handling: `ensure watchdog continues recovery until tool available`

2. **freely stop prevents supervisor resurrection**
   - surface_kind: `end-to-end`
   - target_lane: `feature-local`
   - target: `freely stop cleanup contract`
   - environment: `mock bin/freely start + freely stop`
   - evidence: `test-freely-runtime-handoff-local-stop`
   - failure signal: `supervisor resurrected after freely stop`
   - failure handling: `fix cleanup to prevent resurrection race`

## Real-Environment

### Acceptance Items

1. **bad Codex account auto-switch on real start**
   - surface_kind: `real_env`
   - target_lane: `post-merge-dogfood`
   - promotion_gate: `develop_merge`
   - target: `freely start on real bad Codex account`
   - environment: `develop worktree with bad account a1016`
   - evidence: `real freely start replay + runtime-events.log + workcell-state.env`
   - task_refs: `docs/system/workspace/scripts/runtime/freely`
   - case_design:
     - manually switch Codex to `apikey-codex-a1016-1`
     - execute `./bin/freely start --project <develop-project>`
     - observe first failure with `403 Forbidden: 预扣费额度失败`
     - observe auto-switch to next available slot/tool
     - observe recovery completion without manual `freely ensure-manager`
   - failure signal: `recovery stops on first failure OR repeats same bad slot`
   - failure handling: `fix recovery handoff contract`

2. **freely stop prevents resurrection on real stop**
   - surface_kind: `real_env`
   - target_lane: `post-merge-dogfood`
   - promotion_gate: `develop_merge`
   - target: `freely stop on real runtime`
   - environment: `develop worktree after bad account recovery`
   - evidence: `real freely stop + runtime-events.log + absence of resurrected supervisor.pid`
   - task_refs: `docs/system/workspace/scripts/runtime/freely`
   - case_design:
     - after previous recovery success
     - execute `./bin/freely stop --project <develop-project>`
     - confirm supervisor.pid removed
     - confirm no new supervisor.pid appears
     - confirm no watchdog resurrection in runtime-events.log
   - failure signal: `supervisor.pid reappears after stop`
   - failure handling: `fix cleanup race condition`

### Real-Environment Status

- real_environment_status: `pending`
- real_environment_reason: `tests implemented but not yet executed on real bad account; waiting for develop merge to trigger post-merge dogfood`

## Post-Merge Acceptance

### Acceptance Items

1. **develop merge replay on bad account**
   - surface_kind: `post_merge_dogfood`
   - target_lane: `post-merge-followthrough`
   - promotion_gate: `develop_merge`
   - target: `merged implementation on develop`
   - environment: `develop canonical worktree`
   - evidence: `develop runtime-events.log showing successful recovery chain`
   - task_refs: `docs/system/workspace/scripts/runtime/freely`
   - case_design:
     - merge this fix to `develop`
     - set Codex to real bad account
     - run `./bin/freely start`
     - observe full recovery chain to available slot/tool
   - failure signal: `develop still shows recovery race or resurrection`
   - failure handling: `reopen issue for develop-level fix`

2. **develop stop prevents resurrection**
   - surface_kind: `post_merge_dogfood`
   - target_lane: `post-merge-followthrough`
   - promotion_gate: `develop_merge`
   - target: `merged stop contract on develop`
   - environment: `develop canonical worktree`
   - evidence: `develop runtime-events.log showing clean stop`
   - task_refs: `docs/system/workspace/scripts/runtime/freely`
   - case_design:
     - after previous recovery success
     - run `./bin/freely stop`
     - confirm clean stop without resurrection
   - failure signal: `develop shows resurrection after stop`
   - failure handling: `reopen issue for develop-level fix`

## Not Applicable Sections

### Not Applicable: Wording Review

- not_applicable_reason: `covered_by_more_realistic_required_surface`
- not_applicable_explanation: `This issue focuses on executable recovery chain contract; wording review would not catch the race condition that only manifests in real execution`
- replacement_evidence: `real_env tests + post_merge_dogfood tests`

## Blocker Taxonomy

- `definition_missing`: pre-tests incomplete without executable acceptance
- `commands_only`: tests only check command output, not runtime state
- `evidence_plan_missing`: missing artifact-backed pass/fail items
- `execution_pending_or_failed`: tests defined but not yet executed