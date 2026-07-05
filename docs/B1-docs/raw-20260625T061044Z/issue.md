---
local_id: raw-20260625T061044Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3484'
    url: https://github.com/chatterzhao/freely/issues/3484
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T06:11:03Z'
updated_at: '2026-06-25T06:11:03Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T061044Z-A
source_candidate: docs/B1-docs/20260625T061044Z--issue-sync-batch/candidates.md#C-20260625T061044Z-A
promoted_issue_path: docs/issues/I-20260625T061044Z-A/issue.md
pre_tests_path: docs/epics/issue-sync-batch/verification/pre-tests.md
---

## 问题

scan 发现的同步任务中，大部分是机械操作（close/update/pull），但当前全部交给 Manager→Worker→AI 处理，浪费 token。

## 设计：两层处理

### 第一层：issue-sync batch（脚本层，daemon start 时执行）

只处理确定性的同步类型：

| 场景 | 操作 | 需要工位？ |
|------|------|:--:|
| 本地 terminal + 平台 open | issue-sync close | 是 |
| 平台 closed + 本地 open | 标记 platform_state=closed | 是 |
| 平台有 + 本地无 | raw-issue-pull | 是 |
| 本地有变更 | issue-sync update | 是 |
| 评论不同步 | issue-sync comment | 是 |

处理完的 item 从 scan 队列中移除，不交给 Manager。

### 第二层：scan（给 Manager 的）

只留下需要 AI 判断的：

| 场景 | 需要 AI？ |
|------|:--:|
| 新 raw issue（无工位） | 是（判断 fix/feat） |
| 进行中（有工位、状态不明） | 是（检查 worker） |
| 语义冲突 | 是（需人工判断） |

### 自动化命令链

需要工位的同步，脚本直接走完整 pipeline：

```
wt-create → issue-sync → commit → 
FREELY_SKIP_IBM_GATE pr-create → pr-review --verdict pass → 
pr-merge → wt-close
```

全自动，不经过 Manager/Worker/AI。

### 改动

- daemon start: 在 scan 之前先跑 issue-sync batch 自动化链
- batch 成功处理的 item 从 scan 结果中移除
- FREELY_SKIP_IBM_GATE 用于纯机械同步的 IBM 豁免
