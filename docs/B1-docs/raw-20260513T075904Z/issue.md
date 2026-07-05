---
local_id: raw-20260513T075904Z04Z
kind: raw
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
priority: P1
source: chat-inbox
created_at: '2026-05-13T07:59:04Z'
title: 'pr-merge-guarded: _sync_issues_changed_in_merge reads fm.get(''status'') but
  I-* issues use phase_state'
updated_at: '2026-06-17T00:25:55Z'
platform_ids:
  github:
    issue_id: '329'
    url: https://github.com/chatterzhao/freely/issues/329
    synced_at: '2026-05-13T07:59:10Z'
primary_platform: github
platform_state: closed
---

## Bug

`docs/system/workspace/scripts/worktree/pr-merge-guarded:235` 在 post-merge sync 中读的是 `fm.get('status')`，但 I-* linked issue 的 frontmatter 字段是 `phase_state`，不是 `status`。

## Impact

`linked/completed` case branch 永远匹配不到（因为 `status` 永远是空串），永远只走 `linked/*` 分支（只 `issue-sync update`，不 `issue-sync close`）。

结果：merge 到 develop 后 GitHub issue 从不自动关闭。

## Location

`docs/system/workspace/scripts/worktree/pr-merge-guarded` lines 233-254:

```bash
status=$(python3 -c "... fm.get('status','')")  # ← BUG: should also check phase_state
case "$kind/$status" in
  linked/completed)
    issue-sync close  # ← NEVER REACHED
    ;;
  linked/*)
    issue-sync update  # ← ALWAYS runs, never closes
    ;;
esac
```

## Fix

读 `fm.get('phase_state')` 作为 fallback：

```bash
phase=$(python3 -c "... fm.get('phase_state', fm.get('status',''))")
case "$kind/$phase" in
```
