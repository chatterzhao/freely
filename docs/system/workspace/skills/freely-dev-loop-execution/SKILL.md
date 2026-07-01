---
name: freely-dev-loop-execution
description: >-
  执行 issue 的代码实现与 TDD RED-GREEN 验证。测试先行，代码后行。
  产出 code-review + Implementation Decision Note。不碰 pre-tests.md
  （测试方案由 `freely-doc-B2_IBM-execution` skill 编写）。

  Use when: `freely-test-RED-execution` skill 确认全部 RED 之后，
  需要写实现代码。触发词："写代码"、"dev"、"实现"、"开发"、
  "开始写"、"coding"。
---

# skill:freely-dev-loop-execution

> 全链路: [cmd] freely feedback → [skill] freely-workflow-guarded-execution → [cmd] freely wt-create → [skill] freely-doc-B1_IBM-execution → [skill] freely-doc-B2_IBM-execution → [skill] freely-test-RED-execution → [skill][here] freely-dev-loop-execution → [skill] freely-test-execution → [cmd] freely pr-create-guarded → [cmd] freely pr-review-guarded → [cmd] freely pr-merge-guarded → [cmd] freely wt-close

## 职责

- 只处理 docs 已足够的 ready issue。
- 在正确 worktree 中实现、测试并回写状态。
- `dev-loop` 中的“实现”不限于传统代码；也可以是 agent、skill、runtime script、hook、reference 或其他能力产物，只要它们属于已收敛 issue 的交付实现。
- 让 `progress` 只承载 dev-loop 的执行态。
- three-loop 总图与 semantics 的唯一细节真源是 `docs/system/workspace/three-loop-capability-lifecycle.md`；本 skill 只定义 dev-loop 执行步骤，不平行维护总图。
- 若 dev-loop 的 loop placement、回流语义、verification / cleanup handoff 变化，必须先同步检查该真源，再更新本 skill。

## 不负责

- 不重新发明 issue 边界。
- 不把边界外新问题伪装成当前 issue 的实现细节。
- 不承担 pre-brainstorm / IBM 主工作。
- 不自己宣布 terminal completion、cleanup 或 retirement。

## 情景步骤

### 情景 A：开始实现 ready issue

这样做：
1. 读取 issue、`prd.md`、`pre-tests.md`、`tasks.md`、milestone。
2. 确认当前 issue 已是 ready issue，而不是候选或仅 docs 收敛中的 issue。
3. 确认 issue / milestone 的 `phase_state=done_b2_ibm` 或 `in_dev`。
4. 确认当前 worktree 正确：
   - 独立 issue -> 通常基于 `develop`
   - 依赖父分支 -> 基于 `execution_base`
5. 在当前 dedicated worktree 中实现变更。
6. 持续补齐测试、verification evidence 与 code-review 证据。
   - 默认先在当前 dedicated worktree 跑 `./bin/test-lane feature-local -- <command...>`
   - 若需要主线前真实集成面，切到对应 `test-pre-merge-*` worktree 跑 `./bin/test-lane premerge-integration -- <command...>`
   - 若变更已 merge 到目标 protected branch 且需要真实 followthrough，在该 canonical worktree 跑 `./bin/test-lane post-merge-followthrough -- <command...>`
7. 若本轮是 develop-bound implementation-bearing 变更，在当前 owner issue 的 `verification_artifact_dir` 下写 implementation decision note。
   - 最小字段见 [implementation-decision-note.md](references/implementation-decision-note.md)
   - 不要把这份 note 改写到 `progress`、`prd.md` 或新目录里当成平行真源

### 情景 B：回写执行进度

这样做：
1. 仅把执行态写入 `docs/progress/{epic-name}/p-{issue}.md`（`{epic-name}` 由 `freely-doc-B2_IBM-execution` skill 确定——与 I-* issue 所在的 epic 一致）：
   - 当前实现进度
   - 测试结果
   - blocker
   - 恢复上下文
   - 当前活跃 `session_refs`
2. 不把 candidate 收敛或纯 IBM 状态写进 `progress`。
3. 同步更新 milestone 与 issue 状态，并把 `phase_state` 置为 `in_dev`。

### 情景 C：实现中发现边界外新问题

这样做：
1. 不把它塞回当前 issue。
2. 在当前 issue / progress 中记录影响与 blocker。
3. 若会触发恢复或重跑，补充当前 `runtime_state` 与 `session_refs`。
4. 返回：
   - `status=reroute_required`
   - `next_recommended_route=freely-doc-B1_IBM-execution`
   - 新问题证据摘要

### 情景 D：pre-tests.md 结构

> pre-tests.md 完整模板由 `skill:freely-doc-B2_IBM-execution` 内置提供。
> `freely-doc-B2_IBM-execution` skill 阶段写好 `test_command` + `expected_output`，dev-loop 阶段先 RED 后 GREEN。
> 正式执行验证由 `skill:freely-test-execution` 负责——逐条执行并收集 evidence。

dev-loop 阶段的职责：
- 读取 B2 写好的 pre-tests.md
- **先跑 RED**：实现前先执行 test_command，确认测试能失败（证明测试有效）
- **再跑 GREEN**：实现后重新执行，全部 passed 才进入 test skill
- 把 RED-GREEN 结果记录到 pre-tests.md 的 actual_output / evidence_file

**必需章节**（详见 `freely-doc-B2_IBM-execution` skill 模板）：

