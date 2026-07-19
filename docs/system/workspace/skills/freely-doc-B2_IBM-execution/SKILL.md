---
name: freely-doc-B2_IBM-execution
description: >-
  IBM Framework 第二阶段。消费 `freely-doc-B1_IBM-execution` skill 在
  milestones.md candidate_issues 中 promote 的 candidate（通过
  `source_candidate` 找到候选文档，读取 acceptance_criteria 等依据）。
  三步产出：① 根据 `promoted_issue_id` 确定 epic-name/story-name，
  在 milestones.md committed_issues 中生成 I-* issue 正式条目（含真实路径）；
  ② 在 `docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/issues/` 下物化
  完整 I-* issue 文档；③ 产出设计产物 prd.md + pre-tests.md + tasks.md +
  code-reviews/。交付给 `freely-dev-loop-execution` skill。

  Use when: `freely-doc-B1_IBM-execution` skill 完成 candidate promoted
  之后。触发词："B2"、"物化 issue"、"设计"、"pre-tests"、"写测试方案"、
  "PRD"、"分解任务"、"I-* 文档"。
---

# skill `freely-doc-B2_IBM-execution`

> 全链路: [skill] freely-workflow-guarded-execution → [cmd] freely feedback → [cmd] freely wt-create（创建工位后cd到工位进行工作） → [skill] freely-doc-B1_IBM-execution → [skill][here] freely-doc-B2_IBM-execution → [skill] freely-test-RED-execution → [skill] freely-dev-loop-execution → [skill] freely-test-execution → [cmd] freely pr-create-guarded → [cmd] freely pr-review-guarded → [cmd] freely pr-merge-guarded → [cmd] freely wt-close

## I→B→M 骨架

B2_IBM 是 IBM Framework 第二阶段。消费 `freely-doc-B1_IBM-execution` skill promote 的 candidate，做 B（Brainstorm）和 M（Map），**在 milestones.md committed_issues 生成 I-* 正式条目并物化完整文档**，同时产出全部设计产物。

> 四节点链路中，本 skill 负责 milestone → **I-* issue 物化**。M（milestone，M-{raw key}-A）和 candidate 的 `promoted_issue_id`（I-{raw key}-{suffix}）由 B1_IBM 提供。本 skill 据此 key：① 按 [issue-materialization-checklist.md](references/issue-materialization-checklist.md) 规范确定 epic-name/story-name；② 在 milestones.md committed_issues 中生成 I-* 正式条目并**填写 epics 下的真实路径**（`docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/issues/I-{raw key}-{suffix}.md`）；③ 在该路径物化完整 I-* issue 文档。
>
> 关键区分：B1_IBM 产出的是 key（I-{raw key}-{suffix}，在 candidate_issues 中）。B2_IBM 将 key 变成 milestones.md 中的**正式条目（含真实路径）**和 epics 目录下的**完整文档**。

| 阶段 | 含义 | 做什么 | 产物 |
|------|------|------|------|
| **I** | Input | 读 B1 产物：milestones.md → promoted candidate → 获取 `promoted_issue_id`（key+suffix）和 `source_candidate` 路径 | 此时 I-* issue **只有元信息**（key+suffix），还不是文件 |
| **B** | Brainstorm | 对每个 I-* issue 做实现前置研究：读 candidate 的 acceptance_criteria → 评估方案 → 设计 prd/pre-tests/tasks → **生成所有产物文件** | brainstorm 笔记 + I-* issue.md + prd.md + pre-tests.md + tasks.md |
| **M** | Map | 把 B 阶段生成的所有产物放入规范目录，更新 milestones.md committed_issues（I-* 正式条目含真实路径） | 完整的 `raw-{raw key}/` 目录树 |

