# Tasks: worktree-exclusive-ownership-and-promotion-lease-governance

## Slice 1: IBM contract freeze

- [x] Freeze phase-1 `occupancy record` fields.
- [x] Freeze phase-1 `intent lease record` fields.
- [x] Freeze canonical enums for `lease_kind`, `lease_status`, and `takeover_policy`.
- [x] Freeze `promotion lease` identity as `issue_id + integration_target`.
- [x] Freeze `soft-stale / hard-stale / blocked-but-owned / explicit-handoff` semantics.
- [x] Freeze `manager-only arbitration` and `worker locality default-deny`.

## Slice 2: Runtime hook-point mapping

- [x] Map worker launch path to future intent gate consumption.
- [x] Map cleanup followthrough retain/delete path to ownership-aware retain/reclaim decisions.
- [x] Map promotion / merge-prep path to ownership-aware routing after global cleanliness inspection.

## Slice 3: Status and continuity surfaces

- [x] Decide whether phase-1 lease truth is project-level, worktree-level, or dual-surfaced.
- [x] Define `live-status` and `fleet-status` output additions.
- [x] Define manager continuity / worker prompt additions: `intent_kind`, `intent_target`, lease disposition.
- [x] Define fallback normalization for missing/unknown prompt intent metadata.

## Slice 4: Test plan

- [x] Define same-worktree double-write conflict scenario.
- [x] Define dirty cleanup contention scenario.
- [x] Define duplicate promotion scenario.
- [x] Define sibling-dirty overreach scenario.
- [x] Tie stale/takeover behavior to explicit acceptance evidence.

## Exit

- [x] IBM artifacts are sufficient to move this owner from `in_ibm` to `done_ibm`.
- [x] The first dev-loop slice is obvious enough to execute without reopening pre-brainstorm.
