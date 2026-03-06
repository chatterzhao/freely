---
name: doc-pre-brainstorm-execution
description: 执行 pre-brainstorm 前置收敛环，负责把原始问题收敛为 candidate，并与 milestone 保持原子同步。
---

# skill:doc-pre-brainstorm-execution

## 适用边界

- 当前输入尚未命中可继续执行的正式 issue。
- 当前问题仍处于前置研究、边界收敛、候选分解阶段。
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
- milestone 承接 candidate 的可扫描入口，但不是前置收敛事实源
- 本 skill 的目标是把原始问题收敛成可路由的 candidate，而不是直接产出正式 story 产物

## 工作流

1. 确认当前为何不能直接进入 `doc-ibm-execution` 或 `dev-loop-execution`：
   - 尚无 issue path
   - milestone 中仅命中 candidate / research-needed 项
   - 虽有相关条目，但当前仍需研究、排序、边界收敛
2. 选择或创建当前问题对应的 `docs/pre-brainstorms/<id>/` 目录。
3. 在 `brainstorms.md` 中记录至少这些内容：
   - 问题来源
   - 当前为何不能直接走已有 issue
   - 是否属于新问题、既有问题扩边、或治理漂移
   - 推荐后续路由
4. 在 `candidates.md` 中写入或更新 candidate：
   - `title`
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
6. milestone 绑定完成后，必须回写 `candidates.md`：
   - `milestone` 不再允许停留在 `pending://milestone-binding`
   - 若该 candidate 已被接纳进入后续执行面，`status` 更新为 `promoted`
7. 若只是治理问题，允许同步更新治理文档，但不得假装已经进入 dev-loop。

## 不负责

- 不产出正式 issue 目录下的：
  - `issues/{issue}.md`
  - `brainstorms/b-{issue}.md`
  - `prd.md`
  - `pre-tests.md`
  - `tasks.md`
- 不直接进入实现、测试与进度回写

## 状态交换

- 输出给 `auto-loop` / `context-source-skill` 的最小结果应包括：
  - 本轮 candidate 更新摘要
  - milestone 同步结果
  - 是否已形成可进入 `doc-ibm-execution` 的 issue-ready candidate
  - 若阻塞，阻塞原因与下一动作

## 完成

- `brainstorms.md` 与 `candidates.md` 已更新。
- `docs/milestones.md` 与 candidate 状态保持原子一致。
- 当前问题已经被收敛成后续可由 `doc-loop(IBM+G)` 接管的 candidate，而不是悬空问题。