> **核心理解**: I-* issue 在 Input 阶段只是一个 key（如 `I-20260701T085407Z-A`）——由 B1 candidate 提供，还不是文件。
> **Brainstorm 阶段把它变成真实的 issue.md 文件**，同时产出 prd/pre-tests/tasks。
> 每个 candidate（C-{raw key}-A）→ 一个 I-* issue（I-{raw key}-A）→ 一个 brainstorm（b-I-{raw key}-A）→ 一套设计产物。

### I：Input — 读 B1 产物，获取 I-* issue 元信息

B2 不创建 I-* issue 的 key——key 由 B1 提供。B2 按以下步骤获取：

1. 打开 `docs/milestones.md` → 找到 `candidate_issues` 中 `status=promoted` 的 candidate
2. 读取 candidate 条目，获取：
   - `promoted_issue_id`: I-* issue 的 key（如 `I-20260701T085407Z-A`）→ 包含 `{raw key}` 和 `{suffix}`
   - `source_candidate`: 指向 `docs/B1-docs/raw-{raw key}/candidates.md#C-{raw key}-{suffix}` 的完整路径
3. 根据 `source_candidate` 打开候选文档，读取：
   - `acceptance_criteria` — 验收标准（Brainstorm 必须覆盖）
   - `promotion_gate` — 晋级条件（Brainstorm 必须满足）
   - `decision_reason` — 为什么选这个方案
   - `open_questions` — 待解决问题

**此时 I-* issue 还不是文件**——只有 key 和元信息。Brainstorm 阶段才把它变成真实的 issue.md。

### B：Brainstorm — 对每个 I-* issue 做实现设计，生成全部产物

B 阶段是 B2_IBM 的核心工作。对每个 candidate（即每个 I-* issue），依次完成：

**B1. 研究 + 记录 brainstorm 笔记**

读取 candidate 的 acceptance_criteria、promotion_gate，评估实现方案、替代方案、边界条件。将研究过程写入：

```
docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/brainstorms/b-I-{raw key}-{suffix}.md
```

> `b-I-{raw key}-A.md` 对应 `I-{raw key}-A`。suffix 一一对应。一个 candidate → 一个 I-* issue → 一个 brainstorm。

**B2. 基于 brainstorm 结论，物化 I-* issue**

将 key 变成真实文件——写入包含完整 frontmatter 和正文的 issue 文档：

```
docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/issues/I-{raw key}-{suffix}.md
```

