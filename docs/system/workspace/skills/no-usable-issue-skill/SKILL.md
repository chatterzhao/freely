---
name: no-usable-issue-skill
description: 当当前输入尚未命中 usable issue 时，继续在 pre-brainstorms 收敛，并原子同步 milestone。
---

# skill:no-usable-issue-skill

## 适用边界

- 当前输入没有命中可直接执行的 issue。
- 当前工作仍停留在 pre-brainstorm / candidate 收敛阶段。

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
5. 若本轮收敛已足以形成可执行边界：
   - 将 candidate 从研究态推进到 committed / ready-to-materialize
   - 回流给 `lead-agent` 在下一轮按 usable issue 处理
6. 若只是治理问题，允许同步更新治理文档，但不得假装已经进入 dev-loop。

## 退出条件

- 已形成新的候选或更新后的候选，并完成 milestone 绑定。
- 或者问题被判定为 `dropped`，并从活跃 milestone 队列移除。
- 或者已经收敛到足以交给 `has-usable-issue-skill`。

## 完成

- `brainstorms.md` 与 `candidates.md` 已更新。
- `docs/milestones.md` 与 candidate 状态保持原子一致。
