---
b1_id: B1-20260708T185138Z
phase_state: completed
source_raw: raw-20260708T185138Z
---
# B1: git diff relative path fix
## Problem
_sync_issues_changed_in_merge git diff -- "$issues_dir" 用绝对路径，git 需要相对路径。
## Decision
改为 git diff -- "docs/B1-docs" (repo-relative)
