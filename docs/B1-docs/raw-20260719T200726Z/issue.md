---
local_id: raw-20260719T200726Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '4028'
    url: https://github.com/chatterzhao/freely/issues/4028
    synced_at: ''
  gitee:
    issue_id: IK25JY
    url: https://gitee.com/zhaoquan/freely/issues/IK25JY
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-19T20:07:49Z'
updated_at: '2026-07-19T20:07:49Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因
Pre-IBM framework raw issues (source_family=chain_trace) have corrupted issue.md frontmatter:
- local_id has extra 'Z' suffix (e.g. 20260517T113021Z21Z)
- phase_state field missing or inconsistent
- These items were never created via 'freely feedback' on a platform

When 'freely wt-create --source platform' is used, the raw-issue-pull step fails because:
1. The local_id doesn't match the scan key
2. The platform pull expects a valid platform issue

## 影响
- 13 merged_develop items blocked: cannot create worktrees for issue-sync close
- 20 raw_not_started items blocked: cannot create B1 worktrees
- 1 raw_not_started wt-create attempted but rolled back

## 修复方案
Option A: Add --source chain_trace or --skip-pull to wt-create
Option B: Create a batch migration script that normalizes all old issue.md files
Option C: Update scan template to detect chain_trace and use a different workflow path

Affected items:
merged_develop: 20260517T113021Z, 20260517T113514Z, 20260517T113807Z, 20260517T114147Z, 20260517T114702Z, 20260517T115113Z, 20260517T115824Z, 20260517T120124Z, 20260517T120752Z, 20260517T121432Z, 20260527T004453Z, 20260617T035314Z, 20260714T021808Z
raw_not_started: 20260616T023944Z, 20260616T042539Z, 20260616T084121Z, 20260616T110714Z, 20260616T111514Z, 20260616T141507Z, 20260616T153638Z, 20260616T153903Z, 20260616T154953Z, 20260616T224707Z, 20260617T011030Z, 20260617T031719Z, 20260617T040640Z, 20260617T042034Z, 20260617T043953Z, 20260617T055840Z, 20260617T065642Z, 20260617T090413Z, 20260617T124129Z, 20260627T084545Z
