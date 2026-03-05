---
name: config-backup-guard
description: Enforce mandatory configuration backup before modifications. Use whenever AI changes any configuration file to create traceable backup and recovery path before editing.
---

# skill:config-backup-guard

## Workflow
1. Detect target config files before edit.
2. Create backup using required naming convention.
3. Apply changes only after backup success.
4. Record backup path and timestamp in execution notes.

## Done
- Every config change has a recoverable backup artifact.
