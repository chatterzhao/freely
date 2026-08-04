---
b1_id: B1-20260720T120329Z
phase_state: completed
source_raw: raw-20260720T120329Z
source_url: https://github.com/chatterzhao/freely/issues/4064
produced_candidates:
  - C-20260720T120329Z-A
  - C-20260720T120329Z-B
  - C-20260720T120329Z-C
created_at: 2026-07-20
---

# B1_IBM: agent-id.env 退役与三角色协作单真源收敛

## Input
- **来源**: GitHub #4064 / Gitee IK2EEZ
- **问题**: `agent-id.env` 文件与 `agent_working` DB 表形成双真源，导致 Manager/Worker/Reviewer 在启动、分配、handoff、review、comment、watchdog、lifecycle 等路径得到不一致的身份与会话状态

## Discovery — 代码搜索证据

### agent-id.env 仍在生产代码中的引用（freely 脚本 9 处）

| 行号 | 功能 | 操作 | 缺陷编号 |
|------|------|------|---------|
| L309-365 | `_agent_working_shim` | agent_working → fallback agent-id.env | #1/#4 |
| L340/L371 | `_resolve_current_agent_id` | 解析失败默认 `manager_01` | #1 |
| L4323-4338 | Worker startup identity | 读 agent-id.env | #1 |
| L4832-4835 | 另一身份解析点 | agent_working → fallback agent-id.env → `manager_01` | #1 |
| L6014-6065 | Worker assignment | **双写** agent-id.env + agent_working | #2 |
| L12935-12947 | Zombie cleanup | 读 agent-id.env 文件 | #9 |
| L13881 | A2A handoff | 读 agent-id.env 取 worker ID，缺失时 fallback `worker` | #3 |
| L24606-24607 | Discuss | **写** agent-id.env | #9 |
| L24726 | Lifecycle | 读 agent-id.env | #9 |

### agent-id.env 在 scan 中的引用

| 文件 | 行号 | 操作 |
|------|------|------|
| task-lifecycle-scan.py | L886-910 | agent_working primary → agent-id.env fallback → "both missing" |

### DB daemon 缺口（freely_db_manager.py）

| 缺口 | 缺陷编号 | 现状 |
|------|---------|------|
| `agent_working.record_review` RPC handler | #5 | **不存在**。agent_working.py L282 调用但 DB 无 handler |
| `agent_working.get_reviews` RPC handler | #5 | **不存在**。agent_working.py L308 调用但 DB 无 handler |
| `agent_working.next_free_and_assign` | #8 | Handler 存在（L1489）但生产代码未使用 |
| Watchdog session update 协议 | #7 | 与 `agent_working.upsert` 参数结构不匹配 |

### 已迁移的路径（无需修改）
- `pr-review-guarded`: 无 agent-id.env 引用 ✅
- `wt-close`: 无 agent-id.env 引用 ✅

## Problem — 逐缺陷根因分析

### D1: 身份解析仍依赖 agent-id.env + manager_01 默认值
`_resolve_current_agent_id` (L340, L4323, L4832) 三个站点都先查 agent_working，失败则 fallback 到 agent-id.env，再失败则默认 `manager_01`。Worker 工位被误识别为 Manager → 错误 slot → 错误 AI tool → 错误行为链。

### D2: Worker 分配双写
L6014-6065: `agent-table: assign` 先写 agent-id.env 文件，再调 `agent_working` RPC。如果 DB RPC 失败（`|| true` 吞错误），文件有绑定但表无绑定 → 文件真源与 DB 真源分歧。

### D3: A2A handoff 读文件取 Worker
L13881: `grep agent-id.env` 取 worker ID，缺失时 `|| echo "worker"` — 字面值 `worker` 不是合法 agent ID，导致 A2A task 投递到不存在的 Agent。

### D4: Comment 唤醒依赖文件
`_agent_working_shim` (L309-365) 查 agent_working 失败则 fallback 读 agent-id.env。表中有 Worker 但文件无记录时 → 不唤醒。

### D5: Review RPC 缺失
`agent_working.py` 有 `agent_record_review()` (L282) 和 `agent_get_reviews()` (L308) 但 `freely_db_manager.py` 无对应 `@_h("agent_working.record_review")` / `@_h("agent_working.get_reviews")` handler。调用时 DB 返回 error response → Reviewer verdict 无法持久化。

### D6: Reviewer UPDATE_ONLY 启动
`agent_working.py` `acp_session_register` 对 reviewer role 使用 UPDATE_ONLY 语义。Worker 行未建立时 Reviewer 启动但不注册到 `agent_working` → 无绑定 session → verdict 无处可写。

