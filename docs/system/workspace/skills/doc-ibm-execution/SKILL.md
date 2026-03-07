---
name: doc-ibm-execution
description: 在法律和宪法下执行 issue-bound docs 环，负责 `IBM+G` 产物、里程碑同步和进入 `dev-loop-execution` 前的文档收敛。
---

# skill:doc-ibm-execution

## 职责

- 负责在已有 issue 边界内完成 issue-bound `IBM+G` 文档收敛。
- 负责把问题从“已有 issue 但文档仍不足”推进到“ready for dev”或“明确阻塞”。
- 负责 docs、milestone、candidate 提升记录之间的一致性。
- 不负责代码实现；实现进入 `dev-loop-execution`。
- 调用方必须把当前要处理的 issue 或 candidate-to-issue 上下文传入；本 skill 不负责自己挑新的 issue 来做。

## 进入条件

- `IBM`：issue 接入、brainstorm、mapping、里程碑与路由同步。
- `G`：治理资产维护（`docs/CONSTITUTION.md`、`docs/LAWS.md`、`docs/system/workspace/skills/**`）的一致性修复与收敛。
- 当前已有 issue path，或已从 candidate 提升为 issue。
- 当前仍缺 issue-bound brainstorm、mapping、`PRE_TEST`、tasks 或治理口径收敛。

## 输入上下文

- 调用方传入的当前 issue 标识、issue path 或 candidate-to-issue 提升信息
- 调用方显式附带或指向的：
  - `docs/epics/{epic}/{story}/issues/{issue-name}.md` 或待创建 issue 路径
  - `docs/milestones.md`
  - 当前关联的 `candidates.md` / `brainstorms.md`，若 issue 来自 pre-brainstorm
  - `docs/CONSTITUTION.md`
  - `docs/LAWS.md`
- 按需读取调用方已指向的补充证据：
  - `docs/progress/**`
  - story-scoped `code-reviews/**` / test / recovery 证据
  - 相关治理资产

## 调用约定

- 调用方至少应传入：
  - `issue_ref` 或 `candidate_ref`
  - `issue_scope_summary`
  - `milestone_path`
  - 当前缺失的 docs 产物提示
  - 当前推荐下一跳仍是本 skill 的原因
- 本 skill 只收敛传入 issue 的 docs 边界，不在 skill 内凭空选择别的 issue。

## 工作产物

- `docs/epics/{epic}/{story}/issues/{issue-name}.md`
- `docs/epics/{epic}/{story}/brainstorms/b-{issue-name}.md`
- `docs/epics/{epic}/{story}/prd.md`
- `docs/epics/{epic}/{story}/pre-tests.md`
- `docs/epics/{epic}/{story}/tasks.md`
- `docs/milestones.md`
- 按需更新：
  - `docs/CONSTITUTION.md`
  - `docs/LAWS.md`
  - `docs/system/workspace/skills/**`
- `docs/progress/**` 不是本 skill 的主工作产物；progress 主回写归 `dev-loop-execution`。

## 工作步骤
1. 接收 issue 并对齐 epic/story/milestone 所有权。
2. 产出或更新 issue-bound brainstorm：`brainstorms/b-{issue-name}.md`。
3. 在 map 阶段完善：
   - `prd.md`
   - `pre-tests.md`
   - `tasks.md`
4. 在开发开始前定义 `PRE_TEST` 基线，包括集成验收标准与最小证据要求。
5. 若当前 issue 来源于 pre-brainstorm candidate：
   - 更新 `candidates.md` 的 `promoted_issue_path`
   - 更新 candidate 状态与 route/status 记录
6. 原子化同步 `docs/milestones.md` 与 issue 映射、状态和下一动作。
7. 若存在治理漂移（术语、路由、证据口径、门禁语义不一致），触发 `G` 轨维护并更新对应治理资产。
8. 治理资产变更必须在专用 `feature/*` 分支 + worktree 中进行，并绑定关联实现或门禁变更证据。
9. 用 `skill:laws-enforcer` 验证。
10. 若 issue 已具备实现条件，明确向 `auto-loop` 返回“可进入 dev-loop”的状态与最小上下文。

## 不负责

- 不直接修改实现代码作为主工作。
- 不把 code-review/test 暴露的新边界问题强行塞进当前 issue；若边界变化，应回流给 `auto-loop` 重判。
- 不替代 `dev-loop-execution` 的实现、测试与 progress 主回写职责。

## 状态回流给 auto-loop

当出现以下任一情况时，应把状态交还 `auto-loop`：

- issue 文档已 ready for `dev-loop-execution`
- 当前 issue 仍需继续 docs 收敛
- 当前被阻塞
- 发现边界变化，应该退回 `doc-pre-brainstorm-execution` 或重新路由

回流时最少应提供：
- `status`: `in_progress | blocked | reroute_required | completed`
- `why`
- `updated_artifacts`
- `next_recommended_route`
- `recovery_context`

语义要求：
- ready for dev 时，`next_recommended_route` 设为 `dev-loop-execution`
- 仍缺 `b-issue/prd/pre-tests/tasks` 任一关键产物时，保持 `doc-ibm-execution`
- 若 issue 边界失稳，明确说明为何不能继续留在本环

## 完成判定

- 必需的 issue-bound docs 产物完整。
- `IBM` 与 `G` 两轨在当前 issue 范围内保持一致可追溯。
- 已明确是进入 `dev-loop-execution`，还是因阻塞/边界变化回流外循环。
