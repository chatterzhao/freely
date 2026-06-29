---
name: freely-doc-B1_IBM-execution
description: >-
  IBM Framework 第一阶段。消费 raw issue 做 Brainstorm 发散收敛，
  产出 candidate 进入 milestone 规划队列。candidate promote 时通过
  `promoted_issue_id` 提供 I-* issue 的基础信息（key）。B2_IBM
  根据此 key 确定 epic/story、在 milestones.md committed_issues
  生成正式条目（含真实路径）并物化完整文档。
  标准产物：brainstorms.md + candidates.md + milestones.md candidate_issues。

  Use when: `freely wt-create` 命令建好工位之后，需要对 raw issue
  做根因分析、方案评估、scope 判定的预研阶段。触发词："B1"、"预研"、
  "brainstorm"、"candidate"、"分析这个 issue"、"评估方案"。
---

# skill:freely-doc-B1_IBM-execution

> 全链路: [cmd] freely feedback → [skill] freely-workflow-guarded-execution → [cmd] freely wt-create → [skill][here] freely-doc-B1_IBM-execution → [skill] freely-doc-B2_IBM-execution → [skill] freely-test-RED-execution → [skill] freely-dev-loop-execution → [skill] freely-test-execution → [cmd] freely pr-create-guarded → [cmd] freely pr-review-guarded → [cmd] freely pr-merge-guarded → [cmd] freely wt-close

## I→B→M 骨架

B1_IBM 是 IBM Framework 第一阶段。I（Input）由 `freely wt-create` 命令准备，`freely-doc-B1_IBM-execution` skill 做 B（Brainstorm）和 M（Milestone）。

| 阶段 | 含义 | 谁准备 | 产物 |
|------|------|--------|------|
| **I** | Input | `freely wt-create` 命令（已物化到工位） | `docs/issues/raw-{key}/issue.md` |
| **B** | Brainstorm | `freely-doc-B1_IBM-execution` skill | `docs/pre-brainstorms/{key}--{slug}/brainstorms.md`：发散→收敛→决策 |
| **M** | Milestone | `freely-doc-B1_IBM-execution` skill | `docs/pre-brainstorms/{key}--{slug}/candidates.md`（candidate 文档）+ milestones.md candidate_issues（candidate 的 `promoted_issue_id` 指定 I-* issue 的身份标识） |

> Candidate promote 时，`promoted_issue_id` 字段确定 I-* issue 的 key。值是 `I-{key}-{suffix}`（如 `I-20260508T011858Z-A`），suffix 继承 candidate 的 suffix。`freely-doc-B2_IBM-execution` skill 根据此 key，自行确定 epic/story 后构造完整路径（`docs/epics/{epic-name}/{story-name}/raw-{raw-key}/issues/I-{raw-key}-{suffix}.md`）并物化文件。B1_IBM 不决定文件放在哪个 epic/story——那是 B2_IBM 的架构决策。

### I：Input — `freely wt-create` 命令准备的 raw issue

`freely wt-create` 命令从两个来源拉取 raw issue 并物化到工位：
- Source 1：`freely.db` chats 表（`chat_type=new-issue, consumed=0`）
- Source 2：平台 API GitHub/Gitee（OPEN issues 含 `raw-{key}`）

**关键**：Source 1 来的 raw issue 还没有 `platform_ids`（尚未 push 到平台）。`freely-doc-B1_IBM-execution` skill 不关心来源，只消费 `docs/issues/raw-{key}/issue.md`。

`freely-doc-B1_IBM-execution` skill 不创建 raw issue。

### B：Brainstorm — 发散→收敛→决策

0. 审视 issue 价值与时效性：确认该 raw issue 仍值得投入。检查其提出时间、是否已被其他 issue/candidate 覆盖、当前项目阶段是否仍相关。若认为已过时或价值不足，写入 brainstorms.md 的 discovery 部分说明理由并标记 dropped，直接终止 B1_IBM 流程。
1. 读取 `docs/issues/raw-{key}/issue.md`（Input）
2. 读取边界文档：CONSTITUTION.md、LAWS.md、PROJECT_INTENT.md
3. 读取依赖：已有 milestones.md、相关 epics
4. 发散→收敛→决策，产出 `docs/pre-brainstorms/{key}--{slug}/brainstorms.md`

