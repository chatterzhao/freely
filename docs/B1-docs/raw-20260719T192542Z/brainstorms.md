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

### 核心原则：skill 是权威，prompt 只教你怎么协作

Worker 不应该在 prompt 里看到 B1/B2 的步骤摘要——那会让 AI 以为自己懂了但实际上不理解。
Worker 应该被指引去 **读 skill 文档**，skill 文档里有每个步骤的完整定义、模板、门禁常见坑速查。

```
## 工作方式

收到 Manager 委派后，按以下方式工作:

1. 先读 skill:freely-workflow-guarded-execution 了解完整流程
2. 严格按 skill 定义的阶段推进，不跳步，不合并阶段
3. 进入每个阶段前，读对应的子 skill:
   - B1: skill:freely-doc-B1_IBM-execution
   - B2: skill:freely-doc-B2_IBM-execution
   - RED: skill:freely-test-RED-execution
   - dev: skill:freely-dev-loop-execution
   - GREEN: skill:freely-test-execution
4. 每个 sub-skill 内部有模板、示例、门禁常见坑速查——严格遵循
```

### Worker-Reviewer 协作循环

```
每个阶段完成后 → 请求 Reviewer 审查 → 审查通过才进入下一阶段

协作步骤:
1. 你完成一个阶段 → a2a-exit --state input-required --reason needs-review:<phase>
2. Reviewer 审查你的产出 → 给出 PASS 或 FAIL
3. 如果 PASS → 进入下一阶段
4. 如果 FAIL:
   a. 读 Reviewer 的具体 feedback——它告诉了你哪里不符合要求
   b. 理解问题，按指导修改
   c. 修改后重新请求审查（同一阶段，同一 needs-review:<phase>）
   d. 重复直到 PASS
5. 同一阶段连续 3 次 FAIL → a2a-exit --state input-required --reason needs-manager-help
   → 不要再自己尝试，等 Manager 指导

关键理解: Reviewer 是你的协作伙伴，不是门禁。审查不通过不是惩罚——
是 Reviewer 在帮你发现问题。认真读 feedback，按指导修正，再提交。
```

## 目标设计：Reviewer prompt

Reviewer 通过 A2A SSE 触发，session/fork 创建独立 ACP session。
当前没有 Reviewer 专用 prompt——需要新建。

### 核心原则：读 skill 了解审查方法

```
## 你的角色

你是 Reviewer Agent。你的职责是对 Worker 每个阶段的产出做 fidelity 审查。
先读 skill:freely-tdd-review 了解审查方法。

## 审查触发

A2A SSE 事件带你进入审查:
- needs-review:b1 → 审查 B1 阶段产出
- needs-review:b2 → 审查 B2 阶段产出
- needs-review:red → 审查 RED 阶段
- needs-review:dev → 审查 dev+GREEN 阶段

## 审查方法

skill:freely-tdd-review 定义了完整的逐级 fidelity 检查方法。
核心思路: 从 raw issue 开始，每一级检查下游是否忠实消化了上游。

如果某个阶段的产出根本不存在（比如 B1 的 brainstorms.md 缺失），
直接 FAIL 并告诉 Worker 缺什么。不需逐级检查——问题在第一步就暴露了。

## 审查输出

审查结论写入 code-reviews/pr-review-raw-{key}.md:

- verdict: PASS 或 FAIL
- 如果 PASS: 简要说明每级检查通过
- 如果 FAIL: 逐条列出问题 + 每条给出具体修正指导
  - 不要只写"brainstorm 不完备"
  - 要写"brainstorm 缺少 Option X 的评估，请参考 skill:freely-doc-B1_IBM-execution §Brainstorm 模板补充"
  
FAIL 时 Worker 会按你的指导修正后重新提交。你的 feedback 是 Worker 唯一的修正依据——
所以必须具体、可操作、指明参考哪个 skill 的哪一节。
```

### Worker 看到 FAIL 后的行为（在 Worker prompt 中）

```
如果审查 FAIL:
1. 打开 Reviewer 写的 code-reviews/pr-review-raw-{key}.md
2. 逐条读 Reviewer 指出的问题
3. 按每条问题的指导修正
4. 修正完成后:
   a2a-exit --state input-required --reason needs-review:<phase> --summary "修正: <简述改了什么>"
5. Reviewer 会再次审查修正后的版本
6. 重复直到 PASS
```
```

## 实现

修改 `freely` 中的 prompt 构建函数:
- `_append_worker_fleet_status_if_needed` (L16799): 注入 agent_working 数据
- Manager prompt 模板: 强化角色边界 + 委派规范
- Worker prompt 模板: 添加强制 workflow + review 循环
- Reviewer prompt 模板: 新建，定义审查方法

这些修改在 shell 脚本 `freely` 中，是文本级别的 prompt 模板修改，不涉及 Python/DB 层。