必填字段：`issue_id`、`phase_state`（初始 `in_b2_ibm`）、`source_candidate`、`pre_tests_path`、`verification_artifact_dir`。格式见 [规范文档示例](#规范文档示例copy-paste可用)。

**B3. 产出设计产物**

基于 brainstorm 结论，在同一目录下产出：

| 产物 | 路径 | 内容 |
|------|------|------|
| `prd.md` | `raw-{raw key}/prd.md` | Goal → 实现方案 → Dev-Loop Handoff |
| `pre-tests.md` | `raw-{raw key}/verification/pre-tests.md` | 结构化测试计划（模板见下方） |
| `tasks.md` | `raw-{raw key}/verification/tasks.md` | 任务分解，关联 owner issue |
| IDN | `raw-{raw key}/code-reviews/implementation-decision-note.md` | 5 字段（decision/why_this/alternatives/boundary/residual_risk） |

### M：Map — 确定 epic/story + 写入 milestones + 完整交付

**步骤 0：确定 epic-name 和 story-name**（写任何产物前必须先做）。

`{epic-name}` 是能力域（capability domain），`{story-name}` 是 epic 下的可交付切片。详见 [issue-materialization-checklist.md](references/issue-materialization-checklist.md) §如何确定 epic-name 和 story-name。简单原则：
- 这个 raw issue 解决的能力问题，和已有 epic 的**能力域重叠** → 复用已有 epic
- 能力域**正交**（独立可理解、独立可验收）→ 新建 epic
- 同一 epic 下的新子问题 → 新建 story

**步骤 1：确认规范目录结构**。B 阶段已产出所有文件，M 阶段确认它们都在正确位置。

> **`{raw key}`** = raw issue 的时间戳 key（如 `20260701T085407Z`）。
> **`{suffix}`** = 来自 Input（candidate 的 `promoted_issue_id` 字段，如 `I-{raw key}-A` 中的 `A`）。B2 **不发明** suffix——直接沿用 B1 candidate 提供的值。
> **`{epic-name}`** 和 **`{story-name}`** 由 B2_IBM 的步骤 0 决定（按语义判断能力域和可交付切片）。

### 规范目录结构（B 阶段产出，M 阶段确认）

```
docs/B2-docs/{epic-name}/{story-name}/
└── raw-{raw key}/                           ← 一个 raw issue 一个目录
    │
    ├── prd.md                               ← B 产出：Goal → Dev-Loop Handoff
    │
    ├── brainstorms/                          ← B 产出：每个 I-* 一个研究笔记
    │   ├── b-I-{raw key}-A.md               ← 对应 I-{raw key}-A 的方案研究
    │   └── b-I-{raw key}-B.md               ← 对应 I-{raw key}-B 的方案研究
    │
    ├── issues/                               ← B 产出：物化后的 I-* issue 文件
    │   ├── I-{raw key}-A.md                 ← 物化自 candidate C-{raw key}-A
    │   └── I-{raw key}-B.md                 ← 物化自 candidate C-{raw key}-B
    │
    ├── verification/                         ← B 产出：测试方案 + 任务分解
    │   ├── pre-tests.md
    │   ├── tasks.md
    │   └── test-evidence/
    │       └── acceptance-*.log
    │
    └── code-reviews/                         ← B 产出：实现决策笔记 + 评审记录
        ├── implementation-decision-note.md
        └── pr-review-*.md
```

> **全部文件在 B (Brainstorm) 阶段生成**。M (Map) 阶段确认路径正确 → 写入 milestones.md committed_issues → 交付 dev-loop。

> `brainstorms/b-I-{raw key}-A.md` 与 `issues/I-{raw key}-A.md` **suffix 一一对应**。
> suffix 来自 Input（candidate），不是 B2 取的。一个 candidate → 一个 I-* issue → 一个 brainstorm。

### B2 产物清单

| 产物 | 路径 | 要求 |
|------|------|------|
| `issues/I-{raw key}-{suffix}.md` | （见上树） | **I-* issue 完整文档**。含 phase_state、pre_tests_path、verification_artifact_dir 等全部字段 |
| `prd.md` | （见上树） | Goal → Dev-Loop Handoff |
| `pre-tests.md` | （见上树） | 结构化测试计划（含 test_command + expected_output），模板见下方 |
| `tasks.md` | （见上树） | 任务分解，关联 owner issue |
| `code-reviews/` | （见上树） | Implementation Decision Note（5 字段） |

**I-* issue 完整示例**（`docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/issues/I-{raw key}-{suffix}.md`，此处 suffix = A）：

```markdown
---
local_id: I-20260508T011858Z-A
kind: linked
status: in_dev
phase_state: in_dev
promoted_from: raw-20260508T011858Z
source_candidate: docs/B1-docs/raw-20260508T011858Z/candidates.md
canonical_issue_path: ""
platform_ids: {}
primary_platform: ""
last_synced_comment_at: {}
hash: ""
created_at: 2026-05-08T01:18:58Z
updated_at: 2026-05-08T01:18:58Z
intake_id: ""
author: zhaoquan
channel: freely-workflow-guarded-execution
session_refs: []
pre_tests_path: docs/B2-docs/skill-gate-fix/raw-20260508T011858Z/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/skill-gate-fix/raw-20260508T011858Z/code-reviews
---

# I-20260508T011858Z-A: skill 引导与门禁对齐

- source_candidate: `docs/B1-docs/raw-20260508T011858Z/candidates.md`
- pre_tests_path: `docs/B2-docs/skill-gate-fix/raw-20260508T011858Z/verification/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/skill-gate-fix/raw-20260508T011858Z/code-reviews`

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

> ⛑️ **TDD RED-GREEN 流程（B2→dev 之间必须执行）**
>
> B2 写好 pre-tests 后，先跑 RED，再写代码，再跑 GREEN。
>
> | 阶段 | 含义 | fix | feature |
> |------|------|-----|---------|
> | **RED** | 确认测试真的会失败 | 确认 bug 可复现（已有测试、新测试、手工端到端复现均可） | 确认功能还未实现（设计充分的端到端、集成、单元测试） |
> | **GREEN** | 确认实现通过全部测试 | bug 已修复，回归测试通过 | 功能已实现，验收测试通过 |
>
> `red-green-status` 字段：B2 写入时 = `pending` → RED 确认后 = `red` → dev 实现 → GREEN 通过后 = `green`。
> 全部 `green` 或合理 `not_applicable` 后才能进入 test-pre-merge 最终验证。

> ⚠️ **AI 时代测试层级：端到端第一，集成第二，单元第三**
>
> AI 生成的代码最容易在模块边界和端到端流程中出错。
> 端到端测试是防止 AI 代码崩坏项目的最后防线，**不可跳过**。
>
> 设计测试时从最重要开始：
> 1. **端到端（E2E）**：用户可见行为、完整业务流程。AI 代码出错最多的层级。**必须有。**
> 2. **集成**：多模块协作、数据流、状态变更。AI 改 A 模块经常无意破坏 B 模块。
> 3. **单元**：单一函数/脚本的输入输出验证。用于快速定位，但不能替代上面两层。
>
> 层级选择原则：能用端到端兜底就用端到端。没有端到端的设计是不完整的。

> ⚠️ **通用铁律**
>
> - 如果不知道该测什么：重新读 raw issue 理解改动范围，从改动面推导测试面
> - 如果改动不影响某层：写 `not_applicable` 且 **必须写明具体理由**（不是"不适用"三个字敷衍）
> - 禁止：无理由全部 not_applicable + mock
> - 禁止：status 写 pass 但 actual_output 为空（那是 ghost pass，会被 pretests-retirement-gate 硬拦截）
> - 每一条 test_command 必须是真正可执行的测试用例（单元测试、集成测试、端到端测试、API 调用、编译验证、shell 脚本等均可），expected_output 必须具体可验证
> - **糊弄 pre-tests.md 是导致项目失败的严重失职行为。**

```markdown
# Pre-Tests: <功能名>
- issue_id: I-{raw key}-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: <验收条件简述>
- acceptance_target: <raw issue 验收标准>
- testing_layer: unit | integration | end-to-end
- target_environment: test-pre-merge-{raw key}-{slug}
- required_evidence: <测试通过的证据要求>
- evidence_level: mock | integration | real_env | post_merge_dogfood
- artifact_ref: <指向测试产物文件，如 docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/verification/test-evidence/acceptance-1.log>
- test_command: <实际执行的 shell 命令，如：freely test-lane feature-local -- echo ok>
- expected_output: <命令的预期输出（GREEN 时的输出），如：所有测试 PASSED>
- expected_RED_output: <RED 阶段的预期输出——fix: 证明 bug 存在；feature: 证明功能未实现>
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段由 skill `freely-test-execution` 执行后填写)
- evidence_file: (执行后填写。注意 .log 文件可能被 .gitignore 忽略，需 `git add -f` force-add)
- red-green-status: pending | red | green
> B2 写入 = pending。RED 确认后 = red（证明测试真的会失败）。dev 实现后跑 GREEN 通过 = green。
- status: pending | passed | failed | not_applicable
> 必须配合 red-green-status=green + 有 worker state。无 worker state 时 passed 会被判 execution_missing，请改用 not_applicable。
- blocker: (失败时填写) definition_missing | commands_only | evidence_plan_missing | execution_pending_or_failed
- not_applicable_reason: (not_applicable 时必填) change_not_touching_this_layer | no_executable_boundary_at_this_layer | protected_environment_only | human_observation_only | covered_by_more_realistic_required_surface
- not_applicable_explanation: (not_applicable 时必填) <具体原因>
- replacement_evidence: (not_applicable 时必填) <替代验证方式或证据>
- red_how: <RED 怎么确认的> fix: 如何复现 bug（已有测试/新测试/手工端到端步骤）。feature: 设计的测试层级和理由（端到端优先）

