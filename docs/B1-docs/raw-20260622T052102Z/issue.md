---
local_id: raw-20260622T052102Z02Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3338'
    url: https://github.com/chatterzhao/freely/issues/3338
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T05:21:19Z'
updated_at: '2026-06-22T05:21:19Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

`fetch_open_platform_issues` 在 `task-lifecycle-scan.py` 中硬编码了 `gh issue list`，只查 GitHub。应改为读 `FREELY_REPO_PLATFORMS` 配置，对所有配置的平台取 open issues 的 union。

## 设计

在 `platform-adapter.py` 新增 `list_open_issues()` 函数：

```python
def list_open_issues(platforms: list[str]) -> dict[str, str]:
    """列出所有平台 OPEN issues，返回 union {number: state}"""
    result = {}
    for p in platforms:
        if p == "github":
            proc = subprocess.run(
                ["gh", "issue", "list", "--state", "open", "--limit", "200",
                 "--json", "number,state"],
                capture_output=True, text=True, timeout=30)
            if proc.returncode == 0:
                for issue in json.loads(proc.stdout):
                    result[str(issue["number"])] = issue["state"]
        elif p == "gitee":
            proc = subprocess.run(
                [sys.executable, str(RUNTIME_DIR / "gitee-issue.py"),
                 "list", "--state", "open", "--per-page", "50"],
                capture_output=True, text=True, timeout=30)
            if proc.returncode == 0:
                for issue in json.loads(proc.stdout):
                    num = str(issue.get("number", issue.get("id", "")))
                    if num:
                        result[num] = issue.get("state", "OPEN")
    return result
```

`fetch_open_platform_issues` 改为：

```python
platforms = os.environ.get("FREELY_REPO_PLATFORMS", "").split(",")
platforms = [p.strip() for p in platforms if p.strip()]
open_issues = list_open_issues(platforms)
```

不需要新 CLI 命令。`issue-sync` 的 create/close/comment 已经是这个模式（一个命令对所有平台执行）。只是 scan 的 list 漏了。

## 涉及文件

| 文件 | 改动 |
|------|------|
| `platform-adapter.py` | 新增 `list_open_issues()` |
| `task-lifecycle-scan.py` | `fetch_open_platform_issues` 改为调用 adapter |

## 验证

- `FREELY_REPO_PLATFORMS = "github"` → 只查 GitHub
- `FREELY_REPO_PLATFORMS = "github,gitee"` → 两平台 union
- `FREELY_REPO_PLATFORMS = ""` → 空，scan 无平台数据

🤖 Generated with [Claude Code](https://claude.com/claude-code)
