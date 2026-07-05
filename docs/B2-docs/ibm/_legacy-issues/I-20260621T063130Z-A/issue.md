---
local_id: I-20260621T063130Z-A
kind: linked
phase_state: completed
source_candidate: docs/B1-docs/raw-20260621T063130Z30Z/candidates.md#C-20260621T063130Z-A
platform_ids: {}
primary_platform: github
canonical_issue_path: docs/B1-docs/raw-20260621T063130Z30Z/candidates.md
created_at: '2026-06-21T06:31:30Z'
author: claude
channel: claude
source_raw: raw-20260621T063130Z30Z
candidate_id: C-20260621T063130Z-A
milestone_id: M-20260621T063130Z-A
---

# I-20260621T063130Z-A: raw-key-driven tooling fixes

## Map

### PRD
1. wt-close: 从 fix/raw-{key}-{slug} 分支名解析 raw-key + slug，推导 test-pre-merge 分支，存在则关闭
2. issue-sync close: platform_ids 为空时搜索 GitHub API by raw-key，都找不到则报错

### Tasks
- [x] wt-close Phase 6b: raw-key 解析 + test-pre-merge 推导清理
- [x] issue-sync cmd_close: GitHub search fallback + error on exhaustion

### Code Review
- issue_id: I-20260621T063130Z-A
- reviewer: claude
- verdict: pass
