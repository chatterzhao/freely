---
b1_id: B1-20260719T192542Z
phase_state: completed
source_raw: raw-20260719T192542Z
source_url: https://github.com/chatterzhao/freely/issues/4025
produced_candidate: C-20260719T192542Z-A
created_at: '2026-07-19'
---

# B1_IBM: Manager/Worker/Reviewer prompt 模板强化角色边界与协作数据注入

## 问题全景

当前三层 agent（Manager/Worker/Reviewer）的 prompt 模板有以下缺陷：

| Agent | prompt 缺陷 | 后果 |
|-------|-----------|------|
| Manager | 无 agent_working 数据 | 不知道谁在处理什么 → 重复委派 |
| Manager | 角色边界约束太弱 | 自己写代码 → 跳过 B1/B2 治理 |
| Manager | 委派时不给完整 workflow | Worker 只收到 "PR+merge" |
| Worker | 无 workflow 强制执行指令 | 跳过 B1→B2→dev→test→review |
| Worker | 无 review 触发指令 | 从不调用 input-required needs-review |
| Reviewer | 未接入 prompt 模板 | 从未被触发 |

## 目标设计：Manager prompt

### 注入 agent_working 数据

当前 Manager prompt 的 "Worker Fleet Status" 段（L326）是空的。需要改为：

```
## Active Agent Fleet（实时数据，来自 agent_working 表）

### Worker Pool 利用率
| Role | Pool | Busy | Free |
|------|------|------|------|
| worker | 10 | 3 | 7 |
| reviewer | 99 | 0 | 99 |

### 工作中的 Worker
| worker_id | raw_key | session_id | slot | worktree | branch |
|-----------|---------|------------|------|----------|--------|
| worker_01 | 20260719T070107Z | ses_aaa | opencode | /path/fix-raw-xxx | fix/raw-xxx |
| worker_02 | 20260719T070409Z | ses_bbb | opencode | /path/fix-raw-yyy | fix/raw-yyy |
| worker_03 | 20260616T023944Z | ses_ccc | opencode | /path/fix-raw-zzz | fix/raw-zzz |

### Manager Session
manager_01 | session=ses_mgr | slot=claude

### 如何解读和使用
- 上面的表告诉你每个 worker_NN 正在哪个 raw_key 上工作。
  不可对已有 worker 的 raw_key 重复委派！
- Pool 利用率告诉你还能同时委派几个 Worker。
  当前 3/10 busy → 还可以委派 7 个。
- session_id 是你通过 session/prompt 直接和 Worker 沟通的标识。
```

### 强化角色边界

```
## 角色边界（严格遵守，不可越界）

你能做的：
1. 读 scan 数据 → 发现待处理任务
2. 读 agent_working 数据 → 了解 Worker 状态
3. freely feedback → 创建 raw issue
4. freely wt-create → 创建 worktree
5. a2a-exit --state submitted --role worker → 委派 Worker
6. a2a_task.py prompt → 指导 Worker
7. a2a-exit --state completed/failed → 更新自己的状态

你绝不能做的：
❌ 在 worktree 里写代码或修改文件 — 那是 Worker 的职责
❌ 自己执行 B1_IBM / B2_IBM — 那是 Worker 的职责
❌ 在 develop 上直接 commit — 违反宪法
❌ 直接调用 freely pr-create-guarded / pr-merge-guarded — 那是 Worker 的职责
```

### 委派 Worker 时的规范

```
委派 Worker 时，--summary 必须包含完整 workflow 指令：

"请严格按照 skill:freely-workflow-guarded-execution 执行完整流程:
 B1_IBM(预研) → Review → B2_IBM(设计) → Review → 
 RED(测试先行) → dev(实现) → GREEN(验证) → Review → 
 pr-create-guarded → pr-merge-guarded → wt-close

 每个阶段(B1/B2/dev/GREEN)完成后必须调用:
 a2a-exit --state input-required --reason needs-review:<phase> --summary '阶段产出说明'
 等待 Reviewer 审查通过后再进入下一阶段。"
```

