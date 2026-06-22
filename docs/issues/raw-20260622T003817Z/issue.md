---
local_id: raw-20260622T003817Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3308'
    url: https://github.com/chatterzhao/freely/issues/3308
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T00:38:34Z'
updated_at: '2026-06-22T00:38:34Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

#3291（scan_state 生命周期）只实现了 2/3，遗漏了 `task-lifecycle-scan.py` 的扫描刷新端。

**已实现（✅）：**
- wt-create 成功后 → 写入 scan_state="working"
- wt-close 成功后 → 写入 scan_state="closed"

**遗漏（❌）：**
- task-lifecycle-scan.py 扫描刷新时，没有根据已有 worktree 设置 scan_state

**后果：**
```
wt-create (00:14) → scan_state="working" ✅
scan 刷新 (00:29)  → 从头生成       → scan_state 丢失 ❌
Manager 看到 scan → scan_state="?"  → 和没修一样
```

## 修复

### task-lifecycle-scan.py

在 `build_payload` 返回 items 之后、输出 JSON 之前，遍历所有 item：

```python
# 对每个 item，根据 worktree 是否存在设置 scan_state
import subprocess

def _resolve_scan_state(item, project):
    """根据 worktree 存在 + 旧 scan state 决定新 state"""
    key = item.get("key", "")
    na = item.get("next_action", "")
    
    # 提取可能的 raw_key
    rk = _extract_raw_key(key) or _extract_raw_key(na)
    if not rk:
        return "pending"
    
    # 检查是否有工位
    wt = _find_worktree_for_raw_key(project, rk)
    if wt:
        return "working"
    
    # 检查旧 scan 中是否 closed（保留 closed 状态）
    old = _read_old_scan(project)
    if old and _was_closed(old, rk):
        # 但如果 raw issue 被 reopened → 恢复 pending
        if _raw_issue_reopened(project, rk):
            return "pending"
        return "closed"
    
    return "pending"
```

### 设计要点

| 条件 | scan_state |
|------|-----------|
| 该 raw_key 有活跃 worktree | `working` |
| 旧 scan 中是 `closed` + raw issue 已关闭 | `closed`（保留） |
| 旧 scan 中是 `closed` + raw issue 被 reopen | `pending`（重置） |
| 其他 | `pending` |

不需要跨 scan 保留 state 文件。每次扫描重新判断 worktree 存在性，这本身就是实时的真相来源。

## 涉及文件

- `task-lifecycle-scan.py` — 扫描输出前补充 scan_state

## 验证

1. wt-create 后 → 下一轮 scan 刷新 → scan_state="working"（worktree 存在）
2. wt-close 后 → 下一轮 scan 刷新 → scan_state="closed"（旧 scan closed + raw 已关闭）
3. 工位被手动删除 → 下一轮 scan 刷新 → scan_state="pending"（worktree 不存在）

🤖 Generated with [Claude Code](https://claude.com/claude-code)
