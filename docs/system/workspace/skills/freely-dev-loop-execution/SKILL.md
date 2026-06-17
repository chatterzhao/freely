---
name: freely-dev-loop-execution
description: 执行 scan-selected 或 handoff-continued ready issue 的实现、测试与进度回写。
---

# skill:freely-dev-loop-execution

> 全链路: feedback → wt-create → B1_IBM → B2_IBM → dev → pr-create-guarded → pr-merge-guarded → wt-close
>                                                          ↑ you are here（实现 + code-review + pre-tests）

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
3. 确认 issue / milestone 的 `phase_state=done_ibm` 或 `in_dev`。
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
1. 仅把执行态写入 `docs/progress/{epic}/p-{issue}.md`：
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

pre-tests.md 是验证计划，不是门禁表单。写真正会执行的测试，引用实际存在的测试产物。

**必需章节**：

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
- status: pass
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
