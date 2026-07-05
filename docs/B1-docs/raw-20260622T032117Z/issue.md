---
local_id: raw-20260622T032117Z17Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3333'
    url: https://github.com/chatterzhao/freely/issues/3333
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T03:21:35Z'
updated_at: '2026-06-22T03:21:35Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

`task-lifecycle-scan.py` 中 `platform_ids` 存在两种格式：

- **扁平格式**（`_extract_platform_ids` 返回）：`{"github": "97", "gitee": "..."}` — 值是 string
- **嵌套格式**（`collect_lifecycle_items` 构建）：`{"github": {"issue_id": "97", "url": "..."}}` — 值是 dict

4 处代码拿到嵌套格式但当扁平格式用，导致 `str(dict)` 变成 `"{'issue_id': '97'}"`，在 `platform_all` 中永远匹配不到。

## 受影响位置

| 行号 | 代码 | 影响 |
|------|------|------|
| L367 | `raw_pids["github"]` | `check_completion`: raw 的 github 关闭状态永远检测不到 |
| L392 | `pids["github"]` | `check_completion`: child 的 github 关闭状态永远检测不到 |
| L397 | `pids.get("gitee")` | `check_completion`: gitee 关闭状态永远检测不到 |
| L1278 | `pids.get("github", "")` | `chain_trace`: platform_close 永远 unreached |

**后果**：所有已关闭的 issue 被误报为 `platform_close_missing`，daemon 反复创建 sync batch 浪费资源。

## 修复

添加 `_platform_issue_id(pids, platform)` 统一提取函数：

```python
def _platform_issue_id(pids: dict, platform: str) -> str:
    val = pids.get(platform, "")
    if isinstance(val, dict):
        return val.get("issue_id", "")
    return val
```

4 处调用点全部改用此函数。

## 验证

1. `platform_all` 中有 #97 (CLOSED)，scan 中 20260404-0119 的 `platform_close` 应为 reached
2. daemon 不再对已关闭 issue 重复创建 platform sync batch

🤖 Generated with [Claude Code](https://claude.com/claude-code)
