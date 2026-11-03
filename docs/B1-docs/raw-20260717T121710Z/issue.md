---
local_id: raw-20260717T121710Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '3977'
    url: https://github.com/chatterzhao/freely/issues/3977
    synced_at: ''
  gitee:
    issue_id: IK1TMQ
    url: https://gitee.com/zhaoquan/freely/issues/IK1TMQ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-17T12:17:33Z'
updated_at: '2026-07-17T12:17:33Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因

a2a_task.py a2a-exit --state submitted --role worker 创建 A2A submitted task 后，Runtime 的 worker launch verification 阻断所有 worker 启动。

## 影响

- 49 个 scan items 全部无法推进: 14 merged_develop、15 i_non_terminal、20 raw_not_started
- 所有新创建的 worktree 降级为 agent_dead/僵尸工位（已在 round 040 和 041 中验证）
- 前轮（040）曾创建 raw-20260717T103026Z 但未进入 scan/B1-docs，已丢失

## 历史

- Round 040: 首次发现，清理 2 个 agent_dead 工位，创建原始 raw issue
- Round 041: 尝试 chain_trace 迁移模式（feedback → wt-create → delegate），worker 0dc8219e 再次 blocked
- Round 042: 当前轮，清理僵尸工位 20260717T121252Z，重新创建此 issue

## 修复建议

需要检查:
1. Runtime 如何检测 submitted A2A tasks 并启动 worker
2. watchdog_sse 或 ACP session 连接逻辑
3. launch_verification 的条件是什么，为何始终 block
4. 是否存在 missing worker_pid、stale_state 或 session 初始化问题

## 复现步骤

1. freely feedback → 获得 raw key
2. freely wt-create --raw-key <key> --source platform --kind fix --slug test
3. a2a-exit --state submitted --role worker --worktree <path> --branch <branch> --raw-key <key>
4. Worker 立即退出: exit=manager_worker_launch_verification_blocked
