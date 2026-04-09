---
name: doc-ibm-execution
description: 在法律和宪法下执行 milestone-owned issue 的 `IBM+G` 文档收敛。
---

# skill:doc-ibm-execution

## 职责

- 处理 milestone 已接纳的 candidate / milestone-owned issue。
- 先把 milestone `candidate_issues` 中的输入 materialize 成正式 `epic/story` 目录与一个或多个 milestone-owned issue，再把这些 issue 从“docs 不足”推进到“ready for dev”或“明确阻塞”。
- 同步 issue、milestone 与治理资产。
- `IBM + G` 作为 doc-loop 的一部分，其循环归宿与生命周期细节以 `docs/system/workspace/three-loop-capability-lifecycle.md` 为准。

## 不负责

- 不把 raw problem 直接当作 IBM issue。
- 不直接承担实现代码、测试与 progress 主回写。

## 工作流

1. 先读取 [issue-materialization-checklist.md](references/issue-materialization-checklist.md) 确认当前输入已经被 milestone 接纳；若当前还只是 pre-brainstorm candidate，则先回到 `doc-pre-brainstorm-execution`。
2. 对 milestone `candidate_issues` 中的 `M-{issue-id}`，先完成 `B` 的 materialization 职责：
   - 确定 `epic-name`
   - 确定 `story-name`
   - 判断该 `M-{issue-id}` 应拆成一个还是多个正式 `I-{issue-id}*`
   - 明确这些 `I-*` 在 milestone 中属于哪个阶段、什么顺序
3. 只有当 `M-{issue-id}` 已被 materialize 成一个或多个正式 `I-{issue-id}*` 后，才继续写 IBM 正式产物。
4. 补齐 IBM 产物时，`prd.md` 不得只停留在人类摘要；必须按 [prd-quality-bar.md](references/prd-quality-bar.md) 达到 AI-ready 的最小结构。
5. 若 IBM 产物缺失或不完整，按 [ibm-completion-gate.md](references/ibm-completion-gate.md) 补齐 issue、brainstorm、`prd.md`、`pre-tests.md`、`tasks.md` 与 milestone 回写。
6. `pre-tests.md` 和 `tasks.md` 必须从 `prd.md` 自然派生；若三者之间仍需大量口头补充，视为 IBM 未收口。
7. 在 IBM 中继续深化验收边界：
   - 把 candidate-level acceptance 转成 issue-level acceptance
   - 让 `pre-tests.md`、`tasks.md` 和 issue-bound brainstorm 体现这层深化
8. `pre-tests.md` 不是附属清单，而是 issue-level acceptance 的主控制面：
   - 默认先写 executable acceptance contract，而不是 wording review / truth-source reading checklist
   - 默认优先表达 focused regression、integration、real-environment、dogfood 这些行为验收面
   - 对第一阶段结构，至少固定四个章节：`Unit`、`Integration`、`End-to-End`、`Real-Environment`
   - 四个章节必须都出现；不适用时不得省略，必须写 `not_applicable_reason`、`not_applicable_explanation` 与 `replacement_evidence`
   - `not_applicable_reason` 只允许有限白名单：`change_not_touching_this_layer`、`no_executable_boundary_at_this_layer`、`protected_environment_only`、`human_observation_only`、`covered_by_more_realistic_required_surface`
   - 至少要能恢复 acceptance target、testing layer、target environment、required evidence 与 blocker taxonomy
   - 最小 blocker taxonomy 至少区分：`definition_missing`、`commands_only`、`evidence_plan_missing`、`execution_pending_or_failed`
   - 若存在 merge 后才能验证的能力，显式标记 `post-merge acceptance`
   - 并明确目标验证环境：`develop` 或某个 `test-pre-merge-*` 批次
   - 对每个关键 acceptance 面，写出最小 `environment`、`evidence`、`failure signal`、`failure handling / replay expectation`
   - 对 Freely 自治能力，默认回答：
     - unit
     - pre-merge focused regression / smoke
     - integration
     - end-to-end
     - real-environment
     - post-merge integration acceptance
     - post-merge application-native real-environment acceptance
     - post-merge end-to-end dogfood acceptance
   - 若某类测试面不适用，显式写出不适用理由、短解释与替代证据，而不是省略
   - 写清该环境只用于验证，不用于继续实现
   - 不要让后续 verification 只能靠口头解释或代码阅读来恢复验收标准
9. 若文档已经足够驱动实现，按同一 gate 把 `phase_state` 切到 `done_ibm`，并返回最小实现上下文。
10. 若在 IBM 中发现边界外新问题，停止扩写当前 issue，返回 `next_recommended_route=doc-pre-brainstorm-execution`。

## 回流输出

- `status`
- `why`
- `updated_artifacts`
- `next_recommended_route`
- `recovery_context`
- `execution_base`
- `integration_target`
- `depends_on`

## 完成判定

- 当前 issue 已明确属于 milestone-owned issue。
- 当前 milestone candidate 若进入 IBM，已被 materialize 成一个或多个 `I-{issue-id}*`，且这些 issue 已回写到 milestone 的正式编排区。
- 关键 IBM 产物完整，或已明确为什么必须 reroute。
- `prd.md` 已达到 AI-ready quality bar，且 `pre-tests.md`、`tasks.md` 与之对齐。
- candidate acceptance 已被深化为 issue-level acceptance。
- `pre-tests.md` 已明确本 issue 的主验收面，且默认以 executable acceptance evidence 为主，而不是 wording review 为主。
- `pre-tests.md` 质量 gate 已足够区分“定义不完整”和“执行未完成/失败”。
- 进入 dev-loop 所需的最小上下文已备齐。
