---
local_id: raw-20260503T094500Z
kind: raw
priority: high
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
source: platform
platform_ids:
  gitee:
    issue_id: IJKTEJ
  github:
    issue_id: '375'
    url: https://github.com/chatterzhao/freely/issues/375
    synced_at: '2026-05-16T13:22:19Z'
created_at: '2026-05-03T09:45:00Z'
title: 'feat: migrate scan results and issue-sync state to SQLite'
platform_state: closed
updated_at: 2026-05-17T04:47:25Z
primary_platform: github
---
## 问题
scan JSON 和 .scan-state 分散两处，后者误在 git-tracked 目录。
入 SQLite 后可查询、有历史、事务更新、JOIN 关联、webhook 直写。

## 要求
- 将 scan 结果从 JSON 迁移到 SQLite
- issue-sync 状态也入同一个 DB
- 移除 .scan-state 文件

## 讨论
### 2026-05-03 09:50 (chat)
wt-create sync 时机: 工位创建时按分支 key 只 sync 对应 issue。
当前 _materialize_chat_if_needed 只处理 chat-inbox 来源，需加 _sync_platform_issue_if_needed 处理平台来源（GitHub/Gitee 直接开的 issue）

### 2026-05-03 09:53 (chat)
raw issue 来源是并列可选——chat_inbox 或 chain_trace(平台)。
scan 的 source_family 字段已区分。wt-create 只需看 source_family:
- chat_inbox → materialize from SQLite
- chain_trace → 从平台 API fetch
scan 是唯一真相源，不需要额外渠道。

### 2026-05-03 23:50 (chat)
协调：GitHub #190 (freely start --task <scan-id>) 需要 scan 有统一的 scan-id。
建议 scan 入 SQLite 时用 PRIMARY KEY 作为 scan-id。
两个 issue 配合：IJKTEJ 做 scan→SQLite 重构 → #190 做 --task 模式。