### M：Milestone — 创建 milestone 节点（M-{key}-A），candidate 入队，决定 I-* 身份标识

1. 从 brainstorms.md 收敛结论产出 `candidates.md`（candidate 文档）。candidate 的 ID 命名规则：`C-{key}-{suffix}`，suffix 从 A 开始递增（C-{key}-A、C-{key}-B...）。**一个 raw issue 通常只有一个 candidate（C-{key}-A）；raw issue scope 过大时拆成多个 candidate。**
2. 在 `docs/milestones.md` 中创建 `## M-{key}-A` milestone 节点，将 candidate 写入 `candidate_issues` 队列。Milestone ID 与第一个 candidate 对齐（M-{key}-A）。
3. Candidate 的 `promoted_issue_id` 字段**决定 I-* issue 的身份标识**。值是 I-* 的 key（如 `I-20260629T095905Z-A`），suffix 继承 candidate 的 suffix（C-{key}-A → I-{key}-A，C-{key}-B → I-{key}-B）。`freely-doc-B2_IBM-execution` skill 根据此 ID 确定 epic/story 后构造完整路径并物化文件。
4. Candidate 路径：`proposed → needs_research → blocked → promoted / absorbed / dropped`
5. 状态变为 promoted 后，handoff 给 `freely-doc-B2_IBM-execution` skill

**candidates.md 示例**（promoted 状态）：

```markdown
# Candidates

## C-20260508T011858Z-A: skill 引导与门禁对齐

- candidate_format_version: v2
- title: 审查 skill 引导与门禁标准的差距
- status: promoted
- decision_reason: #247/#251 开发中反复被门禁拦截，根因是 skill 引导缺失
- next_action: 修改 doc-B1/doc-B2/dev-loop skill → 合并
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - doc-B1: candidate 格式示例完整可用
  - doc-B2: I-* issue 示例覆盖全部必需字段
  - dev-loop: pre-tests 结构和产物要求清晰
- promotion_gate: 三个 skill 修改完成且语法无误
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 审查 #247/#251 门禁拦截历史，确认 skill 修改方向正确
  - verdict: pass
- promoted_issue_id: I-20260508T011858Z-A
- milestone: M-20260508T011858Z-A
- session_refs: []
```

> `promoted_issue_id` 的值是 I-* issue 的 key（如 `I-20260508T011858Z-A`），不含路径。`freely-doc-B2_IBM-execution` skill 根据此 key 确定 epic/story 后构造完整路径并物化文件。

**milestones.md 对应条目**：

```markdown
## M-20260508T011858Z-A
- title: skill gate alignment
- status: active
### candidate_issues
1. `C-20260508T011858Z-A`
- milestone: M-20260508T011858Z-A
- status: promoted
- promoted_issue_id: `I-20260508T011858Z-A`
```

注意 `milestone` 使用 `M-{key}-A` 格式，与 candidate 的 key 一致。candidates.md 和 milestones.md 中的 milestone 名称必须一致。

### 完成自检

- [ ] `brainstorms.md` 包含 discovery、research、decision
- [ ] `candidates.md` 每个 candidate 有 status/milestone/decision
- [ ] milestones.md candidate_issues 条目已更新
- [ ] 下一跳明确：继续 B1_IBM 还是进入 `freely-doc-B2_IBM-execution`

## 不负责

- 不创建 raw issue（wt-create 负责）
- 不产出 B2_IBM 产物（prd.md、pre-tests.md、tasks.md、code-review）

## 门禁常见坑速查

> 若 gate 报错，先在此表查找匹配项。更多细节见下方规范模板。

