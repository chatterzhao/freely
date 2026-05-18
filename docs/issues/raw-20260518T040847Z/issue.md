---
kind: raw
priority: P1
phase_state: proposed
source: feedback
created_at: '2026-05-18T04:08:47Z'
title: scan 支持 --raw-key 参数 + task-mode id 用其过滤 prompt
platform_ids:
  github:
    issue_id: '552'
    url: https://github.com/chatterzhao/freely/issues/552
    synced_at: '2026-05-18T04:08:55Z'
updated_at: '2026-05-18T04:08:55Z'
primary_platform: github
platform_state: open
---

## 根因

`task-mode set --task-mode id:raw-xxx` 切换任务后，manager 的 scan 仍输出全部 503 个 item，prompt 里的 task_mode 只印了一行提示"仅处理 scan-id=raw-xxx"，但下面塞了全部 item，manager 被积压项淹没，从未聚焦到指定任务。

## 设计

保持两源模型（scan + handoffs），不扩大面。`task-mode id:` 就是在已有 scan 框架内过滤：

```
task-mode set --task-mode id:raw-20260518T020323Z
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
