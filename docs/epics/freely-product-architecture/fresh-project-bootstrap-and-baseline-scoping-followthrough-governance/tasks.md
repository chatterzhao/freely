# Tasks: fresh-project-bootstrap-and-baseline-scoping-followthrough-governance

1. Rewrite synced config root-bound fields to the target project instead of copying source-root absolute paths unchanged.
2. Rematerialize `.githooks` into fresh targets when the source project has them.
3. Add a focused fresh-project bootstrap regression covering `sync-tooling`, `baseline-status`, `status --view baseline`, and follow-on `init`.
4. Re-run the existing baseline/status regressions to confirm the narrower repair does not break the established status surface.
