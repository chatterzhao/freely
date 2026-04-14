# Tasks: freely-start-auto-recovery-rootcause-governance

## Implementation Tasks

### [x] Fix cleanup_supervisor to read shared runtime state

**Owner**: root cause fix  
**Scope**: `docs/system/workspace/scripts/runtime/freely`  
**Description**: `cleanup_supervisor()` 必先读取共享 runtime 真相（`runtime_read_desired_state()`），而不是只信当前进程内的 stale `DESIRED_RUNTIME_STATE_VALUE`  
**Evidence**: 代码改动已 staged  
**Acceptance**: `test-cleanup-supervisor-reads-shared-state`（待补）  
**Closeout**: `[x] cleanup now reads shared state first`

### [x] Fix cleanup_supervisor to exit when replacement alive

**Owner**: root cause fix  
**Scope**: `docs/system/workspace/scripts/runtime/freely`  
**Description**: 若已经有 replacement supervisor 存活，旧 supervisor cleanup 直接退出，不再覆盖共享 state，也不再去杀/重拉共享 control-plane  
**Evidence**: 代码改动已 staged  
**Acceptance**: `test-cleanup-exits-when-replacement-alive`（待补）  
**Closeout**: `[x] cleanup exits when replacement supervisor alive`

### [x] Replace one-shot recheck with continuous watchdog

**Owner**: root cause fix  
**Scope**: `docs/system/workspace/scripts/runtime/freely` + `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`  
**Description**: manager 失败后的续跑执行者，从 one-shot `launch_manager_control_plane_recheck()` 改成持续 `launch_manager_watchdog()`  
**Evidence**: 代码改动已 staged  
**Acceptance**: `test-manager-recovery-launches-watchdog`（待补）  
**Closeout**: `[x] manager recovery uses continuous watchdog`

## Test Tasks

### [x] Add regression: worker runtime falls through to cross-tool

**Owner**: regression  
**Scope**: `docs/system/workspace/scripts/tests/test-freely-worker-runtime-falls-through-to-cross-tool-after-failure`  
**Description**: 证明 worker runtime 在 same-tool slot recovery 失败后能继续进入 cross-tool fallback  
**Evidence**: test exists and passes  
**Acceptance**: `[PASS]` output  
**Closeout**: `[x] regression passes`

### [x] Add regression: watchdog accepts actual slot without JSON

**Owner**: regression  
**Scope**: `docs/system/workspace/scripts/tests/test-watchdog-switch-to-codex-slot-accepts-actual-slot-without-json`  
**Description**: 证明 watchdog 接受实际活跃 slot 作为成功证据，即使 switch JSON 为空  
**Evidence**: test exists and passes  
**Acceptance**: `[PASS]` output  
**Closeout**: `[x] regression passes`

### [x] Add regression: freely start watchdog recovers when fallback tool appears late

**Owner**: regression  
**Scope**: `docs/system/workspace/scripts/tests/test-freely-start-watchdog-recovers-when-fallback-tool-appears-late`  
**Description**: 证明 `freely start` 在当前工具先失败、fallback 工具稍后才变可用时，watchdog 会持续接力直到恢复成功  
**Evidence**: test exists and passes  
**Acceptance**: `[PASS]` output  
**Closeout**: `[x] regression passes`

### [ ] Add regression: freely stop prevents supervisor resurrection

**Owner**: regression（待补）  
**Scope**: `docs/system/workspace/scripts/tests/test-freely-runtime-handoff-local-stop`  
**Description**: 证明 `freely stop` 不会在 cleanup/recheck race 下被反向拉起  
**Evidence**: test exists  
**Acceptance**: `[PASS]` output  
**Closeout**: `[ ] regression passes`

### [ ] Add regression: cleanup reads shared state

**Owner**: regression（待补）  
**Scope**: `docs/system/workspace/scripts/tests/test-cleanup-supervisor-reads-shared-state`  
**Description**: 证明 cleanup_supervisor 先读取共享 runtime state  
**Evidence**: 待补  
**Acceptance**: `[PASS]` output  
**Closeout**: `[ ] regression passes`

### [ ] Add regression: cleanup exits when replacement alive

