---
name: no-usable-issue-skill
description: 当当前输入尚未命中 usable issue 时，继续在 pre-brainstorms 收敛，并原子同步 milestone。
---

# skill:no-usable-issue-skill

## 适用边界

- 当前输入没有命中可继续执行的正式 issue。
- 当前问题仍处于前置收敛阶段，还不能直接进入 issue-bound `IBM` 或 `DDD`。
- 常见来源包括：
  - `chat` / session evidence
  - `review`
  - `test`
  - `github-issue`
  - `docs/PROJECT_INTENT.md`
  - milestone 中仍停留在 `candidate_issues` 的条目

## 工作产物

- `docs/pre-brainstorms/<id>/brainstorms.md`
- `docs/pre-brainstorms/<id>/candidates.md`
- `docs/milestones.md`

## 主事实源

- pre-brainstorm 阶段的主事实源是 `candidates.md`
- milestone 只承接 candidate 被接纳后的扫描入口
- 本 skill 负责把 candidate 事实同步进 milestone，但执行态事实源还不在这里
- 本 skill 的目标是把原始问题收敛成可路由的 candidate，而不是直接产出正式 story 产物

## Candidate 字段约定

`candidates.md` 应只表达前置收敛状态，字段保持最小：

- `title`
- `status`
- `decision_reason`
- `promoted_issue_path`
- `milestone`
- `session_refs`

`status` 只使用这些前置态：

- `proposed`
- `needs_research`
- `promoted`
- `dropped`

说明：

- `promoted` 表示该 candidate 已被 milestone 接纳，后续应从 milestone / issue 继续推进
- `promoted` 不是开发完成态，也不承载 `in_progress` / `blocked` / `completed` 这类执行态
- `promoted_issue_path` 在 issue 尚未正式落位前可保持 `pending://issue-materialization`
- `milestone` 在未绑定前可保持 `pending://milestone-binding`

## 工作流

1. 确认当前输入为何不构成 usable issue：
   - 尚无 issue path
   - milestone 中仅为 candidate
   - 虽有条目，但仍需研究 / 排序 / 边界收敛
2. 选择或创建当前问题对应的 `docs/pre-brainstorms/<id>/` 目录：
   - `brainstorms.md` 记录讨论、比较、分流理由
   - `candidates.md` 记录本轮形成的候选 issue
3. 在 `docs/pre-brainstorms/<id>/brainstorms.md` 记录收敛过程，至少写清：
   - 问题来源
   - 当前为何不能直接走已有 issue
   - 是否属于新问题、既有问题扩边、或治理漂移
   - 推荐后续路由
4. 在对应 `candidates.md` 写入或更新 candidate：
   - `status`
   - `decision_reason`
   - `promoted_issue_path`
   - `milestone`
   - `session_refs`
5. 当 candidate 状态不是 `dropped` 时，原子更新 `docs/milestones.md`：
   - 归属哪个 milestone
   - 位于 `candidate_issues`
   - 当前下一步动作通常应指向 `doc-loop(IBM+G)`，而不是直接 `dev-loop`
   - 保留 candidate 与 milestone 的可追溯映射
6. 当 milestone 绑定已经完成时，必须回写 `candidates.md`：
   - `milestone` 不再允许停留在 `pending://milestone-binding`
   - 若该 candidate 已被接纳进入后续执行面，`status` 必须更新为 `promoted`
7. 若 candidate 被选中进入后续执行面：
   - 本 skill 到此结束
   - 不自行产出正式 `issues/brainstorms/prd/pre-tests/tasks`
   - 回流给 `context-source-skill` / `lead-agent`，下一轮由 `has-usable-issue-skill` 指挥 issue-bound `IBM` 或 `DDD`
8. 若只是治理问题，允许同步更新治理文档，但不得假装已经进入 dev-loop。

## 与 doc-loop / dev-loop 的边界

- 本 skill 负责的是 `pre-brainstorm -> candidate -> milestone candidate entry`
- 本 skill 不负责：
  - `docs/epics/{epic}/{story}/issues/{issue}.md`
  - `docs/epics/{epic}/{story}/brainstorms/b-{issue}.md`
  - `docs/epics/{epic}/{story}/prd.md`
  - `docs/epics/{epic}/{story}/pre-tests.md`
  - `docs/epics/{epic}/{story}/tasks.md`
  - `docs/progress/{epic}/p-{issue}.md`
- 上述正式 issue 产物属于 issue-bound `IBM` / `DDD`

## 退出条件

- 已形成新的候选或更新后的候选，并完成 milestone 绑定。
- 或者问题被判定为 `dropped`，并从活跃 milestone 队列移除。
- 或者已经收敛到足以交给 `has-usable-issue-skill`。

## 完成

- `brainstorms.md` 与 `candidates.md` 已更新。
- `docs/milestones.md` 与 candidate 状态保持原子一致。
- candidate 被提升后，执行态不再继续写回 candidate 字段。
- 当前问题已经被收敛成后续可由 `doc-loop(IBM+G)` 接管的 candidate，而不是悬空问题。
