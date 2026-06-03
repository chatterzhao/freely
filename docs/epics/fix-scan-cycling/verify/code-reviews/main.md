## Implementation Decision Note

- decision: "Two-part fix: (1) issue-sync batch creates linked I-* items on platform, (2) task-lifecycle-scan.py deduplicates platform_sync_batch across scans"
- why_this: "Platform_sync_batch was cycling infinitely because linked I-* items were never created on platform (only updated/closed), and each scan generated a new unique batch key"
- alternatives_considered:
  - "Single dedup-only fix: would leave linked I-* items uncreated on platform"
  - "Single batch-only fix: would not prevent re-creation of same batch on rescan"
- boundary_non_goals:
  - "Not addressing deeper lifecycle issues in the scan pipeline"
  - "Not changing the fundamental batch architecture"
- residual_risk: "If the state file is manually deleted, a duplicate batch will be recreated"