**Owner**: regression（待补）  
**Scope**: `docs/system/workspace/scripts/tests/test-cleanup-exits-when-replacement-alive`  
**Description**: 证明 cleanup 在 replacement supervisor 存活时直接退出  
**Evidence**: 待补  
**Acceptance**: `[PASS]` output  
**Closeout**: `[ ] regression passes`

## Verification Tasks

### [ ] Run all regressions on feature branch

**Owner**: verification  
**Scope**: `feature/freely-start-auto-recovery-rootcause-20260414`  
**Description**: 在当前 feature branch 运行所有新增回归  
**Evidence**: `./bin/governance-check` + individual test outputs  
**Acceptance**: all tests `[PASS]`  
**Closeout**: `[ ] all regressions pass on feature branch`

### [ ] Run real bad account replay on feature branch

**Owner**: verification  
**Scope**: `feature/freely-start-auto-recovery-rootcause-20260414`  
**Description**: 在当前 feature branch 执行真实坏号 replay  
**Evidence**: `runtime-events.log` + `workcell-state.env`  
**Acceptance**: recovery chain completes without race  
**Closeout**: `[ ] real bad account recovery succeeds on feature branch`

### [ ] Run freely stop verification on feature branch

**Owner**: verification  
**Scope**: `feature/freely-start-auto-recovery-rootcause-20260414`  
**Description**: 在当前 feature branch 执行 `freely stop` 验证  
**Evidence**: absence of resurrected `supervisor.pid`  
**Acceptance**: no resurrection after stop  
**Closeout**: `[ ] freely stop prevents resurrection on feature branch`

## Promotion Tasks

### [ ] Merge to test-pre-merge batch

**Owner**: promotion  
**Scope**: `test-pre-merge-freely-start-auto-recovery-rootcause-20260414`  
**Description**: 把 feature branch merge 到对应 test-pre-merge-* 批次  
**Evidence**: merge commit + receipt  
**Acceptance**: merge receipt valid  
**Closeout**: `[ ] feature merged to test-pre-merge`

### [ ] Run premerge-integration tests on batch

**Owner**: promotion  
**Scope**: `test-pre-merge-freely-start-auto-recovery-rootcause-20260414`  
**Description**: 在 test-pre-merge 批次跑 premerge-integration lane  
**Evidence**: test outputs  
**Acceptance**: all tests pass  
**Closeout**: `[ ] premerge-integration tests pass on batch`

### [ ] Merge batch to develop

**Owner**: promotion  
**Scope**: `develop`  
**Description**: 把 test-pre-merge 批次 merge 到 develop  
**Evidence**: merge commit + receipt  
**Acceptance**: merge receipt valid  
**Closeout**: `[ ] batch merged to develop`

## Post-Merge Tasks

### [ ] Run real bad account replay on develop

**Owner**: post-merge dogfood  
**Scope**: `develop`  
**Description**: 在 develop 执行真实坏号 replay  
**Evidence**: `runtime-events.log` + `workcell-state.env`  
**Acceptance**: recovery chain completes without race  
**Closeout**: `[ ] real bad account recovery succeeds on develop`

### [ ] Run freely stop verification on develop

**Owner**: post-merge dogfood  
**Scope**: `develop`  
**Description**: 在 develop 执行 `freely stop` 验证  
**Evidence**: absence of resurrected `supervisor.pid`  
**Acceptance**: no resurrection after stop  
**Closeout**: `[ ] freely stop prevents resurrection on develop`

### [ ] Update milestone status

**Owner**: governance  
**Scope**: `docs/milestones.md`  
**Description**: 把 issue 从 committed_issues 移到 completed_issues  
**Evidence**: milestone update  
**Acceptance**: milestone shows completed state  
**Closeout**: `[ ] milestone updated`

## Closeout Gate

### Completion Checkboxes

- [ ] All implementation tasks complete
- [ ] All regression tests pass on feature branch
- [ ] All real-env tests pass on feature branch
- [ ] Feature merged to test-pre-merge
- [ ] Premerge-integration tests pass on batch
- [ ] Batch merged to develop
- [ ] Post-merge dogfood tests pass on develop
- [ ] Milestone updated to completed state
- [ ] Worktree cleanup complete

### Adequacy Gate

- **Definition**: All closeout checkboxes checked
- **Evidence**: This tasks.md with all `[x]` markers
- **Guard**: `pretests-gate` will enforce tasks closeout before promote