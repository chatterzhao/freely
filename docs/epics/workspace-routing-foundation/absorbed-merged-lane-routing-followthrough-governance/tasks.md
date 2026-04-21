# Tasks: absorbed-merged-lane-routing-followthrough-governance

- [x] Reproduce the develop-side patrol drift where absorbed merged lanes still look like active worker execution targets.
- [x] Downgrade absorbed merged worker lanes in fleet status so they surface as cleanup followthrough instead of `role=worker`.
- [x] Route absorbed merged progress owners to cleanup in task-source-scan while keeping them visible as unfinished followthrough.
- [x] Add focused regressions and rerun nearby scan/fleet coverage.
- [ ] Replay `feature/absorbed-merged-scan-routing-fix-20260421 -> test-pre-merge-20260421-absorbed-merged-scan-routing-fix -> develop` through `./bin/merge-guarded`.
- [ ] Keep canonical develop self-host acceptance and temporary lane retirement as post-promote completion conditions owned by this issue.
