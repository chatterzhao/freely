---
local_id: raw-20260619T045626Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T045626Z-A
platform_ids:
  github:
    issue_id: '3031'
    url: https://github.com/chatterzhao/freely/issues/3031
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T04:56:43Z'
updated_at: '2026-06-19T04:56:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

pr-merge-guarded 在 develop 上执行 `git merge --no-ff --no-commit`。当 merge 中途失败（governance gate 不通过、冲突等）时，MERGE_HEAD 残留在 .git 中。后续任何 merge 尝试都被 `fatal: You have not concluded your merge (MERGE_HEAD exists)` 阻塞，需手动 `git merge --abort` 清理。

## 实际踩坑

PR #3021 (doc-only SVG): merge 因 governance gate 失败 10+ 次，每次都留下 MERGE_HEAD，每次都需要手动 `git merge --abort; git reset --hard; git clean -fd` 才能重试。

## 行业对比

| 系统 | 并发控制 |
|------|---------|
| GitHub Merge Queue | 服务器端 FIFO + 临时 refs |
| GitLab Merge Train | 服务器端流水线 + 自动重建 |
| Mergify | 服务器端 DAG + scope 隔离 |
| Freely 当前 | **无** — 依赖 Manager 串行调用 |

## 建议修复

在 pr-merge-guarded 的 merge 段加 flock：

```bash
LOCKFILE="$(git rev-parse --git-dir)/freely-merge.lock"
exec 200>"$LOCKFILE"
flock -x -w 300 200 || fail "merge lock timeout (another merge in progress?)"
# ... existing git merge --no-ff --no-commit logic ...
flock -u 200
```

同时在 pr-merge-guarded 的 trap 中添加 `find .git -name "MERGE_*" -delete` 作为兜底清理。

## 影响范围

- `bin/pr-merge-guarded`：加 flock + MERGE_HEAD 兜底清理
