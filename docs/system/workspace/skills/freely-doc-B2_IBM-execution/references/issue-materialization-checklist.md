# Issue Materialization Checklist

## Entry checks

- 当前输入已经是 milestone-owned issue，或 candidate 已被 milestone 接纳并进入某个 `M-{issue-id}`
- 若仍只是未绑定 milestone 的 pre-brainstorm candidate：回到 `freely-doc-B1_IBM-execution`
- 若来源 candidate 是 `candidate_format_version: v2`，先读取其 `acceptance_criteria`、`promotion_gate`、`open_questions`、`acceptance_reviews`

## Identity and materialization contract

- `C-{issue-id}` 表示 pre-brainstorm candidate 身份
- `M-{issue-id}` 表示 candidate 已进入 milestone `candidate_issues`
- `I-{issue-id}*` 表示 IBM materialization 后的正式 milestone-owned issue 身份
- `B` 的职责不是只写目录；`B` 必须把 `M-{issue-id}` materialize 成一个或多个 `I-{issue-id}*`
- 若拆成多个正式 issue，所有 `I-*` 都必须保留同一个 `{issue-id}` 主键片段，确保能回溯到同一个候选来源
- materialization 完成后，milestone 的正式编排区应挂这些 `I-*`，而不是继续只靠 `M-{issue-id}` 代表执行态

## Stable ownership required

写 IBM 正式产物前，必须先确定 `epic-name` 和 `story-name`。

### 目录结构

```
docs/epics/{epic-name}/                          ← epic：一个能力域
├── {story-name}/                                ← story：epic 下的子交付批次（可选，平铺时省略）
│   ├── issues/{issue-name}.md                   ← I-* issue
│   ├── brainstorms/b-{issue-name}.md            ← B2 头脑风暴
│   ├── prd.md                                   ← 本批次的需求设计
│   ├── pre-tests.md                             ← 本批次的测试计划
│   └── tasks.md                                 ← 本批次的任务分解
└── code-reviews/                                ← 审查产物（epic 级共用）
```

**规则**：
- 一个 epic 可以放多个 story
- 一个 story 对应**一个批次的 I-* + prd + pre-tests + tasks**
- 同批次 = 同一次 B2 执行产出的相关 I-* 集合
- 简单 epic（只有一个批次、一个 I-*）可平铺，省略 story 层
- code-reviews/ 放在 epic 级，不放在 story 下

### 如何确定 epic-name 和 story-name

1. **读取 `docs/epics-map.svg`**：了解现有 epic 和 story 的全貌
2. **从 candidate 提取关键词**：取 candidate title 的核心能力名词，转为 kebab-case slug
3. **搜索已有 epic**：
   - 关键词匹配已有 epic 名 → 用已有 epic
   - 已有 epic 下有 story → 判断本批次是否可归入已有 story，还是需要新建 story
   - 无匹配 → 新建 epic（kebab-case，简短描述能力域，如 `chat-refactor`）
4. **新建 story 的命名**：`{epic-name}` 下的子交付 slug，如 `comment-module`
5. **更新 `docs/epics-map.svg`**：新建或变更 epic/story 后必须更新 SVG，门禁会检查对齐

### 需确认的字段

- `epic-name` — 本 I-* 归属的能力域
- `story-name` — 本 I-* 归属的子交付批次（平铺时可省略）
- `issue-name` — I-* 文件名（继承 `I-{key}-{suffix}`）
- 当前 `M-{issue-id}` 是否需要拆成多个 `I-{issue-id}*`
- 若拆成多个 issue，它们在 milestone 中的阶段归属与排序

任一未稳定：

- 停止写正式 IBM 产物
- 回到 `freely-doc-B1_IBM-execution`

## Required artifacts

- `docs/epics/{epic-name}/{story-name}/issues/{issue-name}.md`
- `docs/epics/{epic-name}/{story-name}/brainstorms/b-{issue-name}.md`
- `docs/epics/{epic-name}/{story-name}/prd.md`
- `docs/epics/{epic-name}/{story-name}/pre-tests.md`
- `docs/epics/{epic-name}/{story-name}/tasks.md`

Issue front matter 还应显式绑定：

- `pre_tests_path`
- `verification_artifact_dir`
- 若后续会进入 develop-bound implementation materialization，默认约定该目录下的 review / verification artifact 还要承载 `## Implementation Decision Note`
  - 最小字段：`decision`、`why_this`、`alternatives_considered`、`boundary_non_goals`、`residual_risk`

写完后仍需按 [prd-quality-bar.md](prd-quality-bar.md) 检查 `prd.md` 是否达到 AI-ready 最小结构；未达标时不得宣称 `done_b2_ibm`。

## Required write-back

