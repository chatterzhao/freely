# Tasks: freely-start-auto-recovery-rootcause-governance

## Feature Lane

### [x] Correct codex after-failure selector path

**Owner**: runtime
**Scope**: `docs/system/workspace/scripts/runtime/freely`  
**Description**: `codex` after-failure manager recovery must use the unified next-slot switch path instead of cached-ready probing.
**Evidence**: `tool_select_ready_slot_for_manager_auto_recovery()` now routes `after_failure` through `switch_to_next_codex_slot(... after_failure_exec_recovery_next_slot)`.
**Closeout**: `[x] after-failure selection path corrected`

### [x] Split cached-ready selection from saved-slot traversal

**Owner**: watchdog
**Scope**: `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
**Description**: Keep cache-filtered readiness for normal probing, but add a saved-slot-only selector for real after-failure traversal.
**Evidence**: `select_next_codex_slot()` stays cache-filtered and forward-only; `select_next_codex_saved_slot()` now drives after-failure switching.
**Closeout**: `[x] cached-ready and after-failure semantics separated`

### [x] Add focused regressions for saved-slot order

**Owner**: verification  
**Scope**: `docs/system/workspace/scripts/tests/*codex*`
**Description**: Lock the corrected after-failure contract with focused selector/runtime regressions.
**Evidence**: four focused regressions added or updated and passing.
**Closeout**: `[x] focused regressions cover cache skip, forward-only selection, next-slot recovery, and same-tool-before-cross-tool order`

### [x] Verify feature-local lane

**Owner**: verification  
**Scope**: `feature/freely-start-auto-recovery-rootcause-20260414`  
**Description**: Run the focused regressions in the writable feature worktree.
**Evidence**: `feature-local` runs passed for the four focused regressions plus `git diff --check`.
**Closeout**: `[x] feature-local verification passed`

### [x] Verify real runtime replay on feature lane

**Owner**: dogfood
**Scope**: `feature/freely-start-auto-recovery-rootcause-20260414`  
**Description**: Replay freely on real bad/good codex slots and confirm it can recover to a usable slot and continue doing work.
**Evidence**: ordered traversal from `worahe1000` through later saved slots plus successful `a1020-1` run creating `.freely/run/healthcheck14.txt` and `.freely/run/healthcheck15.txt`.
**Closeout**: `[x] real feature-lane replay passed and runtime was stopped after proof`

## Promotion Lane

### [x] Merge feature lane into test-pre-merge batch

**Owner**: promotion  
**Scope**: `test-pre-merge-20260414-freely-start-auto-recovery-rootcause`
**Description**: Assemble the current owner into a disposable test-pre-merge batch via `pr-merge-guarded`.
**Evidence**: guarded premerge merge commit `ca6ef7a8`.
**Closeout**: `[x] feature absorbed into current test-pre-merge batch`

### [x] Verify premerge-integration lane

**Owner**: promotion  
**Scope**: `test-pre-merge-20260414-freely-start-auto-recovery-rootcause`
**Description**: Re-run the focused regressions and governance audit on the authoritative batch.
**Evidence**: four `premerge-integration` runs passed and `./bin/governance-check` passed in the batch.
**Closeout**: `[x] premerge-integration adequacy passed`

### [ ] Promote batch to develop

**Owner**: promotion  
**Scope**: `develop`  
**Description**: Replay guarded merge from the authoritative `test-pre-merge-*` batch into canonical `develop`.
**Evidence**: pending guarded merge receipt after owner lifecycle artifacts are refreshed.
**Closeout**: `[ ] develop promote pending`

## Post-Merge Followthrough

### [ ] Run post-merge usable-slot replay on develop

**Owner**: dogfood
**Scope**: `develop`  
**Description**: Start Freely from canonical `develop` on the current usable slot and confirm it continues doing work.
**Evidence**: pending post-merge followthrough artifact.
**Closeout**: `[ ] develop followthrough pending`

### [ ] Stop runtime cleanly after followthrough

**Owner**: dogfood
**Scope**: `develop`  
**Description**: Stop the canonical runtime after followthrough and confirm it remains stopped.
**Evidence**: pending live-status / stop truth after post-merge replay.
**Closeout**: `[ ] develop stop followthrough pending`

## Retirement

### [ ] Retire test-pre-merge worktree

**Owner**: cleanup
**Scope**: `test-pre-merge-20260414-freely-start-auto-recovery-rootcause`
**Description**: Delete the disposable test-pre-merge branch/worktree once canonical develop absorbs it.
**Evidence**: pending local worktree/branch deletion.
**Closeout**: `[ ] test-pre-merge worktree pending retirement`

### [ ] Retire feature worktree

**Owner**: cleanup
**Scope**: `feature/freely-start-auto-recovery-rootcause-20260414`
**Description**: Delete the dedicated feature branch/worktree after post-merge followthrough passes.
**Evidence**: pending local worktree/branch deletion.
**Closeout**: `[ ] feature worktree pending retirement`
