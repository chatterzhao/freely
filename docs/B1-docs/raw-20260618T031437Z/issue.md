---
local_id: raw-20260618T031437Z37Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260618T031437Z-A
platform_ids:
  github:
    issue_id: '2961'
    url: https://github.com/chatterzhao/freely/issues/2961
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T03:14:54Z'
updated_at: '2026-06-18T03:14:54Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Bug

wt-close Phase 4 (Remote branch delete) 有两处 bug 导致远程分支删除失败：

### Bug 1: $SELF_ROOT 未定义 (line 368)

```bash
_gitee_branch_delete() {
  local gitee_py="$SELF_ROOT/docs/system/workspace/scripts/runtime/gitee-issue.py"
```

`$SELF_ROOT` 只在 `freely` runtime 脚本中定义，wt-close 是独立脚本，没有这个变量。导致 gitee API 删除永远失败。

修复：改为 `$PROJECT_ROOT`（wt-close 已有）。

### Bug 2: 静默失败 (Phase 4 多处)

```bash
if git fetch "$remote" "$branch" 2>/dev/null; then   # fetch 失败 → 跳过删除
  ...
  git push "$remote" --delete "$branch" 2>/dev/null || true  # push 失败 → 被吞
fi
```

fetch 失败不应该跳过删除——远程分支可能 fetch 不到但仍存在。push --delete 失败应该至少打印 warning。

### 影响

GitHub 上 9 个远程分支残留：本地已 wt-close，远程未删除。
