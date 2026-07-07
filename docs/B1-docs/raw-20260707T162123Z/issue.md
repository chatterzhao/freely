---
local_id: raw-20260707T162123Z
kind: raw
phase_state: absorbed
absorbed_into: 'I-20260707T162123Z-A'
platform_ids:
  github:
    issue_id: '3813'
    url: https://github.com/chatterzhao/freely/issues/3813
    synced_at: ''
  gitee:
    issue_id: IJZHOV
    url: https://gitee.com/zhaoquan/freely/issues/IJZHOV
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-07T16:21:48Z'
updated_at: '2026-07-07T16:21:48Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

1. wt-close 只调了 GitHub close，没关 Gitee
2. close_issue/add_comment 的公开 API 接受单个 platform_issue_id，传给所有平台——不同平台 ID 格式不同（GitHub 数字 vs Gitee 字母）

## 设计

### close_issue / add_comment 改为接受 platform_ids dict

```python
# 旧（有问题）
def close_issue(local_id: str, platform_issue_id: str) -> dict:
    return {h.name: h.close_issue(platform_issue_id) for h in _handlers()}

# 新（正确）
def close_issue(local_id: str, platform_ids: dict) -> dict:
    results = {}
    for h in _handlers():
        pid = platform_ids.get(h.name, {})
        issue_id = pid.get('issue_id', '') if isinstance(pid, dict) else str(pid or '')
        if not issue_id:
            results[h.name] = {'status': 'skipped', 'error': f'no issue_id for {h.name}'}
            continue
        results[h.name] = h.close_issue(issue_id)
    return results
```

### wt-close 改为双平台关闭

从 issue.md 读取 platform_ids，对每个平台分别调 close。

### 扩展性

新平台只需在 Handler 中实现 close_issue(issue_id)。platform_ids 从 issue.md 自动读取——新平台创建 issue 时自动填入。
