---
local_id: raw-20260618T054147Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260618T054147Z-A
platform_ids:
  github:
    issue_id: '2976'
    url: https://github.com/chatterzhao/freely/issues/2976
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T05:42:04Z'
updated_at: '2026-06-18T05:42:04Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Bug

wt-close Phase 4 删除远程分支后，本地 tracking ref (`refs/remotes/{remote}/{branch}`) 仍然存在。`git fetch` 默认不 prune，导致本地累积大量 stale refs。

本次清理发现 67 个 stale tracking refs（github 49 + origin 18），对应早已删除的远程分支。

## Fix

wt-close Phase 4 在成功删除所有远程分支后，执行 `git remote prune` 清理对应 remote 的 stale tracking refs。

```bash
# 在 Phase 4 末尾、Phase 5 之前
for remote in "${remotes[@]}"; do
  git remote prune "$remote" 2>/dev/null || true
done
```

不需要修改其他地方——prune 是幂等操作，只清理远程已不存在的 tracking refs。
