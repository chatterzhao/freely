---
name: freely-doc-B2_IBM-execution
description: B2_IBM：I→B→M 第二阶段。从 scan、A2A task 与 continuity evidence 选出的 milestone committed_issues 取 I-{key}，经 Brainstorm 实现设计，产出 Map（prd/pre-tests/tasks/code-review）交付 dev-loop。
---

# skill:freely-doc-B2_IBM-execution

> 全链路: feedback → wt-create → B1_IBM → B2_IBM → dev → pr-create-guarded → pr-review-guarded → pr-merge-guarded → wt-close
>                                               [本 skill 自此开始 — 实现设计 → Map 交付 dev-loop]

## I→B→M 骨架

B2_IBM 是 IBM Framework 第二阶段。I（Input）从 scan、A2A task 与 continuity evidence 选出的里程碑已提交 issue 来，B2_IBM 做 B（Brainstorm）和 M（Map）。

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
| `pre-tests.md` | 结构化测试计划（含 test_command + expected_output），模板见下方 |
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
channel: freely-feature-execution
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

### pre-tests.md 完整模板

B2_IBM 阶段直接写入以下格式。AI 按模板填写，无需查看任何其他文件。模板已满足 LAWS.md §4c 全部要求。

> ⚠️ **反糊弄铁律**
>
> pre-tests.md 不是给门禁看的，是给测试执行者看的。
> 每条 acceptance item 必须是**真实的测试用例**，能切实验证改动是否正确。
>
> - 如果不知道该测什么：重新读 raw issue 理解改动范围，从改动面推导测试面
> - 如果改动不影响某层：写 `not_applicable` 且 **必须写明具体理由**（不是"不适用"三个字敷衍）
> - 禁止：无理由全部 not_applicable + mock
> - 禁止：status 写 pass 但 actual_output 为空（那是 ghost pass，会被 pretests-retirement-gate 硬拦截）
> - 每一条 test_command 必须是真正可执行的测试用例（单元测试、集成测试、端到端测试、API 调用、编译验证、shell 脚本等均可），expected_output 必须具体可验证
>
> **端到端测试和集成测试是 AI 编程中防止项目失败的最重要保证。**
>
> - 如果改动涉及多模块协作、数据流、状态变更 → 必须设计集成测试
> - 如果改动影响用户可见行为、UI 交互、完整业务流程 → 必须设计端到端测试
> - 不要只写单元测试了事——AI 生成的代码最容易在模块边界和端到端流程中出错
> - 选择测试层级的原则：能用端到端兜底就用端到端，需要集成测试兜底就必须用集成测试
>
> **糊弄 pre-tests.md 是导致项目失败的严重失职行为。绝对不允许糊弄测试相关的任何环节。**

```markdown
# Pre-Tests: <功能名>
- issue_id: I-{key}-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: <验收条件简述>
- acceptance_target: <raw issue 验收标准>
- testing_layer: unit | integration | end-to-end
- target_environment: test-pre-merge-{key}-{slug}
- required_evidence: <测试通过的证据要求>
- evidence_level: mock | integration | real_env | post_merge_dogfood
- artifact_ref: <指向测试产物文件，如 docs/epics/{epic}/test-evidence/acceptance-1.log>
- test_command: <实际执行的 shell 命令，如：./bin/test-lane feature-local -- echo ok>
- expected_output: <命令的预期输出，如：所有测试 PASSED，无 FAIL>
- actual_output: (由 skill:freely-test-execution 执行后填写)
- evidence_file: (执行后填写，指向 staged 证据文件)
- blocker: (失败时填写) definition_missing | commands_only | evidence_plan_missing | execution_pending_or_failed
- status: pending | passed | failed | not_applicable
> passed 状态需要 worker execution state（.freely/run/workcell-state.env）。无 worker state 时 passed 会被判 execution_missing，请改用 not_applicable。
- not_applicable_reason: (not_applicable 时必填) change_not_touching_this_layer | no_executable_boundary_at_this_layer | protected_environment_only | human_observation_only | covered_by_more_realistic_required_surface
- not_applicable_explanation: (not_applicable 时必填) <具体原因>
- replacement_evidence: (not_applicable 时必填) <替代验证方式或证据>

### acceptance-2
- id: AT-002
- requirement: <验收条件简述>
- acceptance_target: <验收标准2>
- testing_layer: end-to-end
- target_environment: test-pre-merge-{key}-{slug}
- required_evidence: <证据要求>
- evidence_level: integration
- artifact_ref: <证据文件路径>
- test_command: <shell 命令>
- expected_output: <预期输出>
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: pending

## Unit
- acceptance_target: <单元测试覆盖目标>
- testing_layer: unit
- target_environment: <feature worktree>
- required_evidence: <判定标准>
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: (如不适用填写) no_executable_boundary_at_this_layer
- not_applicable_explanation: (如不适用填写) <原因和替代验证>
- replacement_evidence: (如不适用填写) <替代验证方式>

## Integration
- acceptance_target: <集成测试覆盖目标>
- testing_layer: integration
- target_environment: test-pre-merge-{key}-{slug}
- required_evidence: <判定标准>
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: <端到端验证目标>
- testing_layer: end-to-end
- target_environment: test-pre-merge-{key}-{slug} → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass | fail | not_tested
- real_environment_reason: <真实环境验证结果>
```

**status 取值**: `pending`（未执行）、`passed`（通过）、`failed`（失败）。

**blocker 取值**: `definition_missing`（验收标准缺失）、`commands_only`（只有命令无预期输出）、`evidence_plan_missing`（无证据计划）、`execution_pending_or_failed`（未执行或失败）。

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

