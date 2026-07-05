---
local_id: raw-20260625T044836Z36Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3477'
    url: https://github.com/chatterzhao/freely/issues/3477
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T04:48:55Z'
updated_at: '2026-06-25T04:48:55Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T044836Z-A
source_candidate: docs/B1-docs/raw-20260625T044836Z36Z/candidates.md#C-20260625T044836Z-A
promoted_issue_path: docs/issues/I-20260625T044836Z-A/issue.md
pre_tests_path: docs/B2-docs/issue-sync-filter/verification/pre-tests.md
---

## 问题

issue-sync batch 遍历全部 docs/issues/ 的每个 issue，逐个比对本地和平台状态。issue 越多越慢。

## 设计

### 过滤：只看有至少一方 open 的 issue

scan 并集逻辑：
- 本地 platform_state != closed（或为空/不存在）
- 平台上 state = open
- 两边取并集 → 只有这些 issue 需要处理
- 全 close → 跳过

### 分类处理

| 场景 | 本地 | 平台 | 动作 |
|------|------|------|------|
| 已完成未同步 | completed/absorbed | open | issue-sync close（直接推送） |
| 未开始 | proposed，无工位 | open | feedback + wt-create 创工位 |
| 进行中 | 非 terminal，有工位 | open | 检查 worker agent 状态 |
| 无本地 | 不存在 | open | adapter pull 创建本地 |

### 收益

- 200+ issue 中已完成的大部分直接跳过
- 只有 ~10-20 个不一致的需要处理
- scan 速度从分钟级降到秒级
