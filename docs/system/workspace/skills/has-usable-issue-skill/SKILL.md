---
name: has-usable-issue-skill
description: 当当前输入已经命中 usable issue 时，接入 issue-bound doc-loop(IBM+G)，确保正式 issue 产物、PRE_TEST 与 milestone 状态一致。
---

# skill:has-usable-issue-skill

## 适用边界

- milestone、issue、progress 或 recovery 中已经存在可继续执行的 issue。
- 当前回合需要将该 issue 正式接入或续接到 issue-bound `doc-loop(IBM+G)`。
- 当前 issue 的后续工作已经不再属于 pre-brainstorm。

## 工作产物

- `docs/milestones.md`
- 正式 issue 产物
- issue-bound `IBM` 产物

正式 issue 产物至少包括：

- `docs/epics/{epic}/{story}/issues/{issue-name}.md`
- `docs/epics/{epic}/{story}/brainstorms/b-{issue-name}.md`
- `docs/epics/{epic}/{story}/prd.md`
- `docs/epics/{epic}/{story}/pre-tests.md`
- `docs/epics/{epic}/{story}/tasks.md`

## 主事实源

- 一旦命中 usable issue，主事实源从 candidate 切换为 `milestone + issue`
- 本 skill 不再把 candidate 当成执行态事实源
- 后续 brainstorm 若仍需要存在，应属于 `IBM` 的 `B`，即 issue-bound brainstorm，而不是 pre-brainstorm

## 工作流

1. 确认 usable issue 的证据来源：
   - `docs/milestones.md` 的 `committed_issues`
   - 已存在的 issue path
   - 已存在的 progress / recovery 记录（仅作为 issue 已活跃过的旁证，不改变本 skill 的 doc-loop 归属）
2. 将该 issue 接入或续接到 `skill:doc-loop-execution`。
3. 当进入 `skill:doc-loop-execution` 时，本 skill 负责明确要求 `IBM+G` 至少完成：
   - issue 落位到 `docs/epics/{epic}/{story}/issues/{issue-name}.md`
   - 产出或更新 `docs/epics/{epic}/{story}/brainstorms/b-{issue-name}.md`
   - 产出或更新 `docs/epics/{epic}/{story}/prd.md`
   - 产出或更新 `docs/epics/{epic}/{story}/pre-tests.md`
   - 产出或更新 `docs/epics/{epic}/{story}/tasks.md`
   - 原子同步 `docs/milestones.md`
   - 若该 issue 来自 pre-brainstorm candidate，回写 `candidates.md` 的 `promoted_issue_path` 与状态
4. 在进入 `doc-loop` 前，确认 milestone 状态一致：
   - `committed` 的 issue 保持在可扫描队列
   - `blocked` 的 issue 必须记录阻塞原因与下一动作
   - `completed` 的 issue 不应再次接入本 skill
5. 若 issue 仍需局部脑暴，但边界已经属于既有 issue：
   - 走 issue-bound brainstorm，也就是 `IBM` 的 `B`
   - 不回退成新的 pre-brainstorm
   - 不再回写 candidate 执行态
6. `doc-loop-execution` 完成后：
   - 若 issue 已具备开发条件，由后续循环再进入 `skill:dev-loop-execution`
   - `dev-loop-execution` 是独立技能，不由本 skill 直接替代或吞并
7. 本 skill 完成时，把 issue 接入要求与 milestone 状态要求明确交给 `doc-loop-execution`。

## 不负责

- 不把既有 issue 重新降级成 pre-brainstorm candidate
- 不把 `candidates.md` 当作执行态主事实源
- 不直接决定或执行 `skill:dev-loop-execution`
- 不在没有 evidence 的情况下跳过 `pre-tests` / milestone 回写
- 不把已有 issue 无故拆回新的 pre-brainstorm

## 完成

- 当前 issue 已被正确送入 `doc-loop-execution`。
- 正式 issue 目录与 `pre-tests` 等核心文档已被要求产出或更新。
- 相关 milestone / issue 状态没有分叉失真。
- `IBM` 的 `B` 与 pre-brainstorm 的 `brainstorms.md` 已保持边界清晰。
