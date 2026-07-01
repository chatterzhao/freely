---
b1_id: B1-20260701T085407Z
phase_state: completed
source_raw: raw-20260701T085407Z
source_url: https://github.com/chatterzhao/freely/issues/3697
produced_candidate: C-20260701T085407Z-A
created_at: 2026-07-01
---

# B1_IBM: A2A reviewer agent — 最终收敛架构 + TODO

## 1. 最终收敛架构

### 三角色 + Worktree 绑定

| 角色 | 工位 | Agent ID | 职责 |
|------|------|---------|------|
| Manager | develop | manager_01 | 巡逻、委派、收口 |
| Worker | fix/raw-{key} | worker_01..10 | B1/B2/RED/dev/test |
| Reviewer | test-pre-merge-{key} | reviewer_01..99 | 每步审查、门禁检查 |

### ACP vs A2A

```
ACP: agent ↔ AI CLI tool (垂直，装大脑)
A2A: agent ↔ agent        (水平，协作)

ACP 管: session/new|fork|resume|close, slot, conversation_id
A2A 管: task 生命周期, agent card, SSE 推送, state machine
两者正交。同一 ACP process 多 session。同一 A2A task 跨 daemon 重启。
```

### agent-table.toml v2 (扁平)

```toml
[[agents]]                          [[agents]]
role = "manager"                    role = "worker"
manager_id = "manager_01"           worker_id = "worker_01"
manager_slot = "..."                worker_slot = "..."
pool = 1                            pool = 10

[[agents]]
role = "reviewer"
reviewer_id = "reviewer_01"
reviewer_slot = "..."
pool = 99
```

### agent_working 表 (SQLite)

```sql
CREATE TABLE agent_working (
    raw_key         TEXT PRIMARY KEY,
    worktree        TEXT NOT NULL,
    branch          TEXT NOT NULL,
    test_worktree   TEXT,
    test_branch     TEXT,
    manager_id      TEXT,       -- manager_01:ses_abc
    worker_id       TEXT,       -- worker_03:ses_def
    reviewer_id     TEXT,       -- reviewer_05:ses_ghi,reviewer_08:ses_jkl
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
```

值格式: `agent_id:session_id`。无 session 时仅有 agent_id。
reviewer 逗号隔开多个 `agent_id:session_id` 对。agent-id.env 完全废弃。

### Runtime Watchdog = Bootstrapper

```
Runtime 介入 (ACP session)     Runtime 不介入 (A2A SSE 直连)
─────────────────────────     ─────────────────────────────
检测 needs-review              Worker↔Reviewer 互推状态
Reviewer 不存在 → 创建 ACP     Reviewer→Worker verdict 推送
Agent crash → 重新启动         正常 state 变更
Daemon 重启 → resume           working/completed 更新
```

### 配对：靠 raw_key，不靠 NN

worker_03 和 reviewer_05 无需 NN 匹配。通过 raw_key 关联：
同一 raw_key 的 dev worktree 和 test worktree，A2A task 携带 raw_key + parent_agent。

### input-required 6 向路由

| # | 方向 | reason | 处理者 | ACP |
|---|------|--------|--------|-----|
| 1 | Worker→Reviewer | needs-review:b1/b2/dev | Reviewer | session/fork 或 new |
| 2 | Worker→Manager | needs-manager-decision | Manager | session/resume |
| 3 | Reviewer→Worker | needs-worker-retry | Worker | session/resume |
| 4 | Reviewer→Manager | needs-manager-scope | Manager | session/resume |
| 5 | Manager→Reviewer | needs-review:gate | Reviewer | session/new |
| 6 | Manager→Worker | needs-worker-task | Worker | session/resume/fork |

### Card 设计 (roles.toml)

```
docs/system/workspace/agents/roles.toml  ← git tracked, 纯能力声明

[manager]   skills: workflow-guarded-execution, branch-management
[worker]    skills: B1, B2, RED, dev, test
[reviewer]  skills: tdd-review, candidate-acceptance-review

不提 slot，不提 pool。
Slot 在 ACP session 创建时从 agent-table 读取。
```

## 2. 关键决策

| # | 决策 | 理由 |
|---|------|------|
| D1 | Runtime 是 bootstrapper 不是 mediator | A2A 协议原生模式是 agent 直连 |
| D2 | Manager 创建 A2A task，Runtime 只创建 ACP session | Manager 有编排上下文 |
| D3 | 配对靠 raw_key 不靠 NN | 解耦 pool 大小，10 worker + 99 reviewer |
| D4 | agent_working SQLite 替代 agent-id.env | 事务、索引、SQL 查询空闲 |
| D5 | session 嵌在 agent_id 列 (冒号分隔) | 无需额外列，一列同时读 |
| D6 | Reviewer 独立 slot | 可用不同 AI 工具，独立 rate limit |
| D7 | 单文件 roles.toml | 简化维护 |
| D8 | reviewer_id 逗号分隔 (不拆表) | 写入串行，无并发冲突 |
| D9 | 6 种双向 input-required | 无遗漏处理场景 |
| D10 | review_stage 字段 | 区分 b1/b2/dev 审查阶段 |
| D11 | session/fork 同 tool, session/new 跨 tool | 复用连接，减少开销 |
| D12 | 轮询降级为 SSE fallback | 主路径 SSE，断连时回退 |

