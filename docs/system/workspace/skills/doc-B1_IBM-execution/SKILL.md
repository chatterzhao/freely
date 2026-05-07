---
name: doc-B1_IBM-execution
description: B1_IBM：I→B→M 第一阶段。消费 wt-create 准备的 raw issue，经 Brainstorm 发散收敛产出 candidate，进入 Milestone 候选队列。
---

# skill:doc-B1_IBM-execution

## I→B→M 骨架

B1_IBM 是 IBM Framework 第一阶段。I（Input）由 wt-create 准备，B1_IBM 做 B（Brainstorm）和 M（Milestone）。

| 阶段 | 含义 | 谁准备 | 产物 |
|------|------|--------|------|
| **I** | Input | wt-create（已物化到工位） | `docs/issues/raw-{key}/issue.md` |
| **B** | Brainstorm | B1_IBM skill | `brainstorms.md`：发散→收敛→决策 |
| **M** | Milestone | B1_IBM skill | `candidates.md` + milestones.md candidate_issues |

### I：Input — wt-create 准备的 raw issue

wt-create 从两个来源拉取 raw issue 并物化到工位：
- Source 1：`freely.db` chats 表（`chat_type=new-issue, consumed=0`）
- Source 2：平台 API GitHub/Gitee（OPEN issues 含 `raw-{key}`）

**关键**：Source 1 来的 raw issue 还没有 `platform_ids`（尚未 push 到平台）。B1_IBM 不关心来源，只消费 `docs/issues/raw-{key}/issue.md`。

B1_IBM 不创建 raw issue。wt-create 已经准备好了。

### B：Brainstorm — 发散→收敛→决策

1. 读取 `docs/issues/raw-{key}/issue.md`（Input）
2. 读取边界文档：CONSTITUTION.md、LAWS.md、PROJECT_INTENT.md
3. 读取依赖：已有 milestones.md、相关 epics
4. 发散→收敛→决策，产出 `docs/pre-brainstorms/{key}--{slug}/brainstorms.md`

### M：Milestone — candidate + 队列

1. 从 brainstorms.md 收敛结论产出 `candidates.md`
2. 每个 candidate 标注：status、milestone、promoted_issue_path、decision
3. 更新 `docs/milestones.md` → candidate_issues 队列
4. Candidate status：`proposed → needs_research → blocked → promoted / absorbed / dropped`

### 完成自检

- [ ] `brainstorms.md` 包含 discovery、research、decision
- [ ] `candidates.md` 每个 candidate 有 status/milestone/decision
- [ ] milestones.md candidate_issues 条目已更新
- [ ] 下一跳明确：继续 B1_IBM 还是进入 `doc-B2_IBM-execution`

## 不负责

- 不创建 raw issue（wt-create 负责）
- 不产出 B2_IBM 产物（prd.md、pre-tests.md、tasks.md、code-review）
- 不实现代码或测试

## 工作流

1. 确认 Input：工位 `docs/issues/raw-{key}/issue.md` 存在
2. 读取 [entry-and-worktree-checks.md](references/entry-and-worktree-checks.md)
3. 首次进入：按 [candidate-recording.md](references/candidate-recording.md) + [milestone-placement.md](references/milestone-placement.md) 写 brainstorms.md、candidates.md、milestones.md
4. 继续研究：沿用同一 reference 补边界、依赖、next_action、revisit_trigger
5. Candidate 准备 promotion 时做 acceptance review
6. 边界稳定且 promotion gate 满足后，按 [promotion-handoff.md](references/promotion-handoff.md) 交给 `doc-B2_IBM-execution`

## 回流输出

- `status` / `why` / `updated_artifacts` / `next_recommended_route`
- `recovery_context` / `execution_base` / `integration_target` / `depends_on`
