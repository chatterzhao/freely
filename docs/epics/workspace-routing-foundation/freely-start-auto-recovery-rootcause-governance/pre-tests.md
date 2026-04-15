# Pre-Tests: freely-start-auto-recovery-rootcause-governance

## Feature-Local Verification

### After-failure next-slot ignores availability cache
- id: `codex-after-failure-next-slot-ignores-cache`
- requirement: `A real runtime failure must switch to the next saved codex slot before availability cache can skip it.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Keep cached-ready probing and after-failure traversal separate so same-tool recovery executes the next saved slot in order.`
- case_design: `Run the focused watchdog selector regression that proves cached-ready still filters by availability while after-failure next-slot ignores the cache and returns the next saved slot.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/freely-start-auto-recovery-rootcause-governance/code-reviews/20260414-freely-start-auto-recovery-rootcause-verification.md`

### Next-slot selection stays strictly forward
- id: `codex-next-slot-no-wrap`
- requirement: `Saved-slot traversal after failure must move strictly forward and must not wrap back to earlier failed slots.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Preserve the existing inner-loop/outer-loop contract by making same-tool codex traversal forward-only.`
- case_design: `Run the focused selector regression and confirm the final slot returns no next candidate instead of wrapping to the head of the saved-slot list.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/freely-start-auto-recovery-rootcause-governance/code-reviews/20260414-freely-start-auto-recovery-rootcause-verification.md`

### Manager after-failure path uses next-slot recovery
- id: `freely-codex-after-failure-uses-next-slot`
- requirement: `Manager auto-recovery on codex after failure must advance via the unified next-slot method instead of replaying saved-slot probe logic.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Route codex after-failure recovery through switch_to_next_codex_slot and keep the same cross-tool fallback contract.`
- case_design: `Run the focused runtime regression that stubs the codex auto-recovery path and proves the after-failure branch reaches switch_to_next_codex_slot rather than ensure_codex_slot_ready_for_manager probe logic.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/freely-start-auto-recovery-rootcause-governance/code-reviews/20260414-freely-start-auto-recovery-rootcause-verification.md`

### Same-tool codex recovery still precedes cross-tool fallback
- id: `freely-ensure-manager-codex-slot-first-then-cross-tool`
- requirement: `When codex is the active tool, recovery still exhausts the same-tool slot path before falling through the configured cross-tool order.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Keep the inner-loop contract bounded to codex slots first, then preserve the existing cross-tool order.`
- case_design: `Run the focused runtime regression that records readiness calls and confirms codex same-tool recovery is attempted before the outer cross-tool tool list is consulted.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/freely-start-auto-recovery-rootcause-governance/code-reviews/20260414-freely-start-auto-recovery-rootcause-verification.md`

### Real feature-lane replay reaches a usable slot and completes work
- id: `real-env-bad-slot-recovers-to-good-slot`
- requirement: `A real freely start replay from a bad codex slot must auto-switch to a usable slot and continue doing real work without manual ensure-manager intervention.`
- surface_kind: `real_env`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Replay freely start on real saved codex slots, then confirm a usable slot can continue the assigned task and leave run-dir evidence.`
- case_design: `Start from known bad codex slots, observe ordered same-tool traversal, switch to the currently usable slot, then verify real runtime work creates healthcheck14/15 before operator stop.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/freely-start-auto-recovery-rootcause-governance/code-reviews/20260414-freely-start-auto-recovery-rootcause-verification.md`

## Guarded Develop Promote

### Guarded develop promote proves codex recovery adequacy
- id: `develop-promote-codex-after-failure-adequacy`
- requirement: `A guarded test-pre-merge replay proves this owner carries explicit premerge-integration coverage for the corrected codex after-failure traversal contract before develop promotion.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `Replay the saved-slot-order verification batch on a disposable test-pre-merge branch created from develop and use that replay to prove guarded promotion adequacy for the corrected codex recovery contract.`
- case_design: `Merge the feature lane into a disposable test-pre-merge batch via merge-guarded, rerun the four focused regressions plus governance-check there, and use the resulting review artifact to prove the owner explicitly covers the premerge-integration:develop_merge lane/gate pair.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/freely-start-auto-recovery-rootcause-governance/code-reviews/20260414-freely-start-auto-recovery-rootcause-verification.md`

## Post-Merge Followthrough

### Develop replay on current usable slot
- id: `post-merge-usable-slot-followthrough`
- requirement: `After guarded promote, canonical develop must still run freely on the current usable slot and continue task execution.`
- surface_kind: `post_merge_dogfood`
- target_lane: `post-merge-followthrough`
- promotion_gate: `develop_merge`
- task_refs: `Re-run freely start from canonical develop using the currently usable codex slot and verify the runtime keeps doing real work.`
- case_design: `After develop absorbs this owner, run freely start in the canonical develop worktree, observe healthy runtime state on the usable slot, and stop it after task execution is confirmed.`
- evidence_level: `real_env`
- status: `pending`

### Develop stop remains stable after followthrough
- id: `post-merge-stop-followthrough`
- requirement: `After post-merge dogfood, canonical develop can be stopped cleanly without lingering runtime drift.`
- surface_kind: `post_merge_dogfood`
- target_lane: `post-merge-followthrough`
- promotion_gate: `develop_merge`
- task_refs: `Stop the canonical develop runtime after followthrough and confirm the manager/AI state returns to stopped without leaving it idle.`
- case_design: `After the develop followthrough replay, execute freely stop and confirm live-status reports stopped state with no accidental long-running token burn.`
- evidence_level: `real_env`
- status: `pending`
