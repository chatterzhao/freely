---
local_id: raw-20260514T103532Z32Z
kind: raw
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '344'
    url: https://github.com/chatterzhao/freely/issues/344
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-14T10:35:46Z'
updated_at: '2026-06-17T00:21:49Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## raw-20260514T103532Z32Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260514T103532Z32Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-14T10:35:32Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260514T103532Z32Z`。实现前请用 `wt-create --raw-key 20260514T103532Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P1
status: open
source: chat-inbox
created_at: "2026-05-14T10:35:32Z"
title: "design: agent handoff protocol — handoffs 表作为 manager-worker 交接媒介的字段语义、消费状态机与多轮连续性"

## 问题

#343 暴露了 manager-worker 交接管道的断裂——validator 读 worker_prompts_csv（manager handoff），launcher 读 pending worker 记录——两个读者读不同字段导致静默失败。但这只是症状。

更深层的问题是：handoffs 表作为 manager 和 worker 之间的唯一共享交接媒介，它的字段语义、值的消费状态机、以及多轮对话的连续性都没有被完整定义。

当前 handoffs 表有 parent_handoff_id 字段但 runtime 从不写入，有 consumed_by 字段但完全未使用，没有 thread_id 来串联同一任务的多轮交接，WORKER_HANDOFF_INJECT 只注入自己的 handoff_id 而不注入父记录、线程和前任上下文。

## 影响

- Worker 不知道它是不是某个多轮任务的第二轮——查不到上一轮的交接内容
- Manager 巡逻时看到多个 completed worker 记录，无法区分哪些属于同一个对话线程、哪些已经消费过
- 同一 issue 的多次委派（纠正、换方案、继续推进）在 handoffs 表中是孤立的记录，没有显式的线程归属
- 缺少 consumed 状态导致主管只能靠人工记忆判断是否已处理某个 worker 的完成

## 研究目标

设计完整的 agent handoff protocol，确定：
1. handoffs 表每个字段的语义、写入者、写入时机
2. 记录的状态机和合法转换
3. 多轮 manager-worker 对话的连续性机制（thread_id, parent_handoff_id, previous_worker_handoff_id）
4. 消费语义：主管如何标记已读，runtime 如何自动推进状态
5. Worker Prompt 注入的完整上下文

---

## 吸收子修复：SELF_ROOT 自动检测（#345）

开发过程中发现 `workspace_root_for_project` / `runtime_script_for_project` 返回项目路径导致安装版 Worker 加载旧脚本。`SELF_ROOT` 已能自动检测启动位置，修复在 38903ab8、3554b7b6。此修复吸收进 I-20260514T103532Z-A，不再另开工位。
