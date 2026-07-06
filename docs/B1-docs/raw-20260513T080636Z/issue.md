---
local_id: raw-20260513T080636Z36Z
kind: raw
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
source_candidate: docs/B1-docs/raw-20260513T080636Z36Z/candidates.md#C-20260513T080636Z-A
priority: P2
source: platform
created_at: '2026-05-13T09:49:13Z'
title: '[RAW-20260513T080636Z] raw-20260513T080636Z36Z'
updated_at: '2026-06-17T00:25:19Z'
platform_ids:
  github:
    issue_id: '330'
    url: https://github.com/chatterzhao/freely/issues/330
    synced_at: '2026-05-13T09:49:13Z'
primary_platform: github
platform_state: closed
---

## raw-20260513T080636Z36Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260513T080636Z36Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-13T08:06:36Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260513T080636Z36Z`。实现前请用 `wt-create --raw-key 20260513T080636Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-13T08:06:36Z"
title: "governance: update phase_state to completed for ACP issues already merged to develop"

## 问题

以下 ACP issue 的代码已合并到 develop，但 issue 文档的 phase_state 未更新：

### 1. I-20260508T225041Z-A (ACP bridge restart cooldown)

- 代码已合并：`62ae0ef2` (test-pre-merge-20260508T225041Z-acp-bridge-restart-storm → develop)
- tasks.md 全部 [x]，code-review 存在
- 当前 `phase_state: in_b2_ibm` → 应为 `completed`
- 缺少 `platform_state` 字段

### 2. I-20260503T000000Z-A (ACP bridge crash resilience)

- 代码已合并：`7851a9a0` (hotfix/acp-bridge-crash-resilience-20260502 → develop)
- 短路径 issue.md 已正确标记 `phase_state=completed`，但 canonical epic issue 仍写 `phase_state: in_dev`
- 需同步 canonical epic 文档

### 修复方式

两个 issue 都只缺状态标记更新，不涉及代码变更。可以直接更新 frontmatter + 更新 milestones.md，用 break-glass 跳过 IBM 门禁合并。

文件：
- `docs/issues/I-20260508T225041Z-A/issue.md` — phase_state → completed
- `docs/B2-docs/acp/acp-bridge-crash-resilience/raw-20260503-0000issues/I-20260503T000000Z-A.md` — phase_state → completed
- `docs/milestones.md` — 同步 milestone 状态
