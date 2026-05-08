---
name: doc-B2_IBM-execution
description: B2_IBM：I→B→M 第二阶段。从 milestone committed_issues 取 I-{key}，经 Brainstorm 实现设计，产出 Map（prd/pre-tests/tasks/code-review）交付 dev-loop。
---

# skill:doc-B2_IBM-execution

## I→B→M 骨架

B2_IBM 是 IBM Framework 第二阶段。I（Input）从 milestone committed_issues 来，B2_IBM 做 B（Brainstorm）和 M（Map）。

| 阶段 | 含义 | 谁准备 | 产物 |
|------|------|--------|------|
| **I** | Input | milestone committed_issues | I-{key}（已排期，已有正式 issue 文档） |
| **B** | Brainstorm | B2_IBM skill | 实现前置设计、替代方案评估、验收标准 |
| **M** | Map | B2_IBM skill | prd.md、pre-tests.md（含 Acceptance Items v2 adequacy）、tasks.md、code-reviews/ |

### I：Input — milestone committed_issues

从 `docs/milestones.md` → committed_issues 获取 I-{key}。
I-{key} 由 B1_IBM 阶段 promote 而来，已排期、已有 priority、已有正式 issue 文档。

B2_IBM 不创建 I-{key}。milestone 已经准备好了。

### B：Brainstorm — 实现前置设计

1. 读取 I-{key} issue 文档（Input）
2. 读取 candidate 的 acceptance_criteria、promotion_gate
3. 读实现面、读验收标准、评估替代方案
4. 产出 `brainstorms/b-{issue-name}.md`

### M：Map — 完整产物目录

产出 `docs/epics/{epic-name}/{story-name}/` 下的完整目录：

| 产物 | 要求 |
|------|------|
| `issues/{name}.md` | 正式 I-* issue 文档，含 frontmatter（phase_state、source_candidate、milestone、verification_artifact_dir） |
| `prd.md` | AI-ready 最小结构：Goal → Dev-Loop Handoff |
| `pre-tests.md` | 含 `## Acceptance Items`，每个 item 有 id/requirement/evidence_level/status/artifact_ref。对 `test-pre-merge → develop` guarded promote 的 owner，至少一条 item 含 v2 adequacy 字段：surface_kind、target_lane、promotion_gate（=develop_merge）、task_refs、case_design |
| `tasks.md` | T-00X 任务分解，关联 owner issue |
| `code-reviews/` | 含 Implementation Decision Note（decision/why_this/alternatives_considered/boundary_non_goals/residual_risk） |

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
channel: feat-execution
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

要点：
- YAML frontmatter 和正文 bullet 字段**都需要写**关键字段（`source_candidate`、`pre_tests_path`、`verification_artifact_dir`）
- `canonical_issue_path` 指向该 issue 的 canonical 位置；如果 issue 本身就在 canonical 路径，设为空字符串 `""` 避免自引用
- `phase_state` 初始 `in_dev`，实现完成后更新为 `in_verification`

### 完成自检

- [ ] I-{key} issue `phase_state = done_b2_ibm`
- [ ] pre-tests.md `## Acceptance Items` 含 v2 adequacy 字段
- [ ] tasks.md 存在且任务已分解
- [ ] code-reviews/ 含 Implementation Decision Note
- [ ] milestones.md committed_issues 条目已更新
- [ ] 下一跳明确：进入 `skill:dev-loop-execution`

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
7. 若发现边界外新问题：返回 `next_recommended_route=doc-B1_IBM-execution`
