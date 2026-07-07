---
local_id: raw-20260707T141251Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260707T141251Z-A
platform_ids:
  github:
    issue_id: '3807'
    url: https://github.com/chatterzhao/freely/issues/3807
    synced_at: ''
  gitee:
    issue_id: IJZHGI
    url: https://gitee.com/zhaoquan/freely/issues/IJZHGI
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-07T14:13:23Z'
updated_at: '2026-07-07T14:41:29Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题

platform-adapter.py 每个函数都是 if/elif 硬编码平台分支。加第三个平台需要改所有函数。

## 目标

改为 Handler 注册表模式——新平台只需写一个 Handler 类 + 注册一行，不改现有代码。

## 当前状态

870 行文件中，每个公开函数都含:
```python
if platform == "github": ...
elif platform == "gitee": ...
```

## 目标架构

```python
class PlatformHandler(ABC):
    detect() -> bool
    create_issue(title, body) -> dict
    close_issue(issue_id) -> dict
    add_comment(issue_id, body) -> dict
    create_pr(branch, base, title, body) -> dict
    search_raw_issue(raw_key) -> dict
    fetch_issue(issue_id) -> dict
    get_assignees(issue_id) -> list
    set_assignee(issue_id, login) -> tuple

_REGISTRY = []
register(GitHubHandler())
register(GiteeHandler())
# register(GitLabHandler())  ← 新平台只加这一行
```

## 约束

- 所有现有调用方不感知变化（公开 API 签名不变）
- CLI 入口保持不变
- GitHub/Gitee handler 实现从现有代码提取