### acceptance-2
- id: AT-002
- requirement: <验收条件简述>
- acceptance_target: <验收标准2>
- testing_layer: end-to-end
- target_environment: test-pre-merge-{raw key}-{slug}
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
- target_environment: test-pre-merge-{raw key}-{slug}
- required_evidence: <判定标准>
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: <端到端验证目标>
- testing_layer: end-to-end
- target_environment: test-pre-merge-{raw key}-{slug} → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass | fail
- real_environment_reason: <真实环境验证结果>
```

**status 取值**: `pending`（未执行）、`passed`（通过）、`failed`（失败）。

**blocker 取值**: `definition_missing`（验收标准缺失）、`commands_only`（只有命令无预期输出）、`evidence_plan_missing`（无证据计划）、`execution_pending_or_failed`（未执行或失败）。

### 完成自检

- [ ] I-{raw key} issue `phase_state = done_b2_ibm`
- [ ] pre-tests.md `## Acceptance Items` 含 v2 adequacy 字段
- [ ] tasks.md 存在且任务已分解
- [ ] code-reviews/ 含 Implementation Decision Note
- [ ] milestones.md committed_issues 条目已更新
- [ ] `docs/epics-map.svg` 已更新（新增 epic/story 时必须，运行 `freely check-epics-map` 验证）
- [ ] 下一跳明确：进入 skill `freely-test-RED-execution`

