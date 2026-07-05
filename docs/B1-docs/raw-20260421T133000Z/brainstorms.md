# Brainstorm: absorbed-merged-lane-routing-followthrough

## Problem

Canonical `develop` dogfooding showed one more narrow routing seam after the merged-worker relaunch guards landed: the runtime no longer auto-recovered the old merged blocker lane, but manager patrol still consumed two advisory surfaces as if that lane were a live execution target.

1. `wt-fleet-status` preserved `LAST_ROLE_HINT=worker` for a worktree whose branch tip was already absorbed into `develop`, so the manager prompt still rendered the lane as a worker workcell.
2. `task-source-scan` treated the linked progress owner as a normal `in_verification` execution source because it only looked at progress fields, not at whether the linked branch/worktree had already been absorbed.

That combination let the manager keep routing back toward the old blocker lane even though the correct next action was cleanup/closeout followthrough or selection of another launchable task.

## Boundary

Keep this owner narrow:

1. Downgrade absorbed merged worker lanes in fleet/workcell status from `worker` to cleanup-like visibility.
2. Route progress items bound to absorbed merged lanes toward `cleanup`, while still keeping them visible to scan as unfinished followthrough.
3. Add focused regressions that prove both surfaces stop advertising absorbed merged lanes as edit-ready execution targets.
4. Preserve Freely autonomy: absorbed merged lanes remain discoverable for cleanup, but they no longer crowd out fresh launchable work.

## Non-Goals

1. Do not redesign scan architecture or live-status intent surfaces.
2. Do not introduce a durable prompt lifecycle index.
3. Do not weaken the manager's ability to self-select tasks from scan.
4. Do not reopen the broader daemon self-loop implementation owner.
