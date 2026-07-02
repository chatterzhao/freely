# Review 06: Three-Loop + Agent 协作模型

- owner_issue: raw-20260701T085407Z
- date: 2026-07-01

## Three Loops

```
Loop 1: Doc Loop (发现/设计)
  Manager patrol → 发现待办 → 委派 Worker → B1 预研
  → Reviewer 审查 B1 → pass? → B2 设计
  → Reviewer 审查 B2 → pass? → 进入 Loop 2

Loop 2: Dev Loop (执行/验证)  
  RED → Reviewer 审查 → pass? → dev 实现
  → Reviewer 审查 dev → pass? → test-GREEN
  → Reviewer 审查 test → pass? → 进入 Loop 3

Loop 3: Auto Loop (收口/治理)
  pr-create → pr-review → pr-merge → wt-close
  Runtime 参与: freely restart, agent crash recovery, cleanup
```

## Agent 协作如何完成 Loop

```
Loop 内 worker-reviewer 循环:

  Worker 完成一步
    ↓
  Reviewer 审查
    ↓
  ┌─ pass? ──→ 进入下一步 (loop 推进)
  │
  └─ fail? ──→ Worker 按 guidance 修改 → 重新 Review
       ↑                                    ↓
       └──────────── 同一 loop 内迭代 ─────────┘
```

**关键**：一个 workflow 步骤可能经历多轮 review。
比如 B1 不达标 → Reviewer 说"根因分析不充分" → Worker 重做 → 再审查 → 通过。

## Agent vs Runtime 分工

```
Agent 负责:                    Runtime 负责:
─────────────────────          ────────────────────
Loop 内的执行和审查             Loop 间的状态管理
Worker 做 skill                启动/停止 agent (ACP session)
Reviewer 审查产物               检测 agent 崩溃
Manager 委派和收口              重启恢复 (freely restart)
写 agent_working 表             维护 session-store
写 a2a_tasks 状态               SSE 订阅和路由
                                agent_working 清理
```

## 每个 workflow 步骤的 Review 规则

| 步骤 | 谁审查 | 审查什么 | pass 后 | fail 后 |
|------|--------|---------|---------|---------|
| B1 预研 | Reviewer | brainstorms 根因分析是否充分 | 进入 B2 | 重做根因分析 |
| B2 设计 | Reviewer | PRD/pre-tests 是否覆盖改动面 | 进入 RED | 修正设计 |
| RED | Reviewer(可选) | 测试是否真正 RED | 进入 dev | 修正测试 |
| dev | Reviewer | 代码是否按 TDD 实现 | 进入 test | 修正代码 |
| test | Reviewer | 测试是否全 GREEN | 进入 pr-create | 修正实现 |
| pr-create | gate(自动) | epics-map, IBM lifecycle | 进入 pr-merge | 修正治理文档 |
| pr-merge | gate(自动) | merge receipt, governance | 进入 wt-close | 修正冲突 |

## Auto Loop 需要 Runtime 参与

```
Auto Loop 的特殊性:
  - pr-create/pr-merge 是 bin 命令，不经过 agent
  - freely restart 恢复 → Runtime 读 agent_working → resume agent
  - agent crash → Runtime Watchdog 检测 → restart agent
  - wt-close → Runtime 清理 agent_working + worktree
  - session/close 封装在 wt-close 内
```

## 当前实现状态

| Loop | Agent 部分 | Runtime 部分 |
|------|-----------|-------------|
| L1 Doc | Manager ✅ Worker ✅ | Reviewer ❌ (无 ACP session) |
| L2 Dev | Worker ✅ | Reviewer ❌ SSE push ❌ |
| L3 Auto | pr-create/merge ✅ | restart ❌ crash recovery ❌ wt-close agent clean ❌ |

核心缺口: Reviewer agent 启动 + SSE 推送 + restart 恢复。都卡在同一个地方——ACP session 创建和 SSE 集成未接入 Runtime。
