---
local_id: raw-20260506T0130Z
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
kind: raw
source_family: chat_inbox
created: 2026-05-06 01:30:00+00:00
platform_ids:
  github:
    issue_id: '277'
    url: https://github.com/chatterzhao/freely/issues/277
    synced_at: '2026-05-10T09:29:31Z'
updated_at: '2026-06-17T00:21:55Z'
primary_platform: github
created_at: '2026-05-10T09:29:31Z'
platform_state: closed
---

# raw-20260506T0130Z: scan key 格式归一化——旧 HHMM ↔ 新 THHMMZ 互认

## 现象

chat_inbox 中有 3 种 key 格式共存：

| 格式 | 示例 | 数量 |
|---|---|---|
| 旧 `YYYYMMDD-HHMM` | `20260503-0915` | 7 |
| 新 `YYYYMMDDTHHMMZ` | `20260503T1035Z` | 6 |
| 裸时间戳 `YYYYMMDDHHMMSS` | `20260430222144` | 43 |

scan 的 `_find_all_branches_for_key` 和 worktree 检测用 substring 匹配，但 `20260503-0915` 不是 `20260503T0915Z` 的子串。导致 3 个已有分支的旧格式 chat 被误判为"无工位"。

## 根因

时区标准化迁移（`raw-20260503-0901`）只改了分支命名，chat_inbox 的历史条目仍是旧格式。scan 没有做格式归一化。

## 修复范围

- `_find_all_branches_for_key`：尝试旧→新格式变体匹配
- `scan_chat_inbox` worktree 检测：同上
- 不迁移 chat_inbox 数据本身（那是 `raw-20260503-0901` 的职责）

## 不修

- 裸时间戳 key 匹配 — 这些是 `freely chat --new-issue` 自动生成的 chat ID，无分支可匹配属于正常
- chat_inbox 数据迁移
