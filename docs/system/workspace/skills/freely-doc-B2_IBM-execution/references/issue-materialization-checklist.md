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
docs/B2-docs/{epic-name}/                               ← epic：一个能力域
└── {story-name}/                                     ← story：子交付批次
    └── raw-{raw key}/                                ← 一个 raw issue 的全部 B2 产物
        ├── issues/I-{raw key}-{suffix}.md            ← I-* issue（B2 物化）
        ├── brainstorms/b-I-{raw key}-{suffix}.md      ← B2 头脑风暴
        ├── prd.md                                    ← 本 raw 的需求设计
        ├── verification/
        │   ├── pre-tests.md                          ← 本 raw 的测试计划
        │   └── tasks.md                              ← 本 raw 的任务分解
        └── code-reviews/                             ← 本 raw 的审查产物
```

**命名约定**：
- `raw-{raw key}` = 完整的 raw issue local_id，如 `raw-20260628T005815Z`。`raw-` 是 raw issue 的前缀，`{raw key}` 是时间戳 key（`YYYYMMDDTHHMMSSZ`）。**目录名必须是完整的 `raw-{raw key}`**，不是去掉前缀的 `{raw key}`
- I-* 命名继承 raw key + suffix：`I-{raw key}-{suffix}`，如 `I-20260628T005815Z-A`
- b-I-* 命名同 I-*：`b-I-{raw key}-{suffix}`

**规则**：
- 一个 epic 放多个 story；一个 story 放多个 `raw-{raw key}` 目录
- 新 raw → 看归哪个已有 story（如重构 story、修复 story），或新建 story
- 同名 `raw-{raw key}` → 续到已有 story 下的已有目录
- 门禁检查：目录名 `raw-{raw key}` 与 `docs/issues/raw-{raw key}/` 的 raw issue 不匹配 → 拦截
- 门禁检查：I-* 文件名中的 `{raw key}` 与目录名不一致 → 拦截

### 如何确定 epic-name 和 story-name

> **Epic 和 story 是架构决策，不是字符串转换。** 不要从 candidate title 机械提取关键词拼 kebab-case——那是机器思维，产出的是无法理解的目录名。正确做法：理解这个 raw issue 在解决什么能力问题，然后基于语义确定它属于哪个能力域。

#### 什么是 Epic

一个**能力域**（capability domain），可独立理解、独立交付、独立验收。判断标准：如果 3 个月后有人问"Freely 的 XX 是怎么做的"，XX 就是 epic 名。

| ✅ 好的 epic 名 | ❌ 坏的 epic 名 |
|----------------|----------------|
| `worktree-lifecycle`（工位全生命周期） | `fix-wt-create-local-bug`（用 bug 标题当 epic） |
| `ai-session-continuity`（AI 会话连续性） | `acp-session-id-format-fix`（用修复手段当 epic） |
| `process-supervision`（进程监督） | `sup-pid-file-fix`（太窄，单个修复） |
| `issue-sync-platform`（issue 平台同步） | `platform-adapter-title-key`（太具体） |

命名规则：全小写英文，用 `-` 连接，表达一个**稳定的能力概念**，不是任务描述。不包含 `fix-`、`feat-`、`raw-` 前缀。

#### 什么是 Story

Epic 下的一个**可交付切片**。一个 raw issue 的完整生命周期（raw → candidate → I-* issue）通常对应一个 story。同一 epic 下，不同 story 解决 epic 的不同子问题。

Epic `worktree-lifecycle` 下：
- `creation-from-raw-issue`（wt-create 创建工位）
- `cross-worktree-consistency`（dev↔test 一致性）
- `cleanup-and-retirement`（wt-close 收口）

Epic `ai-session-continuity` 下：
- `session-id-extraction`（session ID 提取兼容）
- `prompt-branch-output-fix`（prompt 分支输出修正）

命名规则：全小写英文，用 `-` 连接，表达 story 解决的**具体切面**。

#### 决策流程

1. **读全貌**：`docs/epics-map.svg` 了解已有 epic 和 story。epics-map.svg 是架构地图——每个 `<rect id="epic-{name}">` 是一个能力域，其下 `<rect id="story-{name}">` 是各 epic 的子交付切片。
2. **读 candidate**：理解这个 raw issue 到底在解决什么**能力层面**的问题。不是"修了一个 bug"，而是"这个 bug 属于哪个能力域的哪个切面"。
3. **判是否已有 epic 覆盖**：
   - 涉及的**能力域**与已有 epic 重叠 → 复用该 epic。例如：raw issue 修的是 session ID 提取的 OpenCode 兼容问题 → epic `ai-session-continuity`（不是 `acp-session-id-format-fix`——那是修复手段，不是能力域）
   - 涉及的**能力域**与所有已有 epic **正交**（独立可理解、独立可验收）→ 新建 epic
4. **判 story**：
   - 同一 epic 下已解决过这个子问题 → 续到已有 story 的 `raw-{raw key}` 目录
   - 是 epic 下的新子问题 → 新建 story
5. **不需要脚本自动化**：epic 和 story 的名字是人读的架构索引——基于语义判断，不基于关键词匹配
6. **更新 `docs/epics-map.svg`**：新建或变更 epic/story 后必须更新 SVG。在 SVG 中添加对应的 `<rect id="epic-{name}">` 和/或 `<rect id="story-{name}">` 元素。门禁（`./bin/check-epics-map`）会检查 SVG 与 `docs/B2-docs/` 目录结构是否对齐——不对齐则拦截

#### 层级模型

```
docs/B2-docs/
└── {epic}/                  ← 能力域。一个 epic 下可以有多个 story
    ├── {story-1}/           ← epic 的一个切面
    │   ├── raw-{key-A}/     ← 一个 raw issue 的全部 B2 产物
    │   └── raw-{key-B}/     ← 同 story 的另一个 raw issue
    └── {story-2}/           ← epic 的另一个切面
        └── raw-{key-C}/
