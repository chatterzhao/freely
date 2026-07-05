---
local_id: raw-20260505T121000Z00Z
issue_title: "issue 状态字段重构：分离 platform_state 和 phase_state，统一 raw/I-* 字段规范"
kind: raw
phase_state: completed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '214'
    url: https://github.com/chatterzhao/freely/issues/214
primary_platform: github
created_at: '2026-05-05T12:10:02Z'
intake_id: 20260505T1210Z-issue-state-refactor
author: human
channel: github
session_refs: []
platform_state: 
---

## 问题

当前 issue（raw 和 I-*）的状态管理混乱：

1. 跨层污染：issue-sync close 把平台层的 closed 写入 raw 的 status，覆盖 absorbed
2. 字段混用：raw 和 I-* 都有 status 字段，语义不同
3. 平台状态缺失：没有显式字段追踪 GitHub/Gitee issue 的 open/closed
4. scan 常量与 IBM Framework §89 不一致

## 四层状态模型

| 层 | 存储 | 字段 | 取值 |
|----|------|------|------|
| chat-inbox | .freely/freely.db | consumed | -1/0/1 |
| raw issue | docs/B1-docs/raw-*/ | status | proposed→absorbed/dropped |
| I-* issue | docs/issues/I-*/ | phase_state | in_b2_ibm→…→completed |
| 平台 issue | GitHub/Gitee API | state | open/closed |

## 目标

1. 新增 platform_state: open|closed 字段
2. raw 只用 status，I-* 只用 phase_state
3. raw 和 I-* 共享同一平台 issue
4. issue-sync 只写 platform_state
5. scan 常量对齐 IBM Framework §89
6. 门禁拦截状态不一致

## 平台

platform: github
platform_issue_id: 214
