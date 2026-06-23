---
local_id: raw-20260623T162243Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260623T162243Z-A
platform_ids:
  github:
    issue_id: '3393'
    url: https://github.com/chatterzhao/freely/issues/3393
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-23T16:23:01Z'
updated_at: '2026-06-23T16:39:11Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 背景

#3381 分析发现：`append_task_source_patrol_seed_if_needed` 构建 Manager prompt 时输出 `key`、`stage`、`ready`、`title`，但不输出 `scan_state` 和 `scan_state_worktree`。

SSE 重构（#3388）后，Manager 通过 SSE Watchdog 实时知道 Worker 状态。但当 SSE 信息不足以判断时——比如 Worker 的 SSE 流断了、scan 里看到一个 item 但不知道它有没有工位——Manager 需要 scan_state 作为补充信号。

## 当前状态

`_set_scan_states`（task-lifecycle-scan.py:627-670）已经正确设置了 `scan_state`（pending/working/closed），wt-create/wt-close 也原地更新 scan JSON。但 Manager prompt 不输出它。

另外，`scan_filter`（freely:16492-16539）会移除有活跃 Worker 的 item。但 `scan_state=working` 且无活跃 Worker 的 item（可能 Worker 死了）会通过 filter——Manager 看到它却不知道有工位。

## 要做的事

### 1. Manager prompt 输出 scan_state
`append_task_source_patrol_seed_if_needed` 中为每个 item 追加：
- `scan_state`: pending / working / closed
- `scan_state_worktree`: 工位路径

### 2. "Worker 可能已死" 提示
对 `scan_state=working` 但 A2A 查不到活跃 Worker（`working`/`submitted`/`launched`）的 item：
```
⚠️ 工位存在但 Worker 无响应：
  - raw_key: X, worktree: /path
  - 建议：查 A2A task 状态，prompt 唤醒或 wt-close
```

### 3. 补 Manager-agent.md
步骤 3 明确：scan 中 scan_state=working → 先查 A2A task 状态 → 死则 prompt → 仍无响应则 wt-close。

## 与 SSE Watchdog 的分工

| 场景 | 谁负责 |
|------|--------|
| Worker 运行中，状态正常变更 | SSE Watchdog 实时推送 |
| Worker 死了，SSE 流断开 | SSE Watchdog 检测到断连 → Manager 知道 |
| 刚重启，不确定 Worker 状态 | scan_state 告诉 Manager 有工位 → prompt 确认 |
| 工位存在但从未有过活跃 Worker | scan_state=working + 无 A2A task → "可能已死" |

## 参考
- 原始分析：https://github.com/chatterzhao/freely/issues/3381（问题 4）
- SSE 实现：https://github.com/chatterzhao/freely/pull/3389
- scan_filter：freely:16492-16539
- _set_scan_states：task-lifecycle-scan.py:627-670
