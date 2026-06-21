---
local_id: raw-20260621T203349Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3291'
    url: https://github.com/chatterzhao/freely/issues/3291
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T20:34:06Z'
updated_at: '2026-06-21T21:25:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

scan 是一次性快照，生成后不再更新。Manager 每轮 patrol 看到同样的 items，即使 Worker 已在处理（wt-create 后）或已完成（wt-close 后），scan 仍显示为待处理。导致：

1. Manager 对已在处理的 item 再次 wt-create（重复工位）
2. Manager 对已完成的 item 再次委派（僵尸 Worker）
3. 无法通过 scan 区分 pending / working / closed

## 设计

### 新增字段

每个 scan item 增加：

```json
{
  "scan_state": "pending",       // pending | working | closed
  "scan_state_worktree": "",     // wt-create 写入的工位路径
  "scan_state_updated_at": ""    // ISO 时间戳
}
```

类型说明：
- `scan_state` — 不与 `phase_state`(raw issue)、`state`(A2A)、`stage`(scan) 冲突
- 旧 scan 缺少此字段 → 兼容，默认视为 `pending`

### 三个更新点

**1. scan 刷新时（task-lifecycle-scan.py）**

对已有 `scan_state` 的 item：
```
working → 检查 worktree 是否还在 → 在则保持 working，不在则重置 pending
closed → 保持 closed（除非 raw issue 重新 open → 重置 pending）
```

对新 item：
```
默认 pending
如果有已有工位（同 raw_key 的 worktree 存在）→ 直接设 working
```

**2. wt-create 成功后**

```python
# 找到对应 scan item（按 raw_key 匹配 key/next_action）
item["scan_state"] = "working"
item["scan_state_worktree"] = "<worktree_path>"
item["scan_state_updated_at"] = "<ts>"
# 原子写入: 读 → 改 → 写临时文件 → rename
```

**3. wt-close 成功后**

```python
item["scan_state"] = "closed"
item["scan_state_updated_at"] = "<ts>"
```

### 两个读取点（闸门）

**Manager prompt（委派前）：**

```
读 scan item.scan_state:
  pending → 正常委派: a2a-exit --state submitted
  working → 不 wt-create，走 session/prompt 纠偏
  closed → 跳过，不委派
```

**Runtime launch worker（兜底）：**

```
scan_state=closed → 标记 A2A task failed，"该 scan item 已关闭"
```

### 并发安全

scan JSON 读写使用原子写入：
```bash
# 读
cat .freely/run/manager-task-source-scan-latest.json

# 写（原子）
python3 -c "..." > .freely/run/scan-tmp.json
mv .freely/run/scan-tmp.json .freely/run/manager-task-source-scan-latest.json
```

不引入锁文件。读可能读到旧版本（已被其他进程覆盖），这是可接受的——最坏情况是 Manager 多等一轮 patrol。

### 涉及文件

| 文件 | 改动 |
|------|------|
| `task-lifecycle-scan.py` | 新增 scan_state 字段 + 刷新逻辑 |
| `wt-create` | 成功后更新 scan_state=working |
| `wt-close` | 成功后更新 scan_state=closed |
| `freely` (Runtime) | launch worker 前检查 scan_state |
| `manager-agent.md` | 委派前读 scan_state 分派 |

### 验证

1. wt-create 后 → scan JSON 中 item.scan_state = "working"
2. Manager 下一轮 patrol → 看到 working → 走纠偏，不 wt-create
3. wt-close 后 → scan JSON 中 item.scan_state = "closed"
4. scan 刷新时 → closed 的 item 不出现在新 scan 中，或保持 closed
5. Runtime 对 scan_state=closed 的 task → 标记 failed

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