phase_state 流转：`in_b2_ibm → done_b2_ibm → in_dev`

## 不负责

- 不决定 I-* issue 的 key（key 由 `freely-doc-B1_IBM-execution` skill 的 candidate 通过 `promoted_issue_id` 指定）
- **负责**根据 key 确定 epic-name 和 story-name（按 [issue-materialization-checklist.md](references/issue-materialization-checklist.md) 规范），构造完整路径，物化文件
- 不实现代码或运行测试（由 `freely-dev-loop-execution` skill 负责）
- 不直接写 progress（由 `freely-dev-loop-execution` skill 负责）

## 负责

- **在 milestones.md committed_issues 中生成 I-* 正式条目**：根据 `promoted_issue_id` 确定的 epic-name/story-name，填写 I-* issue 的真实路径（`docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/issues/I-{raw key}-{suffix}.md`）
- **物化 I-* issue 完整文档**：在 epics 路径下创建包含完整 frontmatter（phase_state、pre_tests_path、verification_artifact_dir 等）和正文的 issue.md 文件
- 产出 prd.md、pre-tests.md、tasks.md
- 产出 code-reviews/（含 Implementation Decision Note）
- 产出 prd.md、pre-tests.md、tasks.md
- 产出 code-reviews/（含 Implementation Decision Note）

## 门禁报错时路径速查

> 门禁报 `missing`/`not found` 时，先对照 M 阶段「规范目录结构」确认文件放对位置。
> 在错误路径改内容永远过不了门禁。

| 产物 | 路径 |
|------|------|
| I-* issue | `docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/issues/I-{raw key}-{suffix}.md` |
| b-I-* | `docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/brainstorms/b-I-{raw key}-{suffix}.md` |
| prd.md | `docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/prd.md` |
| pre-tests.md | `docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/verification/pre-tests.md` |
| tasks.md | `docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/verification/tasks.md` |
| IDN | `docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/code-reviews/implementation-decision-note.md` |

### 治理文件（B2 需更新）

