---
name: freely-doc-B2_IBM-execution
description: B2_IBM：I→B→M 第二阶段。从 scan/handoffs 选出的 milestone committed_issues 取 I-{key}，经 Brainstorm 实现设计，产出 Map（prd/pre-tests/tasks/code-review）交付 dev-loop。
---

# skill:freely-doc-B2_IBM-execution

> 全链路: feedback → wt-create → B1_IBM → B2_IBM → dev → pr-create-guarded → pr-review-guarded → pr-merge-guarded → wt-close
>                                               ↑ you are here（B: 实现设计 → M: Map 交付 dev-loop）

## I→B→M 骨架

B2_IBM 是 IBM Framework 第二阶段。I（Input）从 scan/handoffs 选出的里程碑已提交 issue 来，B2_IBM 做 B（Brainstorm）和 M（Map）。

| 阶段 | 含义 | 谁准备 | 产物 |
|------|------|--------|------|
| **I** | Input | milestone committed_issues | I-{key}（已排期，已有正式 issue 文档） |
| **B** | Brainstorm | B2_IBM skill | 实现前置设计、替代方案评估、验收标准 |
| **M** | Map | B2_IBM skill | prd.md、pre-tests.md（含 Acceptance Items v2 adequacy）、tasks.md、code-reviews/ |

### I：Input — milestone committed_issues

从 `docs/milestones.md` → committed_issues 获取 I-{key}。
I-{key} 由 B1_IBM 阶段 promote 而来，已排期、已有 priority、已有正式 issue 文档。

B2_IBM 不创建 I-{key}。

### B：Brainstorm — 实现前置设计

1. 读取 I-{key} issue 文档（Input）
2. 读取 candidate 的 acceptance_criteria、promotion_gate
3. 读实现面、读验收标准、评估替代方案
4. 产出 `brainstorms/b-{issue-name}.md`

### M：Map — 完整产物目录

产出 `docs/epics/{epic-name}/{story-name}/` 下的完整目录：

| 产物 | 要求 |
|------|------|
| `issues/{name}.md` | I-* issue 文档，完整格式见下方示例 |
| `prd.md` | Goal → Dev-Loop Handoff |
| `pre-tests.md` | 结构见 `skill:freely-dev-loop-execution` 情景 D |
| `tasks.md` | 任务分解，关联 owner issue |
| `code-reviews/` | Implementation Decision Note（decision/why_this/alternatives_considered/boundary_non_goals/residual_risk） |

**I-* issue 完整示例**（`docs/issues/I-{key}-A/issue.md`）：

```markdown
---
local_id: I-20260508T011858Z-A
kind: linked
status: in_dev
phase_state: in_dev
promoted_from: raw-20260508T011858Z
source_candidate: docs/pre-brainstorms/20260508T011858Z--skill-gate-alignment/candidates.md
canonical_issue_path: ""
platform_ids: {}
primary_platform: ""
last_synced_comment_at: {}
hash: ""
created_at: 2026-05-08T01:18:58Z
updated_at: 2026-05-08T01:18:58Z
intake_id: ""
author: zhaoquan
channel: freely-feat-execution
session_refs: []
pre_tests_path: docs/epics/skill-gate-alignment/verification/pre-tests.md
verification_artifact_dir: docs/epics/skill-gate-alignment/code-reviews
---

# I-20260508T011858Z-A: skill 引导与门禁对齐

- source_candidate: `docs/pre-brainstorms/20260508T011858Z--skill-gate-alignment/candidates.md`
- pre_tests_path: `docs/epics/skill-gate-alignment/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/skill-gate-alignment/code-reviews`

## 实现
...
```

注意 `canonical_issue_path` 为空避免自引用；YAML frontmatter 和正文 bullet 字段都需要写关键字段。

### 完成自检

- [ ] I-{key} issue `phase_state = done_b2_ibm`
- [ ] pre-tests.md `## Acceptance Items` 含 v2 adequacy 字段
- [ ] tasks.md 存在且任务已分解
- [ ] code-reviews/ 含 Implementation Decision Note
- [ ] milestones.md committed_issues 条目已更新
- [ ] 下一跳明确：进入 `skill:freely-dev-loop-execution`

phase_state 流转：`in_b2_ibm → done_b2_ibm → in_dev`

## 不负责

- 不创建 I-{key}（B1_IBM 阶段 promote 产生）
- 不实现代码或运行测试（dev-loop 负责）
- 不直接写 progress（dev-loop 负责）

## 工作流

1. 确认 Input：milestone committed_issues 中的 I-{key} 存在
2. 读取 [issue-materialization-checklist.md](references/issue-materialization-checklist.md)
3. Materialize I-* issue 到 `docs/epics/{epic}/{story}/issues/`
4. 写 prd.md、pre-tests.md、tasks.md
5. 写 code-review（含 Implementation Decision Note）
6. 更新 milestones.md committed_issues
7. 若发现边界外新问题：返回 `next_recommended_route=freely-doc-B1_IBM-execution`
8. B2_IBM 完成后，进入 dev-loop 实现 → pr-create-guarded（提 PR）→ pr-merge-guarded（门禁合并）→ wt-close（收口）