## 3. TODO List

### P0: Bug Fix
- [ ] P0.1 修 _restore_tasks L403/442/663 and/or 优先级 (加括号)
- [ ] P0.2 修 L442 变量引用 bug (统一用 agent_id)
- [ ] P0.3 reviewer 专属 _restore_tasks 分支 (working + input-required)
- [ ] P0.4 语法 + 逻辑验证

### P1: agent_working 表 + CRUD
- [ ] P1.1 建表 (freely.db migration)
- [ ] P1.2 agent_session_set/get/remove
- [ ] P1.3 agent_working_next(role, pool) / agent_working_free(role, pool)
- [ ] P1.4 agent_working.py 模块 + 单元测试

### P2: agent-table-query 重写
- [ ] P2.1 废弃 --get-reviewer
- [ ] P2.2 --get-slot 适配 v2 格式
- [ ] P2.3 新增 --next-free, --list-role, --pool-size
- [ ] P2.4 更新所有调用方 + 格式验证

### P3: agent-id.env → agent_working 全局替换
- [ ] P3.1 定位所有读写 agent-id.env 位置
- [ ] P3.2 读 → SELECT agent_working
- [ ] P3.3 写 → agent_session_set
- [ ] P3.4 删 → agent_session_remove
- [ ] P3.5 wt-create/wt-close 移除 agent-id.env 逻辑

### P4: ACP Session 管理
- [ ] P4.1 _ensure_reviewer_agent(reviewer_id, parent_worktree)
- [ ] P4.2 ensure_manager_once 写 agent_working
- [ ] P4.3 launch_worker: next_free + agent_session_set
- [ ] P4.4 wt-close: session/close + agent_session_remove + 删除行

### P5: A2A Multi-Card + Task
- [ ] P5.1 agent-card?role= 端点 + roles.toml
- [ ] P5.2 Manager POST /tasks 委派 Worker
- [ ] P5.3 Manager POST /tasks 委派 Reviewer
- [ ] P5.4 PATCH /tasks/{id} SSE 推送 + 订阅过滤
- [ ] P5.5 review_stage 字段 (b1/b2/dev/red/test/gate)
- [ ] P5.6 Worker state 变更 → SSE push (替代轮询)

### P6: Watchdog SSE
- [ ] P6.1 SSE 订阅 + 重连 (exponential backoff)
- [ ] P6.2 needs-review → 创建 Reviewer session
- [ ] P6.3 needs-manager-decision → resume Manager
- [ ] P6.4 needs-worker-retry → resume Worker
- [ ] P6.5 needs-manager-scope → resume Manager
- [ ] P6.6 轮询降级为 30s fallback
- [ ] P6.7 任务僵死检测 (working > N min → stall event)
- [ ] P6.8 SSE 集成测试

### P7: roles.toml
- [ ] P7.1 创建 docs/system/workspace/agents/roles.toml
- [ ] P7.2 三角色 skills 定义
- [ ] P7.3 确认 git tracked (不含 slot/pool)
- [ ] P7.4 agent card 端点读取 roles.toml

### P8: input-required 双向路由
- [ ] P8.1 规范 input-required schema (task_id, reason, raw_key, review_stage, parent_agent)
- [ ] P8.2 Worker→Reviewer 路由
- [ ] P8.3 Worker→Manager 路由
- [ ] P8.4 Reviewer→Worker 路由
- [ ] P8.5 Reviewer→Manager 路由
- [ ] P8.6 Manager→Reviewer 路由
- [ ] P8.7 Manager→Worker 路由
- [ ] P8.8 路由验证测试

### P9: 生命周期集成
- [ ] P9.1 wt-close: session/close + release + 删行 + 删 worktree
- [ ] P9.2 freely-cycle: dispatch_reviewer 实际执行 (不再只是建议)
- [ ] P9.3 僵死检测 + 孤儿 worktree 清理
- [ ] P9.4 Daemon 重启恢复 agent + SSE 重新订阅

## Candidate

- candidate_id: C-20260701T085407Z-A
- status: promoted
- milestone: M-20260701T085407Z-A
- promoted_issue_id: I-20260701T085407Z-A
- decision_reason: 基于 A2A/ACP 协议 + Zed 参考 + 3 轮 subagent 审查 + 12 项关键决策
- next_action: B2 设计 → 逐 Phase 实现 → PR