| 文件 | 路径 | 更新什么 |
|------|------|---------|
| milestones.md | `docs/milestones.md` | I-* issue 写入 `committed_issues`（含 `path:` 字段指向 epics 下真实路径） |
| epics-map.svg | `docs/epics-map.svg` | 新增 epic/story 时必须更新（运行 `freely check-epics-map`） |
| test-gate.env | `{test-worktree}/.freely/run/test-gate.env` | 测试证据（wt-create 创建，daemon 启停更新，门禁检查） |
| worker-verification-contract.env | `{worker-worktree}/.freely/run/worker-verification-contract.env` | Worker closeout 上下文（manager 委派 worker 时写入） |

### 测试证据文件：test-gate.env

仅存在于 test-pre-merge 工位，由 wt-create 创建，daemon 自动更新：

```
TEST_STATUS="completed"                  # not_tested → testing → completed
LAST_TESTED_AT="2026-07-03T02:58:09Z"
LAST_TESTED_COMMIT="27b55acbe290f..."    # 测试时 HEAD commit hash
```

### Worker closeout 上下文：worker-verification-contract.env

Manager 委派 worker 时写入，worker daemon 从中读取：

```
OWNER_ISSUE=I-{raw key}-A
PRE_TESTS_PATH=docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/verification/pre-tests.md
CLOSEOUT_GATE=create
CLOSEOUT_GATE_COMMAND=freely pr-create-guarded
CLOSEOUT_TARGET_LANE=premerge-integration
CLOSEOUT_PROMOTION_GATE=develop_merge
CLOSEOUT_REQUIRES_ADEQUACY=true
CLOSEOUT_REVIEW_ARTIFACT_POLICY=code-reviews
```

### pre-tests.md 各 section 字段速查

| Section | 必填字段 | 特殊约束 |
|---------|---------|---------|
| `## Acceptance Items` → `### acceptance-N` | id, requirement, evidence_level, artifact_ref, red-green-status, status, test_command, expected_output, actual_output | status 写 `passed`（不是 `passed`），red-green-status 写 `green` |
| `## Unit` | acceptance_target, testing_layer, target_environment, required_evidence, blocker_taxonomy | 没有 concrete test tasks 时必须写 not_applicable_reason + not_applicable_explanation + replacement_evidence |
| `## Integration` | 同上 | 同上 |
| `## End-to-End` | 同上 | 同上 |
| `## Real-Environment` | real_environment_status, real_environment_reason | real_environment_status 只能是 `pass` 或 `fail` |

### 枚举值合法范围（从 gate 源码提取）

| 字段 | 合法值 |
|------|--------|
| `surface_kind` | `unit` / `integration` / `end_to_end` / `real_environment` / `post_merge_followthrough` |
| `target_lane` | `feature-local` / `premerge-integration` / `post-merge-followthrough` |
| `promotion_gate` | `completion` / `develop_merge` / `retirement` |
| `evidence_level` | `mock` / `integration` / `real_env` / `post_merge_dogfood` |
| `red-green-status` | `pending` / `red` / `green` / `not_applicable` |
| `status` (acceptance item) | `pass` / `passed` / `not_applicable` |
| `not_applicable_reason` | `change_not_touching_this_layer` / `no_executable_boundary_at_this_layer` / `protected_environment_only` / `human_observation_only` / `covered_by_more_realistic_required_surface` |

---

## 门禁常见坑速查

> 若 gate 报错，先在此表查找匹配项。更多细节见下方规范模板。
>
> **⚠️ 全字段速查**: 每个 acceptance item 必须包含以下字段（缺一不可）:
> `id` / `requirement` / `acceptance_target` / `testing_layer` / `target_environment` /
> `required_evidence` / `evidence_level` / `artifact_ref` / `test_command` / `expected_output` /
> `expected_RED_output` / `actual_RED_output` / `actual_output` / `evidence_file` /
> `red-green-status` / `status` / `blocker`

