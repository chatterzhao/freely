---
local_id: raw-20260720T120329Z
kind: raw
phase_state: absorbed
platform_ids:
  gitee:
    issue_id: IK2EEZ
    url: https://gitee.com/zhaoquan/freely/issues/IK2EEZ
    synced_at: ''
primary_platform: gitee
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-20T20:03:52+08:00'
updated_at: '2026-07-20T20:03:52+08:00'
intake_id: ''
author: platform
channel: gitee
session_refs: []
---

\n\n## 问题

`agent-id.env` 已在架构上被 `agent_working` 表替代，但当前生产运行时仍存在未完成迁移，形成文件与数据库双真源。Manager、Worker、Reviewer 在启动、分配、handoff、评论唤醒、审查记录、存活恢复和关闭清理时可能得到不同身份与会话状态。

## 已确认的运行时缺陷

1. Worker/Reviewer 工位启动身份仍可能从 `agent-id.env` 解析；解析失败默认 `manager_01`，造成角色与 slot 漂移。
2. Worker 分配仍双写文件和 `agent_working`，DB RPC 失败被吞掉，可能出现文件有绑定、表无绑定。
3. A2A handoff 仍从文件读取具体 Worker，缺失时退化为字面值 `worker`，破坏具体 Agent 关联。
4. `freely comment` 仍从文件查找 worktree，表中有 Worker 但文件无记录时不会唤醒。
5. `agent_working.py` 调用 `agent_working.record_review` / `get_reviews`，DB daemon 没有对应 RPC handler，Reviewer verdict 无法形成持久化事实。
6. Reviewer 使用 UPDATE_ONLY；Worker 行未建立时 Reviewer session 可启动但注册失败，失败没有进入 A2A 阻塞状态。
7. watchdog 清理 dead session 时参数结构与 `agent_working.upsert` 协议不一致，旧 session 可能长期残留。
8. DB 已实现 `next_free_and_assign`，生产分配仍使用非原子的 `next_free` + `assign`，并发下可重复分配同一 Agent。
9. lifecycle scan、`agent-table-query --reconcile`、`pr-review-guarded`、`wt-close` 和 discuss 路径仍保留旧文件读取、写入或清理。
10. 现有测试偏向 mock/内联逻辑，没有证明真实 DB daemon 下 Manager → Worker → Reviewer → Worker/Manager 的完整闭环。

## 根因

原 `agent-id.env → agent_working` 迁移事项被标记 completed/absorbed，但验收只证明表结构和部分调用链存在，没有以“生产代码零读写旧文件”和“真实三角色端到端闭环”为完成条件。后续兼容 fallback 继续掩盖 DB 写入、注册和恢复失败。

## 期望架构

- `agent-table.toml`：仅保存静态 Agent pool 与 slot 配置。
- `agent_working`：唯一的 Agent—raw_key—worktree—role—session 运行时真源。
- `a2a_tasks`：唯一的跨 Agent 任务状态机与消息关联真源。
- `agent-id.env`：生产代码完全停止读取、写入和清理；历史治理文档可保留迁移记录。
- 缺少表记录或 DB RPC 失败必须显式阻塞/失败，不允许默认成 `manager_01` 或退回旧文件。

## 验收条件

1. 生产 runtime、CLI、watchdog、scan、review、comment、discuss、worktree lifecycle 中 `agent-id.env` 读写为零。
2. 身份解析统一通过 worktree/raw_key 查询 `agent_working`；未绑定时显式报错，不默认 Manager。
3. Worker/Reviewer 分配使用 DB 内原子分配与注册，失败可观测且不会启动无绑定 session。
4. 补齐 review record/get RPC，并验证 B1/B2/RED/dev/green verdict 可持久化、恢复和门禁消费。
5. watchdog dead/stale session 更新协议正确，重启后能够 resume 或明确创建新 session。
6. comment、handoff、review、close 全部仅依赖 `agent_working` + `a2a_tasks`。
7. 增加真实 DB daemon 端到端测试：Manager 委派 Worker → Worker 请求 Reviewer → Reviewer verdict → Worker retry 或 Manager 决策 → close 释放；覆盖 daemon 重启和 DB 不可用失败路径。
8. 增加回归门禁：能力目录生产代码出现 `agent-id.env` 即失败。

## 边界

当前 `freely-db` daemon silent-exit/WAIT 降级问题由已有 raw issue 处理；本 issue 聚焦 DB 恢复后仍独立存在的身份双真源和三角色协作闭环缺陷。