```

- **一个 epic**：放多个相关的 story
- **一个 story**：放多个相关的 `raw-{raw key}` 目录（continuation、closeout 等同一子问题的不同阶段）
- **一个 `raw-{raw key}` 目录**：一个 raw issue 的全部 B2 产物（I-* issue、brainstorms、prd、pre-tests、tasks、code-reviews）

#### 维护职责

B2_IBM 确定 epic 和 story 后，必须完成以下维护操作，不能只写文件不更新索引：

1. **新建 epic 时**：在 `docs/epics-map.svg` 中添加 `<rect id="epic-{name}">`，放在合适的垂直位置（按字母序或能力关联）
2. **新建 story 时**：在对应 epic 的 `<rect>` 下方添加 `<rect id="story-{name}">`
3. **复用已有 epic/story 时**：如果 SVG 中没有对应条目（epic/story 在文件系统存在但 SVG 未记录），补上
4. **写完后验证**：运行 `./bin/check-epics-map --project .` 确认对齐。不对齐 → 门禁拦截，必须修正后再继续
5. **更新 milestones.md**：`promoted_issue_id` 必须指向物化后的实际路径

#### 一个 raw → 一个 story 还是多个？

- 一个 raw issue 的 scope 是一个独立子问题 → 一个 story
- raw issue scope 太大、cover 多个独立切面 → B1_IBM 阶段拆成多个 candidate，每个 candidate → 自己的 story
- 多个 raw issue 解决同一个子问题的不同阶段 → 同一个 story 下多个 `raw-{raw key}` 目录

#### 判定示例

| raw issue | 能力域判断 | epic | story |
|-----------|----------|------|-------|
| "wt-create 的 local 关键字 bug" | 工位创建生命周期 | `worktree-lifecycle`（已有则复用） | `creation-from-raw-issue` |
| "session ID 提取不兼容 OpenCode ses_ 格式" | AI 会话连续性 | `ai-session-continuity` | `session-id-extraction` |
| "pr-create-guarded 错误信息不含 cd 指引" | PR 门禁流程 | `pr-guarded-workflow` | `error-message-guidance` |
| "新增一个 AI CLI 工具的 adapter 支持" | 工具适配层（全新能力） | `tool-adapter-framework`（新建 epic） | `new-cli-adapter-support` |

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

- `docs/B2-docs/{epic-name}/{story-name}/issues/{issue-name}.md`
- `docs/B2-docs/{epic-name}/{story-name}/brainstorms/b-{issue-name}.md`
- `docs/B2-docs/{epic-name}/{story-name}/prd.md`
- `docs/B2-docs/{epic-name}/{story-name}/pre-tests.md`
- `docs/B2-docs/{epic-name}/{story-name}/tasks.md`

Issue front matter 还应显式绑定：

- `pre_tests_path`
- `verification_artifact_dir`
- 若后续会进入 develop-bound implementation materialization，默认约定该目录下的 review / verification artifact 还要承载 `## Implementation Decision Note`
  - 最小字段：`decision`、`why_this`、`alternatives_considered`、`boundary_non_goals`、`residual_risk`

写完后仍需按 [prd-quality-bar.md](prd-quality-bar.md) 检查 `prd.md` 是否达到 AI-ready 最小结构；未达标时不得宣称 `done_b2_ibm`。

## Required write-back

- `candidates.md.promoted_issue_id`
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

Refer to `docs/B2-docs/testing-evidence-ladder/testing-evidence-ladder-and-gate-mapping/prd.md` for:

- **Five evidence levels**: script regression, integration, end-to-end scenario, application-native real-environment, protected-env post-merge acceptance.
- **Completion verification minimum evidence**: per issue class, the minimum `evidence_level` required before `phase_state: completed` may be set.
- **Worktree retirement minimum evidence**: per issue class, the minimum `evidence_level` required before a worktree may be retired.
- **Escalation rules**: lower levels cannot satisfy gates requiring higher levels.
- **Blocker taxonomy extension**: `evidence_gap` (level not met) vs `execution_pending` (tests defined but not yet run).

Checklist:

- [ ] Every acceptance item `evidence_level` uses a valid ladder level name
- [ ] The minimum evidence level for the issue class is satisfied before completion
- [ ] Blocker taxonomy distinguishes level-not-met from execution-pending