- `candidates.md.promoted_issue_path`
- `docs/milestones.md.issue_path`
- 若从一个 `M-{issue-id}` 拆出多个 `I-{issue-id}*`，则 milestone 的正式编排区必须写回这些 `I-*` 的顺序与阶段归属
- 原始 `M-{issue-id}` 只保留来源/追溯语义，不继续代替正式执行编排
- `phase_state=in_b2_ibm`
- 继承有效 `session_refs`
- 在 issue / `prd.md` / `pre-tests.md` / `tasks.md` / issue-bound brainstorm 中继续深化 acceptance 边界
- 在 `pre-tests.md` 中默认先写 executable acceptance 行为，而不是 wording review / truth-source reading checklist
- `pre-tests.md` 默认显式回答：
  - unit
  - pre-merge focused regression / smoke
  - integration
  - end-to-end
  - real-environment
  - post-merge integration acceptance
  - post-merge application-native real-environment acceptance
  - post-merge end-to-end dogfood acceptance
- `pre-tests.md` 至少固定四个章节：
  - `Unit`
  - `Integration`
  - `End-to-End`
  - `Real-Environment`
- `Unit`、`Integration`、`End-to-End` 三章写测试任务本体；若某类 acceptance 不适用，必须同时写出：
  - `not_applicable_reason`
  - `not_applicable_explanation`
  - `replacement_evidence`
- `Real-Environment` 章节固定只写：
  - `real_environment_status`: `pass` 或 `fail`
  - `real_environment_reason`: 必填
- `real_environment_status=pass` 只允许表达两类真结论：
  - 本次实现需要的真实环境测试已完成并达标
  - 本次实现不需要真实环境测试
- `real_environment_status=fail` 必须明确指出：哪些测试/实现面需要真实环境测试却还没做、没通过，或环境与恢复条件还不成立
- 若当前 issue 是 follow-on owner，且 scope 触达 `auth switch / account switch / slot recovery / startup recovery / watchdog / freely start / bin/ai / codex exec` family，`Real-Environment` 章节不能只写结论就过；`Acceptance Items` 至少保留一条：
  - `evidence_level: real_env` 或 `post_merge_dogfood`
  - `status: pass`
  - `artifact_ref` 指向 repo 内可追溯 live artifact，且该 artifact 应能证明真实 `bin/ai` / `codex exec` / `freely start` 中至少一条命令链路被执行或观察
- 前三章的 `not_applicable_reason` 只允许：
  - `change_not_touching_this_layer`
  - `no_executable_boundary_at_this_layer`
  - `protected_environment_only`
  - `human_observation_only`
  - `covered_by_more_realistic_required_surface`
- 对每个关键 acceptance 面，默认写出：
  - environment
  - evidence
  - failure signal
  - failure handling / replay expectation
- 若存在 merge 后验收，显式标记 `post-merge acceptance`
- 在 `pre-tests.md` 中写清 story-level 质量 gate 最低字段：
  - acceptance target
  - testing layer
  - target environment
  - required evidence
  - blocker taxonomy
- 在 `pre-tests.md` 中为 completion gate 写出 machine-readable acceptance items：
  - `id`
  - `requirement`
  - `evidence_level`
  - `status`
  - `artifact_ref`
- 对新写或正在升级 adequacy 的 owner，`Acceptance Items` 默认再写：
  - `surface_kind`
  - `target_lane`
  - `promotion_gate`
- 对 develop-bound guarded promote，默认至少保留一条 item：
  - `target_lane: premerge-integration`
  - `promotion_gate: develop_merge`
  - `status: pass`
  - `artifact_ref` 指向 repo 内可追溯 artifact
- `task_refs`、`case_design` 默认作为强建议字段补齐，减少 acceptance item 与任务脱节、或只剩标题式测试
- 最小 blocker taxonomy 至少区分：
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`
- 对 `post-merge acceptance`，必须同时写出：
  - target environment: `develop` 或某个 `test-pre-merge-*` 批次
  - environment type: `protected verification worktree`
  - failure handling: 验收失败后回到 feature worktree / 新 feature worktree 修复
  - route semantics:
    - `test-pre-merge-*`: 主线前临时验证，承担预检运行测试 / 预测试 merge / develop-bound canonical promote；若失败则回到 dedicated writable worktree 修复
    - `develop`: 已进入主线后的 completion verification，不承担主线前预测试

## Evidence level check

Acceptance items MUST reference the five-level testing evidence ladder by name — do not redefine levels locally.

Refer to `docs/epics/testing-evidence-ladder/testing-evidence-ladder-and-gate-mapping/prd.md` for:

- **Five evidence levels**: script regression, integration, end-to-end scenario, application-native real-environment, protected-env post-merge acceptance.
- **Completion verification minimum evidence**: per issue class, the minimum `evidence_level` required before `phase_state: completed` may be set.
- **Worktree retirement minimum evidence**: per issue class, the minimum `evidence_level` required before a worktree may be retired.
- **Escalation rules**: lower levels cannot satisfy gates requiring higher levels.
- **Blocker taxonomy extension**: `evidence_gap` (level not met) vs `execution_pending` (tests defined but not yet run).

Checklist:

- [ ] Every acceptance item `evidence_level` uses a valid ladder level name
- [ ] The minimum evidence level for the issue class is satisfied before completion
- [ ] Blocker taxonomy distinguishes level-not-met from execution-pending
