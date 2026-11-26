---
schema_version: '1'
local_id: raw-20261125T122804Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4707'
    url: https://github.com/chatterzhao/freely/issues/4707
    synced_at: ''
  gitee:
    issue_id: IKY048
    url: https://gitee.com/zhaoquan/freely/issues/IKY048
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-25T12:28:05Z'
updated_at: '2026-11-25T12:28:13Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
severity: P1
---

# fix: issue-sync update 不同步正文 updated 行，raw-reconciliation 永久 block

workflow_kind: fix

## fix: issue-sync update 不同步正文 updated 行，raw-reconciliation 永久 block

| Field | Value |
|-------|-------|
| local_id | `raw-20261125T122804Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-25T12:28:05Z |
| updated | 2026-11-25T12:28:05Z |

---

> **Freely 治理**：这是 raw issue `raw-20261125T122804Z`。实现前请用 `wt-create --raw-key 20261125T122804Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象
`issue-sync update raw-<key>` 刷新本地 frontmatter `updated_at`，但不刷新正文表格里的 `| updated | <ts> |` 行。于是 `_issue_body` 用 frontmatter 的新时间戳生成平台 body，而本地正文表格仍是旧值 → raw-reconciliation 判 `content_diverged`，`pr-create-guarded` 永久 block。

## 实证（#4702 收口现场，重复 3 次）
- 本地 frontmatter `updated_at: 2026-11-25T11:05:19Z`，正文表格 `| updated | 2026-11-25T09:41:13Z |`。
- 平台 body updated=11:05:19Z（由 `_issue_body` 从 frontmatter 生成），本地 body updated=09:41:13Z。
- `pr-create-guarded` 报 `content_diverged`，即使刚执行过 `issue-sync update`。
- 每次都要手工改正文表格再 update 一次才能通过——#4699 和 #4702 都踩了。

## 根因
`issue_create_contract.platform_body()`（:189, :213）用 `metadata.get('updated_at')` 生成 `| updated |` 行；而写入 frontmatter `updated_at` 的路径（promote/close/absorb 等）不回写正文表格。两者形成结构性漂移。

## 期望
1. `issue-sync update`（或 `_issue_body` 生成路径）在写平台前，先把正文的 `| updated |` 行对齐到 frontmatter `updated_at`（或反之），保证本地 canonical body 与平台 body 一致。
2. 或：raw-reconciliation 的 `canonical_projection` 排除 `| updated |` 这类纯元数据行（类似已排除 phase/* 标签），避免时间戳漂移被当内容分歧。
3. 两条路径选一，须有 AT 钉住：update 后 `pr-create-guarded` 的 raw-reconciliation 必须通过，无需手工改正文。

## 验收建议
- 最小复现：构造 frontmatter updated_at 与正文 | updated | 不一致的 raw → `issue-sync update` 后 reconcile 必须 ok。
- 回归：#4699/#4702 现场场景不再需要手工同步正文时间戳。

## 非目标
不改 platform_body 的其他字段语义；不夹带 #4702（已合并）、#4703、#4704、#4698、#4687。
