---
name: no-usable-issue-skill
description: 当当前输入尚未命中 usable issue 时，继续在 pre-brainstorms 收敛，并原子同步 milestone。
---

# skill:no-usable-issue-skill

## 适用边界

- 当前输入没有命中可直接执行的 issue。
- 当前工作仍停留在 pre-brainstorm / candidate 收敛阶段。

## 工作产物

- `docs/pre-brainstorms/<id>/brainstorms.md`
- `docs/pre-brainstorms/<id>/candidates.md`
- `docs/milestones.md`

## 主事实源

- pre-brainstorm 阶段的主事实源是 `candidates.md`
- milestone 只承接 candidate 被接纳后的扫描入口
- 本 skill 负责把 candidate 事实同步进 milestone，但执行态事实源还不在这里

## Candidate Schema

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

## 工作流

1. 确认当前输入为何不构成 usable issue：
   - 尚无 issue path
   - milestone 中仅为 candidate
   - 虽有条目，但仍需研究 / 排序 / 边界收敛
2. 在 `docs/pre-brainstorms/<id>/brainstorms.md` 记录收敛过程。
3. 在对应 `candidates.md` 写入或更新 candidate：
   - `status`
   - `decision_reason`
   - `promoted_issue_path`
   - `milestone`
   - `session_refs`
4. 当 candidate 状态不是 `dropped` 时，原子更新 `docs/milestones.md`：
   - 归属哪个 milestone
   - 位于 `candidate_issues` 还是 `committed_issues`
   - 当前下一步动作是什么
5. 当 milestone 绑定已经完成时，必须回写 `candidates.md`：
   - `milestone` 不再允许停留在 `pending://milestone-binding`
   - 若该 candidate 已被接纳进入后续执行面，`status` 必须更新为 `promoted`
6. 若本轮收敛已足以形成 usable issue：
   - 本 skill 到此结束，不再继续承载执行态
   - 回流给 `lead-agent`，下一轮改由 `has-usable-issue-skill` 消费 milestone / issue 状态
7. 若只是治理问题，允许同步更新治理文档，但不得假装已经进入 dev-loop。

## 退出条件

- 已形成新的候选或更新后的候选，并完成 milestone 绑定。
- 或者问题被判定为 `dropped`，并从活跃 milestone 队列移除。
- 或者已经收敛到足以交给 `has-usable-issue-skill`。

## 完成

- `brainstorms.md` 与 `candidates.md` 已更新。
- `docs/milestones.md` 与 candidate 状态保持原子一致。
- candidate 被提升后，执行态不再继续写回 candidate schema。