| gate 报错关键词 | 原因 | 正确格式 |
|-----------|------|---------|
| verification_artifact_dir too broad or non-canonical | 需以 /code-reviews 结尾，规范格式：docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/code-reviews | `docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/code-reviews` |
| implementation decision note is incomplete | 需 5 个字段 | `decision` / `why_this` / `alternatives_considered` / `boundary_non_goals` / `residual_risk` |
| owner issue 'missing' / that issue cannot be resolved | review/code-review 文件需 bullet 格式的 issue_id | `- issue_id: I-20260508T011858Z-A` |
| I-* canonical fields silently cleared | I-* frontmatter 用了 `---` YAML 包裹格式；canonical reader 只解析 bullet | 去掉 `---` 包裹，用 bullet 格式：`- phase_state: completed` |
| phase_state cannot own capability/implementation changes | 实现变更的 I-* 需 completed | `phase_state: completed` |
| pre_tests_path 验证失败 | I-* issue 需声明 pre_tests_path | `pre_tests_path: docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/verification/pre-tests.md` |
| section missing acceptance_target/testing_layer | 字段名必须用下划线，不是空格 | `- acceptance_target:` / `- testing_layer:` / `- target_environment:` / `- required_evidence:` |
| acceptance item missing id/requirement/evidence_level/artifact_ref | 每个 acceptance item 必须有这 4 个字段 | `- id: AT-001` / `- requirement: ...` / `- evidence_level: mock` / `- artifact_ref: <path>` |
| red-green-status missing / invalid / not green | 每个 item 必须有 TDD 状态追踪。合法值: pending\|red\|green\|not_applicable | `- red-green-status: green` |
| evidence_level unsupported | 合法值仅 4 个 | `mock` / `integration` / `real_env` / `post_merge_dogfood` |
| status must be pass or not_applicable | 合法值仅 3 个 | `pass` (GREEN 通过) / `passed` (同义) / `not_applicable` (不适用) |
| artifact_ref references missing / pending:// | artifact_ref 必须指向磁盘或 git 跟踪的真实文件 | `- artifact_ref: tests/pytest-output.log` |
| execution_missing: got passed | passed 需要测试证据，无则改用 not_applicable | `- status: not_applicable` + not_applicable_reason + replacement_evidence |
| not_applicable missing replacement_evidence | not_applicable 的 item/section 必须写 replacement_evidence | `- replacement_evidence: <替代验证方式>` |
| not_applicable_reason 不支持 | 合法值仅 5 个 | `change_not_touching_this_layer` / `no_executable_boundary_at_this_layer` / `protected_environment_only` / `human_observation_only` / `covered_by_more_realistic_required_surface` |
| section 'X' has no concrete test tasks | section 下需有编号列表测试任务(如 `1. task`)或 lawful not_applicable_reason | 添加 `- not_applicable_reason:` + `- not_applicable_explanation:` + `- replacement_evidence:` |
| Real-Environment missing / unsupported status | real_environment_status 只能是 pass 或 fail | `- real_environment_status: pass` + `- real_environment_reason: <理由>` |
| section missing blocker_taxonomy | Unit/Integration/End-to-End 必须声明 blocker_taxonomy | `- blocker_taxonomy: execution_pending_or_failed` |
| test gate missing / not tested | test-gate.env 缺失或 TEST_STATUS=not_tested | 在 test-pre-merge 工位启动 daemon：`freely daemon start --task-mode auto` |
| surface_kind unsupported | 合法值仅 5 个 | `unit` / `integration` / `end_to_end` / `real_environment` / `post_merge_followthrough` |
| target_lane unsupported | 合法值仅 3 个 | `feature-local` / `premerge-integration` / `post-merge-followthrough` |
| promotion_gate unsupported | 合法值仅 3 个 | `completion` / `develop_merge` / `retirement` |
| evidence_plan_missing — needs real premerge-quality test evidence | premerge+develop_merge 要求的 adequacy v2 item: evidence_level≥integration, status=pass, artifact_ref 存在 | `- surface_kind: end_to_end` / `- target_lane: premerge-integration` / `- promotion_gate: develop_merge` / `- task_refs: A1-A6` / `- case_design: <测试设计说明>` |
| task_closeout_missing / task_closeout_incomplete | I-* completed 时须有 tasks.md 且全部 [x] | 创建 tasks.md，所有任务标记 [x] |
| pretests_retirement_binding_missing | worker-verification-contract.env 缺少 closeout 字段 | 补充 `CLOSEOUT_GATE_COMMAND` 等字段到 contract 文件，详见上方 worker-verification-contract.env 模板 |

