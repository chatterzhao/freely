---
local_id: raw-20260508T133423Z
kind: raw
status: proposed
phase_state: proposed
platform_ids:
  github:
    issue_id: '259'
    url: https://github.com/chatterzhao/freely/issues/259
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-08T13:34:32Z'
updated_at: '2026-05-08T13:34:32Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
---

## Bug 1

`raw-issue-pull` 第 41 行：`git -C "$ROOT_DIR" rev-parse --abbrev-ref HEAD` 永远返回 `develop`，导致第 43-48 行分支检查在所有工位内都被拦截。

```bash
current_branch="$(git -C "$ROOT_DIR" rev-parse --abbrev-ref HEAD)"  # ← 永远是 develop
case "$current_branch" in
  develop|main)  # ← 永远命中，永远拦截
    exit 1
```

## Bug 2 (#257)

`platform-adapter.py` `pull_raw_issue` 第 326 行：标题已有 `raw-{key}` 时仍用 `created_at` 覆盖 key，导致 key 不一致。

## 修复

1. `raw-issue-pull` 第 41 行：`-C "$ROOT_DIR"` 删掉，用当前目录
2. `platform-adapter.py` 第 326 行：标题已有 `raw-{raw_key}` 时跳过标准化

- pre_tests_path: docs/epics/raw-issue-pull-git-cwd/verification/pre-tests.md
- verification_artifact_dir: docs/epics/raw-issue-pull-git-cwd/code-reviews