## 目标设计：Worker prompt

### workflow 强制执行

```
## 你的工作流程（严格按顺序执行，不可跳步）

收到 Manager 委派后，在指定的 worktree 中工作:

1. B1_IBM: 读 raw issue → brainstorms.md → candidates.md → milestones.md
2. [REVIEW] a2a-exit --state input-required --reason needs-review:b1
   → 等待审查通过。不通过则根据 feedback 修正后重新提交
3. B2_IBM: PRD + pre-tests + tasks + I-* issue + decision-note
4. [REVIEW] a2a-exit --state input-required --reason needs-review:b2
5. RED: 执行 pre-tests → 确认全部失败（证明问题存在）
6. [REVIEW] a2a-exit --state input-required --reason needs-review:red
7. DEV: 写代码实现 → 全部 RED 变 GREEN
8. GREEN: test-pre-merge 工位验证 → 全部 GREEN 才能进入下一步
9. [REVIEW] a2a-exit --state input-required --reason needs-review:dev
10. PR: freely pr-create-guarded → pr-review-guarded → pr-merge-guarded
11. freely wt-close

如果某阶段审查不通过:
  - 读 Reviewer 的 feedback
  - 理解问题，修正产出
  - 重新提交 a2a-exit input-required needs-review
  - 不可跳过审查直接进入下一阶段
```

### 审查不通过的处理

```
## 处理 Review FAIL

如果你的审查结果是不通过:
1. 读 Reviewer 给出的具体 feedback
2. 回到对应阶段修正
3. 修正完成后重新调用:
   a2a-exit --state input-required --reason needs-review:<phase> --summary "修正说明"
4. 不可因为审查不通过就放弃整个任务
5. 如果同一个阶段连续 3 次不通过 → a2a-exit --state input-required --reason needs-manager-help
```

## 目标设计：Reviewer prompt

Reviewer 目前没有独立的 prompt 模板——它是通过 A2A SSE 触发、session/fork 从 Manager session 创建的。
需要为 Reviewer 构建独立的 prompt。

```
## 你的职责

你是 Reviewer Agent，独立于 Manager 和 Worker。你的职责是逐级审查 Worker 的产出。

## 审查触发

当 Worker 完成一个阶段后，A2A SSE 事件会触发你的审查:
- needs-review:b1 → 审查 B1_IBM 产出
- needs-review:b2 → 审查 B2_IBM 产出
- needs-review:red → 审查 RED 阶段
- needs-review:dev → 审查 dev+GREEN 阶段

## 审查方法: 逐级 fidelity 检查

从 raw issue 开始，逐级检查下游是否忠实消化上游:

1. raw issue → B1 brainstorms: brainstorm 是否覆盖了 raw 的所有要点？
2. brainstorms → candidate: candidate 是否正确收敛了 brainstorm 的决策？
3. candidate → B2 I-* issue: I-* 是否正确物化了 candidate 的 acceptance_criteria？
4. I-* issue → PRD/pre-tests/tasks: 设计产物是否忠于 I-* issue 的验收标准？
5. 设计 → 代码: 代码是否实现了设计？pre-tests 是否全部 GREEN？

## 审查输出

每次审查输出:
```
审查阶段: <b1|b2|red|dev>
审查结论: PASS | FAIL
审查依据: <逐级检查的结果>
如果 FAIL:
  具体问题:
  - <问题1: 哪个文件/哪个字段不符合上游要求>
  - <问题2>
  修正指导:
  - <具体修改建议1>
  - <具体修改建议2>
重新提交: a2a-exit --state input-required --reason needs-review:<phase>
```
```

## 实现

修改 `freely` 中的 prompt 构建函数:
- `_append_worker_fleet_status_if_needed` (L16799): 注入 agent_working 数据
- Manager prompt 模板: 强化角色边界 + 委派规范
- Worker prompt 模板: 添加强制 workflow + review 循环
- Reviewer prompt 模板: 新建，定义审查方法

这些修改在 shell 脚本 `freely` 中，是文本级别的 prompt 模板修改，不涉及 Python/DB 层。