## 规范文档示例(copy-paste可用)

### I-* issue.md（完整模板）

```markdown
<!-- I-* frontmatter 使用 bullet 格式（- key: value），不用 YAML --- 包裹。
     canonical reader (cgrab) 解析 bullet 和 YAML 均可，但 bullet 是推荐格式。 -->
- issue_id: I-20260508T011858Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260508T011858Z-A
- source_candidate: docs/B1-docs/raw-20260508T011858Z/candidates.md#C-20260508T011858Z-A
- verification_artifact_dir: docs/B2-docs/skill-gate-fix/raw-20260508T011858Z/code-reviews
- canonical_issue_path: ""
- title: 简短描述

# I-20260508T011858Z-A: 标题

- source_candidate: docs/B1-docs/raw-20260508T011858Z/candidates.md#C-20260508T011858Z-A
- verification_artifact_dir: docs/B2-docs/skill-gate-fix/raw-20260508T011858Z/code-reviews
```

### Implementation Decision Note（完整模板）

```markdown
---
issue_id: I-20260508T011858Z-A
issue_path: docs/B2-docs/skill-gate-fix/raw-20260508T011858Z/issues/I-20260508T011858Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260508T011858Z-A
- issue_path: docs/B2-docs/skill-gate-fix/raw-20260508T011858Z/issues/I-20260508T011858Z-A.md

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
- issue_path: docs/B2-docs/skill-gate-fix/raw-20260508T011858Z/issues/I-20260508T011858Z-A.md

## 1. Worktree Check
^- status: passed

## 2. IBM Completeness
^- status: passed

## 3. Code Review Evidence
^- status: passed

## 4. Pre-test Evidence
^- status: passed

## 5. Receipt Integrity
- status: n/a

## 6. Phase State
^- status: passed

## Overall Verdict
- verdict: pass
```

## 工作流

1. 确认 Input：milestones.md candidate_issues 中有 status=promoted 的 candidate
2. 读取 candidate 的 `promoted_issue_id`，确认 I-* issue 目标路径
3. 读取 [issue-materialization-checklist.md](references/issue-materialization-checklist.md)
4. Materialize I-* issue 到 `docs/B2-docs/{epic-name}/{story-name}/raw-{raw key}/issues/`
5. 写 prd.md、pre-tests.md、tasks.md
6. 写 code-review（含 Implementation Decision Note）
7. 更新 milestones.md committed_issues（写入物化后的 I-* issue）
7. 若发现边界外新问题：返回 `next_recommended_route=freely-doc-B1_IBM-execution`
8. B2_IBM 完成后，进入 RED 阶段（skill `freely-test-RED-execution`）确认全部测试 RED → dev-loop 实现 → GREEN → pr-create-guarded（提 PR）→ pr-merge-guarded（门禁合并）→ wt-close（收口）

## 关键参考

- PRD 质量门槛：[references/prd-quality-bar.md](references/prd-quality-bar.md)
- 设计派生的硬约束：`pre-tests.md` 和 `tasks.md` 必须从 `prd.md` 自然派生，不能与 PRD 脱节

B2_IBM 是 doc-loop 的第二阶段（物化设计）。本阶段定义 pre-tests.md 测试方案，
由 dev-loop 的 test 阶段执行。doc-loop 通过 review 后交付 dev-loop，
dev-loop 的输出经 test（GREEN）和 review（Reviewer Agent）双重验证。

三环能力生命周期总图（含回环机制）的唯一细节真源：
`docs/system/workspace/three-loop-capability-lifecycle.md`
