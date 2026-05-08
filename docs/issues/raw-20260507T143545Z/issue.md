---
local_id: raw-20260507T143545Z
kind: raw
status: proposed
phase_state: proposed
platform_ids:
  github:
    issue_id: '248'
    url: https://github.com/chatterzhao/freely/issues/248
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-07T14:36:53Z'
updated_at: '2026-05-07T14:36:53Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

基于 `chat-inbox.py:_utc_timestamp()` 生成的是 `YYYYMMDDHHMMSS`（14位带秒 bare 格式），这是正确的。

但项目中存在三种 key 格式（`task-lifecycle-scan.py:1028-1030`）：

| 格式 | 示例 | 精度 | 碰撞风险 |
|------|------|------|---------|
| Old | `20260503-0915` | HHMM 无秒 | ⚠️ 有 |
| New | `20260506T1000Z` | HHMM 无秒 | ⚠️ 有 |
| Bare | `20260430222144` | HHMMSS 有秒 | ✅ 低 |

Old/New 格式**缺少秒**，同分钟内两次操作会产生重复 key。

## 修复方案

1. **统一为 `YYYYMMDDTHHMMSSZ`**（带秒），所有新创建的 raw issue 使用此格式
2. **修改全部正则** `\d{4}` → `\d{4,6}`，兼容旧 4 位格式
3. **增强 `_normalize_key_variants()`**，支持三种格式互转（含秒）
4. **Bare 格式也生成 New 格式变体**用于 cross-format 匹配

## 涉及文件及正则清单

| 文件 | 行号 | 当前 | 改为 |
|------|------|------|------|
| `task-lifecycle-scan.py` | 107 | `\d{4}Z?` | `\d{4,6}Z?` |
| `task-lifecycle-scan.py` | 198 | `\d{4}Z?` | `\d{4,6}Z?` |
| `task-lifecycle-scan.py` | 688 | `\d{4}Z?` | `\d{4,6}Z?` |
| `task-lifecycle-scan.py` | 1037 | `\d{4}$` | `\d{4,6}$` |
| `task-lifecycle-scan.py` | 1042 | `\d{4}Z$` | `\d{4,6}Z$` |
| `task-lifecycle-scan.py` | 1132 | `\d{4}Z?` | `\d{4,6}Z?` |
| `pre-push.sh` | 47-48 | `[0-9]{4}` | `[0-9]{4,6}` |
| `wt-create` | 236,240 | `[0-9]{4}` | `[0-9]{4,6}` |
| `issue-sync-batch.py` | 37 | `\d{4}` | `\d{4,6}` |

**已正确的不需改**：
- `task-lifecycle-scan.py:715,749` — 已使用 `\d{4,6}Z` ✅
- `wt-create:185` — 已使用 `[0-9]{4,6}Z` ✅
- `worktree-common.sh:54-56` — 已使用 `[0-9]{4,6}` ✅
- `chat-inbox.py:33` — 已使用 `%H%M%S` 带秒 ✅

## 兼容性

- 老格式 `20260503-0915` → 识别为 `20260503T091500Z`（后补 `00` 秒）
- 新格式 `20260506T1000Z` → 识别为 `20260506T100000Z`（后补 `00` 秒）
- 带秒格式 `20260507T143544Z` → 保持不变
