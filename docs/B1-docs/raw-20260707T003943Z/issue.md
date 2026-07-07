---
local_id: raw-20260707T003943Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3788'
    url: https://github.com/chatterzhao/freely/issues/3788
    synced_at: ''
  gitee:
    issue_id: IJZ87T
    url: https://gitee.com/zhaoquan/freely/issues/IJZ87T
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-07T00:40:06Z'
updated_at: '2026-07-07T00:40:17Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

`freely wt-create` 命令执行 `raw-issue-pull` 时，Gitee 平台的 assignee 检查调用方式错误，导致整个 pull 失败。

### 根因

`platform-adapter.py` 中的 `get_assignees()` 和 `set_assignee()` 函数对 Gitee 平台使用了 REST API 风格的调用（`_gitee_api("GET", ...)` 和 `_gitee_api("PATCH", ...)`），但底层 `gitee-issue.py` 使用 CLI 子命令（`get`、`update`）。

**两个具体问题**：

1. `get_assignees()` (line 576): `_gitee_api("GET", ...)` → `gitee-issue.py` 没有 "GET" 子命令（应该是小写 "get"），且参数传递方式不兼容
2. `set_assignee()` (line 613): `_gitee_api("PATCH", ...)` → `gitee-issue.py` 没有 "PATCH" 子命令（应该用 "update" + `--assignee` 参数）

### 影响

任何 Gitee 平台上的 raw issue 无法通过 `freely wt-create` 创建工位。GitHub-only 的 issue 不受影响。

### 修复方案

1. `get_assignees` for Gitee：改用 `subprocess.run` 直接调用 `gitee-issue.py get <number>`
2. `set_assignee` for Gitee：改用 `subprocess.run` 直接调用 `gitee-issue.py update <number> --assignee <login>`
3. `pull_raw_issue`：区分 "claimed by others"（fatal）和 "claim failed"（warning），Gitee assignee 失败不阻塞 pull

### 影响文件

- `docs/system/workspace/scripts/sync/platform-adapter.py`
