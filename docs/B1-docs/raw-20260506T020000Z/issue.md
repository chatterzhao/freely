---
local_id: raw-20260506T020000Z
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
kind: raw
source_family: chat_inbox
created: 2026-05-06 02:00:00+00:00
platform_ids:
  github:
    issue_id: '284'
    url: https://github.com/chatterzhao/freely/issues/284
    synced_at: '2026-05-10T09:30:21Z'
updated_at: '2026-06-17T00:26:22Z'
primary_platform: github
created_at: '2026-05-10T09:30:21Z'
platform_state: closed
---

# raw-20260506T0200Z: 评论消费链路——DB → issue.md → 平台 三段状态追踪

## 现象

39 条 comment-type chat 全部 stuck 在 consumed=0：

- `raw-guidance`（35 条）— 目标 issue 不存在
- `raw-20260503-0945`（3 条）— 目标 issue 不存在
- `raw-20260503-1010`（1 条）— 目标 issue 不存在

0 条已消费，0 条 issue.md 中有 comment 节，0 条同步到平台。

## 评论生命周期

```
chats DB (consumed=0)
  │
  ├─ 工位存在 → cat >> issue.md ### comment-{id} → consumed=1
  │
  └─ 无工位 → 留在 DB，等 wt-create 触发消费
       │
       └─ AI 判定为噪声 → consumed=-1

issue.md ### comment-{id}
  │
  ├─ issue-sync → platform_ids.github.comment_id = xxx
  └─ issue-sync → platform_ids.gitee.comment_id = xxx

平台 (GitHub/Gitee)
  │
  ├─ active（存在）
  ├─ deleted（删除）
  └─ edited（修改）
```

## scan 应扫出的不达标点

| 序号 | 位置 | 不达标 | 检测方式 |
|---|---|---|---|
| 1 | DB | consumed=0，目标 issue 不存在 | 已有 `chat_comment_pending` |
| 2 | DB | consumed=0，目标 issue 存在但无工位 | 已有 |
| 3 | issue.md | comment 节无 platform_ids | 已有 `_count_unsynced` |
| 4 | 平台 | 已同步但被删除/状态变化 | 需要 API 查询 |

1-3 已有机制。4 需要平台 API 集成，本次不实现——它的触发条件是已有 comment_id，然后调 `gh issue view --json comments` / Gitee API 对比状态。

## 本次做

- scan 输出中 `chat_comment_pending` 标注目标 issue 是否存在
- 完善 `_count_unsynced` 逻辑（当前无数据可测，留占位）
