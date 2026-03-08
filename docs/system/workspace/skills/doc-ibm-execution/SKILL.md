---
name: doc-ibm-execution
description: 在法律和宪法下执行 milestone-owned issue 的 `IBM+G` 文档收敛。
---

# skill:doc-ibm-execution

## 职责

- 只处理 milestone 已接纳的 issue。
- 先确定正式目录归属，再把 issue 从“docs 不足”推进到“ready for dev”或“明确阻塞”。
- 同步 issue、milestone 与治理资产。

## 不负责

- 不把 raw problem 直接当作 IBM issue。
- 不直接承担实现代码、测试与 progress 主回写。

## 进入前检查

1. 当前输入必须已经是 milestone-owned issue，或 candidate 已被 milestone 接纳。
2. 在写任何 IBM 产物前，必须先确认正式归属：
   - `epic-name`
   - `story-name`
   - `issue-name`
3. 如果上述任一归属尚未稳定，停止写正式 IBM 产物，回到 `doc-pre-brainstorm-execution` 继续收敛。
4. IBM 正式产物必须落在 `docs/epics/{epic-name}/{story-name}/...`，不得继续写回 `docs/pre-brainstorms/`。

## 情景步骤

### 情景 A：candidate 已进入 milestone，开始 issue materialization

这样做：
1. 先确认当前输入已经是 milestone-owned issue，或 candidate 已被 milestone 接纳。
2. 若还只是 pre-brainstorm candidate 且未进入 milestone：
   - 停止
   - 回到 `doc-pre-brainstorm-execution`
3. 先确定正式归属目录：
   - `docs/epics/{epic-name}/{story-name}/issues/{issue-name}.md`
   - `docs/epics/{epic-name}/{story-name}/brainstorms/b-{issue-name}.md`
   - `docs/epics/{epic-name}/{story-name}/prd.md`
   - `docs/epics/{epic-name}/{story-name}/pre-tests.md`
   - `docs/epics/{epic-name}/{story-name}/tasks.md`
4. 若 `epic-name` / `story-name` / `issue-name` 任一未稳定：
   - 停止写 IBM 正式产物
   - 回到 `doc-pre-brainstorm-execution`
5. 对齐当前 issue 的 `epic-name` / `story-name` / milestone 所有权。
6. 建立或更新：
   - `docs/epics/{epic-name}/{story-name}/issues/{issue-name}.md`
   - `docs/epics/{epic-name}/{story-name}/brainstorms/b-{issue-name}.md`
   - `docs/epics/{epic-name}/{story-name}/prd.md`
   - `docs/epics/{epic-name}/{story-name}/pre-tests.md`
   - `docs/epics/{epic-name}/{story-name}/tasks.md`
7. 同步回填：
   - `candidates.md.promoted_issue_path`
   - `docs/milestones.md.issue_path`
   - `loop_stage=ibm`
   - 从 candidate 继承当前有效 `session_refs`

### 情景 B：issue 文档仍不完整

这样做：
1. 找出缺失项：
   - issue-bound brainstorm
   - `prd.md`
   - `pre-tests.md`
   - `tasks.md`
   - 治理一致性修复
2. 逐项补齐。
3. 更新 `docs/milestones.md` 的 issue 状态与下一动作。
4. 若当前仍在 IBM 收敛，使用 `loop_stage=ibm`；不要为纯 IBM 工作伪造 `progress`。
5. 如果该 issue 依赖未合并父分支：
   - 在 issue 文档中保留 `execution_base`、`integration_target`、`depends_on`

### 情景 C：issue ready for dev

这样做：
1. 确认文档已足够驱动实现。
2. 把下一跳设为 `dev-loop-execution`。
3. 同步把 issue / milestone 的 `loop_stage` 调整为 `ready_for_dev`。
4. 返回最小实现上下文包：
   - `issue_ref`
   - `implementation_scope_summary`
   - `required_doc_refs`
   - `execution_base`
   - `integration_target`
   - `depends_on`

### 情景 D：在 IBM 中发现这是边界外新问题

这样做：
1. 不把它硬塞进当前 issue。
2. 记录为什么超出当前 issue 边界。
3. 返回 `next_recommended_route=doc-pre-brainstorm-execution`。

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
- 关键 IBM 产物完整，或已明确为什么必须 reroute。
- 进入 dev-loop 所需的最小上下文已备齐。
