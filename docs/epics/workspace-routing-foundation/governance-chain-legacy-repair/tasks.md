# Tasks: governance-chain-legacy-repair

## Slice 1: Materialize the umbrella owner

- [x] Add the canonical issue for `I-20260403-1100-A`.
- [x] Add the matching progress artifact.
- [x] Add the milestone committed issue entry.
- [x] Add an issue-bound decision note in the verification artifact dir.

## Slice 2: Normalize active child repair slices

- [x] Reclassify `1200` so it no longer points at a nonexistent issue.
- [x] Reclassify `1201` so it no longer points at a nonexistent issue.
- [x] Reclassify `1202` so it no longer points at a nonexistent issue.
- [x] Reclassify `1203` so it no longer points at a nonexistent issue.
- [x] Make the parent/child relationship explicit in the child pre-brainstorm docs.

## Slice 3: Repair legacy governance chain truth

- [ ] Backfill missing `verification_artifact_dir` fields where required.
- [ ] Backfill missing implementation decision note fields where required.
- [ ] Normalize legacy review / issue key mismatches.
- [ ] Backfill missing candidate continuity fields where required.

## Slice 4: Validate and close the batch

- [x] Run `git diff --check`.
- [x] Run `./bin/governance-check`.
- [x] Review `./bin/wt-status-all` before any promotion or cleanup decision.
- [x] Record which completed or stale worktrees are safe to retire.
