---
b1_id: B1-20260709T142056Z
phase_state: completed
source_raw: raw-20260709T142056Z
source_url: https://github.com/chatterzhao/freely/issues/3843
produced_candidate: C-20260709T142056Z-A
created_at: 2026-07-09
---

# B1_IBM: doc gate 检查了非 agent 注入的过程文档

## Input
- raw issue #3843: doc gate 阻塞 daemon 启动
- 根因：`check_doc_gate_or_fail` 要求 7 个文件，其中 3 个不是 agent 注入治理文档

## Problem
`check_doc_gate_or_fail` (June 23 引入) 要求以下文件存在才能启动 daemon：
1. `CONSTITUTION.md` ✅ agent 注入
2. `LAWS.md` ✅ agent 注入
3. `PROJECT_INTENT.md` ✅ agent 注入
4. `AGENTS.md` ✅ agent 注入
5. `docs/B1-docs/README.md` ❌ 路径错误，全项目零消费者
6. `docs/B1-docs/INDEX.md` ❌ 死代码消费者，架构已迁移
7. `docs/B1-docs/CONVERGENCE.md` ❌ 临时落点，从未使用

Daemon 自从停止后无法重启，因为 `freely init` 从未创建 5-7 这三个文件。

## Discovery
### 价值判断：值得修
- daemon 无法启动是 P0 阻塞问题
- 3 个文件不属于 agent 注入链路，不应阻塞启动

### 覆盖域
| 文件 | 判定 | 理由 |
|------|------|------|
| `B1-docs/README.md` | 移除 | CONSTITUTION §151 说的是项目根 README，不是 B1-docs 下的。零消费者。 |
| `B1-docs/INDEX.md` | 移除 | 唯一的消费者 `pre_brainstorm_patrol_seed_snapshot_for_project` 零调用者。`pre-brainstorms/` 空目录。架构已迁移。 |
| `B1-docs/CONVERGENCE.md` | 移除 | CONSTITUTION §79 临时兜底。实际上从未被写入。cleanup 已有 wt-close + milestones。 |

## Brainstorm
### Option A: 只精简 doc gate（推荐）
移除 3 个非 agent 注入文件的检查，保留核心 4 个。
- 改动：`freely:check_doc_gate_or_fail` 删除 3 行
- 影响：daemon 可正常启动
- 风险：零

### Option B: 精简 gate + 清理死代码
在 A 基础上追加：
- 删除 `pre_brainstorm_patrol_seed_snapshot_for_project` 死代码
- 清理 `docs/pre-brainstorms/` 空目录引用
- 更新 CONSTITUTION §79 CONVERGENCE 措辞

### Option C: 创建缺失文件
创建 README.md/INDEX.md/CONVERGENCE.md 占位文件。
- 缺点：不解决架构混淆问题，死代码继续存在

## Decision: Option A
3 个文件不是 agent 注入文档，不应阻塞 daemon 启动。只需从 gate 移除检查。死代码清理作为后续独立 issue。

## Candidate
- candidate_id: C-20260709T142056Z-A
- status: promoted
- milestone: M-20260709T142056Z-A
