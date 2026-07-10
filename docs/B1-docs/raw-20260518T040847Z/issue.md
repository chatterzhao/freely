---
local_id: raw-20260518T040847Z47Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '552'
    url: https://github.com/chatterzhao/freely/issues/552
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-18T04:09:03Z'
updated_at: '2026-06-17T00:19:17Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed---

## raw-20260518T040847Z47Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260518T040847Z47Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-05-18T04:08:47Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260518T040847Z47Z`。实现前请用 `wt-create --raw-key 20260518T040847Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P1
phase_state: absorbed
source: feedback
created_at: "2026-05-18T04:08:47Z"
title: "scan 支持 --raw-key 参数 + task-mode id 用其过滤 prompt"

## 根因

`task-mode set --task-mode id:raw-xxx` 切换任务后，manager 的 scan 仍输出全部 503 个 item，prompt 里的 task_mode 只印了一行提示"仅处理 scan-id=raw-xxx"，但下面塞了全部 item，manager 被积压项淹没，从未聚焦到指定任务。

## 设计

保持两源模型（scan + handoffs），不扩大面。`task-mode id:` 就是在已有 scan 框架内过滤：

```
task-mode set --task-mode id:raw-20260518T020345Z23Z
  │
  ▼
manager patrol → prompt_builder
  │
  ├── ① 从现有 scan JSON 搜索 raw-xxx，有则直接用
  ├── ② 没有 → task-lifecycle-scan.py --raw-key raw-xxx --json
  └── ③ prompt 只包含这一个 item
```

## 改动

### 1. `task-lifecycle-scan.py` 新增 `--raw-key` 参数

```python
parser.add_argument("--raw-key", default="", help="只扫描指定 raw key")
```

有值时 `collect_lifecycle_items` 只追踪这一个 key 的 raw→I 链。不影响现有逻辑（不传时行为不变）。

### 2. `freely` prompt 构建（14899 行附近）

`task_mode` 为 `id:*` 时：
- 提取 raw-key
- 先查现有 scan JSON 是否有此 key
- 没有则调 `task-lifecycle-scan.py --raw-key <key> --json` 现抓
- prompt 只输出这一个 item 的详情

## 涉及文件

- `docs/system/workspace/scripts/runtime/task-lifecycle-scan.py` — 加 `--raw-key` 参数 + 过滤逻辑
- `docs/system/workspace/scripts/runtime/freely` — prompt 构建段（14899 行附近）