## 门禁常见坑速查

> 若 gate 报错，先在此表查找匹配项。更多细节见下方规范模板。

| gate 报错关键词 | 原因 | 正确格式 |
|-----------|------|---------|
| verification_artifact_dir too broad or non-canonical | 需以 /code-reviews 结尾，至少4段路径 | `docs/epics/{epic-name}/{story-name}/code-reviews` |
| implementation decision note is incomplete | 需 5 个字段 | `decision` / `why_this` / `alternatives_considered` / `boundary_non_goals` / `residual_risk` |
| owner issue 'missing' / that issue cannot be resolved | review/code-review 文件需 bullet 格式的 issue_id | `- issue_id: I-20260508T011858Z-A` |
| I-* canonical fields silently cleared | I-* frontmatter 用了 `---` YAML 包裹格式；canonical reader 只解析 bullet | 去掉 `---` 包裹，用 bullet 格式：`- phase_state: completed` |
| phase_state cannot own capability/implementation changes | 实现变更的 I-* 需 completed | `phase_state: completed` |
| pre_tests_path 验证失败 | I-* issue 需声明 pre_tests_path | `pre_tests_path: docs/epics/{epic}/verification/pre-tests.md` |
| section missing acceptance_target/testing_layer | 字段名必须用下划线，不是空格 | `- acceptance_target:` / `- testing_layer:` / `- target_environment:` / `- required_evidence:` |
| acceptance item missing id/requirement/evidence_level/artifact_ref | 每个 acceptance item 必须有这 4 个字段 | `- id: AT-001` / `- requirement: ...` / `- evidence_level: mock` / `- artifact_ref: <path>` |
| execution_missing: got passed | passed 需要 worker state（.freely/run/workcell-state.env），无则改用 not_applicable | `- status: not_applicable` + not_applicable_reason + replacement_evidence |
| not_applicable missing replacement_evidence | not_applicable 的 item 必须写 replacement_evidence | `- replacement_evidence: <替代验证方式>` |
| section marked not applicable but missing replacement_evidence | section 级别 not_applicable 也要写 replacement_evidence | 同上 |
| 全部 not_applicable 被判 "疑似糊弄" | 需至少 1 个 status=passed，或改为 mock | acceptance-1 用 `- evidence_level: mock` + `- status: not_applicable` |
| not_applicable_reason 不支持 | 合法值仅 5 个 | `change_not_touching_this_layer` / `no_executable_boundary_at_this_layer` / `protected_environment_only` / `human_observation_only` / `covered_by_more_realistic_required_surface` |
| section missing blocker_taxonomy | Unit/Integration/End-to-End 必须声明 blocker_taxonomy | `- blocker_taxonomy: execution_pending_or_failed` |

## 规范文档示例(copy-paste可用)

### I-* issue.md（完整模板）

```markdown
<!-- I-* frontmatter 使用 bullet 格式（- key: value），不用 YAML --- 包裹。
     canonical reader (cgrab) 解析 bullet 和 YAML 均可，但 bullet 是推荐格式。 -->
- issue_id: I-20260508T011858Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260508T011858Z-A
- source_candidate: docs/pre-brainstorms/20260508T011858Z--skill-gate-alignment/candidates.md#C-20260508T011858Z-A
- verification_artifact_dir: docs/epics/skill-gate-alignment/code-reviews
- canonical_issue_path: docs/issues/I-20260508T011858Z-A/issue.md
- title: 简短描述

# I-20260508T011858Z-A: 标题

- source_candidate: docs/pre-brainstorms/20260508T011858Z--skill-gate-alignment/candidates.md#C-20260508T011858Z-A
- verification_artifact_dir: docs/epics/skill-gate-alignment/code-reviews
```

### Implementation Decision Note（完整模板）

```markdown
---
issue_id: I-20260508T011858Z-A
issue_path: docs/issues/I-20260508T011858Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260508T011858Z-A
- issue_path: docs/issues/I-20260508T011858Z-A/issue.md

## Implementation Decision Note

- decision: 做了什么
- why_this: 为什么选这个方案
- alternatives_considered: 考虑过哪些替代方案
- boundary_non_goals: 明确不做的事
- residual_risk: 残余风险
```

### pr-review 文件（code-review 模板）

```markdown
# PR Review: #1234
- pr_number: 1234
- branch: feature/raw-xxx-slug
- base: develop
- reviewer: cli
- verdict: pass
- issue_id: I-20260508T011858Z-A
- issue_path: docs/issues/I-20260508T011858Z-A/issue.md

## 1. Worktree Check
- status: pass

## 2. IBM Completeness
- status: pass

## 3. Code Review Evidence
- status: pass

## 4. Pre-test Evidence
- status: pass

## 5. Receipt Integrity
- status: n/a

## 6. Phase State
- status: pass

## Overall Verdict
- verdict: pass
```

## 工作流

1. 确认 Input：milestone committed_issues 中的 I-{key} 存在
2. 读取 [issue-materialization-checklist.md](references/issue-materialization-checklist.md)
3. Materialize I-* issue 到 `docs/epics/{epic}/{story}/issues/`
4. 写 prd.md、pre-tests.md、tasks.md
5. 写 code-review（含 Implementation Decision Note）
6. 更新 milestones.md committed_issues
7. 若发现边界外新问题：返回 `next_recommended_route=freely-doc-B1_IBM-execution`
8. B2_IBM 完成后，进入 dev-loop 实现 → pr-create-guarded（提 PR）→ pr-merge-guarded（门禁合并）→ wt-close（收口）