| 章节 | 内容 |
|------|------|
| `## Unit` | 单元级测试目标 |
| `## Integration` | 集成测试目标 |
| `## End-to-End` | 端到端验证 |
| `## Real-Environment` | 真实环境结论（含 `real_environment_status` 和 `real_environment_reason`） |
| `## Acceptance Items` | 可追踪的验收项 |

**范例**：

```markdown
# Pre-Tests: <功能名>
- issue_id: I-{key}-A

## Unit
- acceptance target: <具体要验证什么>
- testing layer: unit
- target environment: <feature worktree>
- required evidence: <测试通过的判定标准>
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: <为什么这层不能用自动化测试，以及怎样替代验证>
- replacement_evidence: <实际执行的替代验证方式和结果>

## Integration
- acceptance target: <集成面要验证什么>
- testing layer: integration
- target environment: <test-pre-merge worktree 或等价面>
- required evidence: <集成测试通过的判定标准>
- blocker taxonomy: execution_pending_or_failed

## End-to-End
- acceptance target: feature→test-pre-merge→develop merge passes
- testing layer: end_to_end
- target environment: develop-bound guarded merge chain
- required evidence: guarded merge receipts
- blocker taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: <真实环境验证结果>

## Acceptance Items
### AT-001 <验收项名>
- id: <唯一标识>
- requirement: <验收条件>
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
^- status: passed
- artifact_ref: <指向实际测试产物文件，如 test 脚本或 test 输出日志，不要指向源代码>
```

`not_applicable_reason` 取值：`change_not_touching_this_layer`、`no_executable_boundary_at_this_layer`、`protected_environment_only`、`human_observation_only`、`covered_by_more_realistic_required_surface`。
`evidence_level` 取值：`mock`、`integration`、`real_env`、`post_merge_dogfood`。
`artifact_ref` 指向测试产物文件（测试脚本、运行日志），不是源码行号。

### 情景 E：实现依赖未合并父分支

这样做：
1. 保留 issue 上携带的 `execution_base`、`integration_target`、`depends_on`。
2. 在提升前先确认父分支结果。
3. 父分支进入要求路径后，把当前分支 restack / rebase / merge 上游。
4. 重新执行必需测试，再继续提升。

### 情景 F：质量三步检查（实现前必须通过）

在开始写代码之前，完成以下三步检查。不是走过场——每步必须产出可验证的记录。

#### F1. Tech Stack Review（技术栈审查）

确认实现方案中使用的技术/工具/库是否正确：

1. 列出本次实现涉及的运行时依赖（语言、库、CLI 工具、外部服务）
2. 对每个依赖确认：
   - 是否已在项目中可用（检查 `config.toml`、`bin/`、现有 worktree）
   - 是否需要新增依赖 → 记录到 issue 的 `depends_on` 字段
   - 版本兼容性是否有已知问题
3. 产出：在 issue 或 progress 中写 `## Tech Stack Review` 段落

#### F2. Architecture Check（架构检查）

确认实现不会破坏现有架构边界：

1. 读取 `docs/CONSTITUTION.md` 和 `docs/PROJECT_INTENT.md` 确认边界约束
2. 确认修改不跨越 loop 边界（doc-loop 不改 runtime、dev-loop 不改 scan 分类）
3. 确认不引入循环依赖（如 skill 之间互相引用、runtime 依赖 sync 脚本的运行时状态）
4. 产出：在 issue 或 progress 中写 `## Architecture Check` 段落

#### F3. Acceptance Criteria Mapping（验收标准映射）

确认每条 acceptance criteria 都有对应的实现和测试：

1. 读取 raw issue 的 acceptance criteria（如果有）
2. 读取 I-* issue 的 pre-tests.md
3. 逐条核对：每条 acceptance criteria → 至少一条 pre-tests 中的 acceptance 项
4. 发现未覆盖的 → 回 `freely-doc-B2_IBM-execution` skill 补充 pre-tests
5. 产出：映射表 `## Acceptance Mapping`（acceptance criteria → pre-tests acceptance-N）

### 情景 G：进入 test skill

dev-loop 完成后（代码已提交、RED-GREEN 通过、质量三步完成）：

→ 进入 `skill:freely-test-execution` — 在 test-pre-merge 工位中逐条执行 pre-tests

```
dev-loop 完成 → test skill（全绿）→ pr-create-guarded
              ↘ (有红) → 回 dev-loop 修复
```

## 按需参考

- 需要最小执行示例时，读取 [execution-examples.md](references/execution-examples.md)。

## 回流输出

- `status`
- `why`
- `updated_artifacts`
- `next_recommended_route`
- `recovery_context`

## 完成判定

- 当前 dev-loop 产物、测试、issue、milestone、progress 已一致，并已把 evidence 交回外层判断。
- 开发完成后：在 worktree 中执行 `freely pr-create-guarded` 命令提 PR → 切换到 develop 分支执行 `freely pr-merge-guarded develop <branch>` 命令合并。禁止绕过。
- 若有依赖父分支，已明确后续 restack / promote 要求。
- terminal completion / cleanup / retirement 仍由 `auto-loop` 判定。

## dev↔test 同步

每次 `git commit` 后立即 merge 到 test-pre-merge：
```
git -C <test-worktree> merge <current-branch>
```
pr-create-guarded 检查两边一致，不一致则硬拦截。