| gate 报错关键词 | 原因 | 正确格式 | 示例 |
|-----------|------|---------|------|
| no valid source_candidate / missing a valid source_candidate | source_candidate 需完整文件路径，不能只写 ID | docs/pre-brainstorms/{key}--{slug}/candidates.md#C-xxx | `docs/pre-brainstorms/20260508T011858Z--skill-gate-alignment/candidates.md#C-20260508T011858Z-A` |
| contains no recognizable candidate heading | candidates.md heading 需 ## 或 ### 开头 | `## C-xxx` | `## C-20260508T011858Z-A: 标题` |
| phase_state is invalid for B1 | raw issue phase_state 合法值 | proposed / absorbed / dropped | `phase_state: absorbed` |
| no absorbed_into field | phase_state=absorbed 时必须写吸收目标 | I-* issue ID | `absorbed_into: I-20260508T011858Z-A` |
| milestone binding missing / unassigned | active candidates(promoted/blocked等)需绑 milestone | M-{key} 并放入 milestones.md candidate_issues | `milestone: M-20260508T011858Z-A` |
| branch does not contain a valid issue key | 分支名需含 raw-YYYYMMDDTHHMMZ 或 I-* key | `feature/raw-{timestamp}-{slug}` | `feature/raw-20260508T011858Z-skill-gate-alignment` |
| next_action is missing / revisit_trigger is missing | pre-IBM 状态(proposed/needs_research/blocked)需写明 | next_action 和 revisit_trigger 字段 | `next_action: 修改 B1 skill → 合并` |

## 规范文档示例(copy-paste可用)

### candidates.md

```markdown
---
candidate_id: C-20260508T011858Z-A
status: promoted
source_raw: raw-20260508T011858Z
created_at: 2026-05-08
milestone: M-20260508T011858Z-A
---

## C-20260508T011858Z-A: 标题

- candidate_format_version: v2
- title: 简短标题
- status: promoted
- decision_reason: 为什么选这个方案
- next_action: 下一步做什么
- revisit_trigger: 什么条件下重新审视
- acceptance_criteria:
  - 验收条件1
  - 验收条件2
- promotion_gate: 晋级条件
- open_questions: []
- acceptance_reviews:
  - reviewer: reviewer-name
  - mode: plan-subagent
  - summary: 评审摘要
  - verdict: pass
- promoted_issue_id: I-20260508T011858Z-A
- milestone: M-20260508T011858Z-A
- session_refs: []
```

### brainstorms.md

```markdown
---
b1_id: B1-20260508T011858Z
phase_state: completed
source_raw: raw-20260508T011858Z
source_url: https://github.com/owner/repo/issues/123
produced_candidate: C-20260508T011858Z-A
created_at: 2026-05-08
---

# B1_IBM: 标题

## Input
- 来源信息

## Problem
- 问题描述

## Brainstorm
### Option A: 方案A
### Option B: 方案B

## Decision: Option X
- 理由

## Candidate
- candidate_id: C-20260508T011858Z-A
- status: promoted
- milestone: M-20260508T011858Z-A
```
- 不实现代码或测试

## 工作流

1. 确认 Input：工位 `docs/issues/raw-{key}/issue.md` 存在
2. 读取 [entry-and-worktree-checks.md](references/entry-and-worktree-checks.md)
3. 首次进入：按 [candidate-recording.md](references/candidate-recording.md) + [milestone-placement.md](references/milestone-placement.md) 写 brainstorms.md、candidates.md、milestones.md
4. 继续研究：沿用同一 reference 补边界、依赖、next_action、revisit_trigger
5. Candidate 准备 promotion 时做 acceptance review
6. 边界稳定且 promotion gate 满足后，按 [promotion-handoff.md](references/promotion-handoff.md) 交给 `freely-doc-B2_IBM-execution`

## 回流输出

- `status` / `why` / `updated_artifacts` / `next_recommended_route`
- `recovery_context` / `execution_base` / `integration_target` / `depends_on`