### D7: Watchdog 清理协议不匹配
Watchdog dead/stale session 更新与 `agent_working.upsert` 参数结构不一致 → 旧 session 残留 → `agent_next_free` 误认为 Agent 仍被占用 → 无法分配。

### D8: 非原子分配
生产代码调 `agent_next_free` + `agent_assign`（两次独立 DB RPC），而 DB daemon 已有 `next_free_and_assign`（单次原子 RPC）。并发下两个 Manager/Worker 可能分配到同一 Agent。

### D9: Tooling 路径残留
scan.py (L886-910)、discuss (L24606)、zombie cleanup (L12935) 仍读写 agent-id.env。

### D10: 测试覆盖不足
现有测试 (`test_agent_working_logic.py`, `test_integration_lifecycle.py`) 偏向 mock/内联逻辑，无真实 DB daemon 下端到端三角色闭环测试。

## Brainstorm

### Option A: 全量一次性迁移（不推荐）
一次 commit 移除所有 agent-id.env 引用 + 补齐所有 DB handler + 切原子分配 + E2E 测试。

**优点**: 一次完成
**缺点**: scope 过大（~15 处代码改动 + 2 个新 RPC handler + 测试），review 困难，回滚粒度粗，一个子问题阻塞全部
**评估**: 不可接受 — 违反"小步快跑"原则

### Option B: 分阶段迁移（推荐）

**C-A: DB 基础设施补齐**（无运行时消费者依赖，独立可验收）
- 新增 `agent_working.record_review` RPC handler → `freely_db_manager.py`
- 新增 `agent_working.get_reviews` RPC handler → `freely_db_manager.py`
- `agent_working.py`: `agent_next_free` 改用 `next_free_and_assign`（原子）
- `agent_working.py`: 修复 Reviewer UPDATE_ONLY → INSERT_OR_UPDATE
- `agent_working.py`: 修复 watchdog session update 协议
- **验收**: review 可写可读、原子分配可并验证、Reviewer 注册成功

**C-B: 运行时统一到 agent_working**（依赖 C-A）
- 移除 `_resolve_current_agent_id` 三个站点的 agent-id.env fallback
- Worker assignment 移除 agent-id.env 双写，仅写 agent_working
- A2A handoff L13881 改为查 agent_working
- Comment 唤醒 `_agent_working_shim` 移除 agent-id.env fallback
- Discuss L24606-24726 改读/写 agent_working
- scan.py L886-910 移除 agent-id.env fallback
- Zombie cleanup L12935-12947 改用 agent_working 查询
- `agent_working` 查询失败 → 显式报错退出，不默认 `manager_01` 或 `worker`
- **验收**: `grep -r "agent-id.env"` 在生产代码中零命中（除治理文档）

**C-C: 测试与回归门禁**（依赖 C-A, C-B）
- 新增 E2E 测试：真实 DB daemon → Manager 委派 Worker → Worker 请求 Reviewer → Reviewer verdict 持久化 → Worker retry/Manager 决策 → close 释放
- 覆盖 daemon 重启恢复、DB 不可用失败路径
- 新增回归门禁：`rg 'agent-id\.env' <production-dirs>` 发现引用即 CI fail
- **验收**: E2E 通过，门禁生效

### Decision: Option B — 三候选分阶段

**理由**:
1. C-A 是纯 DB 层改动，不涉及运行时行为变更 → risk 最低、review 最清晰
2. C-B 是统一的大规模替换，但依赖 C-A 的 DB 接口稳定 → 可以等 C-A merge 后独立推进
3. C-C 是质量保障层 → 可以等 A+B merge 后推进
4. 每个 candidate 独立可 promote → 不被其他子问题阻塞

**C-A 与 C-B 的边界清晰**:
- C-A 只改 `freely_db_manager.py` + `agent_working.py`
- C-B 只改 `freely` (shell) + `task-lifecycle-scan.py`
- 没有文件交叉

## Candidates

### C-20260720T120329Z-A: DB 基础设施补齐
- status: promoted
- priority: P0 — C-B 和 C-C 的阻塞依赖
- scope: freely_db_manager.py + agent_working.py

### C-20260720T120329Z-B: 运行时 agent-id.env 退役
- status: promoted
- priority: P1 — 依赖 C-A
- scope: freely + task-lifecycle-scan.py（~9 处 agent-id.env 引用清零）

### C-20260720T120329Z-C: E2E 测试与回归门禁
- status: promoted
- priority: P2 — 依赖 C-A + C-B
- scope: tests/ + CI gate
