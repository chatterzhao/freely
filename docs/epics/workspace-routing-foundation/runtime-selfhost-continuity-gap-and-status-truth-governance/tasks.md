# Tasks: runtime-selfhost-continuity-gap-and-status-truth-governance

- [x] Materialize the self-host continuity-gap candidate into a bounded owner.
- [x] Make `live-status` degrade safely when PID hint validation fails.
- [x] Remove the hard `rg` dependency from workspace-root selection.
- [x] Surface named `manager_continuity_gap_*` fields in `live-status` and a continuity-gap summary row in `fleet-status`, including structured expected/latest-generated/prompt anchors where that surface stays machine-readable.
- [x] Surface continuity-gap age and writer-state so sustained missing continuity is distinguishable from startup grace, with `fleet-status` keeping the bounded fleet-summary form.
- [x] Keep `start-lead-agent.sh` manager prompt guardrails aligned so same-lane handoff stays anchored to the active feature worktree and avoids `zsh` `status` collisions.
- [x] Add focused regressions for continuity-gap and degrade-path coverage.
- [x] Reduce self-host `live-status` scan overhead for blocked-supervision and delegated-continuation truth.
- [x] Verify that this owner stays status-only; any future prompt-required continuity auto-recovery must open a separate follow-on owner.
