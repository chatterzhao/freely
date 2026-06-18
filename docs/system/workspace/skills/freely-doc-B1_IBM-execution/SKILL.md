---
name: freely-doc-B1_IBM-execution
description: B1_IBM：I→B→M 第一阶段。消费 scan 结果中 wt-create 准备的 raw issue，经 Brainstorm 发散收敛产出 candidate，进入 milestone 规划队列。
---

# skill:freely-doc-B1_IBM-execution

> 全链路: feedback → wt-create → B1_IBM → B2_IBM → dev → pr-create-guarded → pr-review-guarded → pr-merge-guarded → wt-close
>                                    ↑ you are here（B: Brainstorm → M: Milestone）

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

B1_IBM 不创建 raw issue。

### B：Brainstorm — 发散→收敛→决策

0. 审视 issue 价值与时效性：确认该 raw issue 仍值得投入。检查其提出时间、是否已被其他 issue/candidate 覆盖、当前项目阶段是否仍相关。若认为已过时或价值不足，写入 brainstorms.md 的 discovery 部分说明理由并标记 dropped，直接终止 B1_IBM 流程。
1. 读取 `docs/issues/raw-{key}/issue.md`（Input）
2. 读取边界文档：CONSTITUTION.md、LAWS.md、PROJECT_INTENT.md
3. 读取依赖：已有 milestones.md、相关 epics
4. 发散→收敛→决策，产出 `docs/pre-brainstorms/{key}--{slug}/brainstorms.md`

### M：Milestone — candidate + 队列

1. 从 brainstorms.md 收敛结论产出 `candidates.md`，格式见下方示例
2. 更新 `docs/milestones.md` → candidate_issues 队列
3. Candidate 路径：`proposed → needs_research → blocked → promoted / absorbed / dropped`

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
- promoted_issue_path: docs/issues/I-20260508T011858Z-A/issue.md
- milestone: M-20260508T011858Z-A
- session_refs: []
```

**milestones.md 对应条目**：

```markdown
## M-20260508T011858Z-A
- title: skill gate alignment
- status: active
### candidate_issues
1. `C-20260508T011858Z-A`
- milestone: M-20260508T011858Z-A
- status: promoted
- promoted_issue_path: `docs/issues/I-20260508T011858Z-A/issue.md`
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
