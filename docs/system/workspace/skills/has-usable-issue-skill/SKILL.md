---
name: has-usable-issue-skill
description: 当当前输入已经命中 usable issue 时，指挥 issue-bound IBM 或 DDD，确保正式 issue 产物、PRE_TEST 与 milestone/progress 状态一致。
---

# skill:has-usable-issue-skill

## 适用边界

- milestone、issue、progress 或 recovery 中已经存在可继续执行的 issue。
- 当前回合需要判断：
  - 先进入 issue-bound `IBM`
  - 还是继续 `DDD`
- 当前 issue 的后续工作已经不再属于 pre-brainstorm。

## 工作产物

- `docs/milestones.md`
- 正式 issue 产物
- issue-bound `IBM` 产物
- progress / recovery 证据

正式 issue 产物至少包括：

- `docs/epics/{epic}/{story}/issues/{issue-name}.md`
- `docs/epics/{epic}/{story}/brainstorms/b-{issue-name}.md`
- `docs/epics/{epic}/{story}/prd.md`
- `docs/epics/{epic}/{story}/pre-tests.md`
- `docs/epics/{epic}/{story}/tasks.md`

若进入 `DDD`，还会继续维护：

- `src/**`
- `tests/**`
- `docs/progress/{epic}/p-{issue}.md`

## 主事实源

- 一旦命中 usable issue，主事实源从 candidate 切换为 `milestone + issue + progress`
- 本 skill 不再把 candidate 当成执行态事实源
- 后续 brainstorm 若仍需要存在，应属于 `IBM` 的 `B`，即 issue-bound brainstorm，而不是 pre-brainstorm

## 工作流

1. 确认 usable issue 的证据来源：
   - `docs/milestones.md` 的 `committed_issues`
   - 已存在的 issue path
   - 已存在的 progress / recovery 记录
2. 在 issue 边界内判断当前缺口：
   - 若缺少 issue 接入归属、issue-bound brainstorm、mapping、验收边界、`PRE_TEST` 基线 -> 先进入 `skill:doc-loop-execution`
   - 若 issue 文档、`prd`、`pre-tests`、tasks、milestone 映射已足够，当前主要任务是实现 / 测试 / 回写 -> 进入 `skill:dev-loop-execution`
3. 当路由到 `skill:doc-loop-execution` 时，本 skill 负责明确要求 `IBM+G` 至少完成：
   - issue 落位到 `docs/epics/{epic}/{story}/issues/{issue-name}.md`
   - 产出或更新 `docs/epics/{epic}/{story}/brainstorms/b-{issue-name}.md`
   - 产出或更新 `docs/epics/{epic}/{story}/prd.md`
   - 产出或更新 `docs/epics/{epic}/{story}/pre-tests.md`
   - 产出或更新 `docs/epics/{epic}/{story}/tasks.md`
   - 原子同步 `docs/milestones.md`
   - 若该 issue 来自 pre-brainstorm candidate，回写 `candidates.md` 的 `promoted_issue_path` 与状态
4. 当路由到 `skill:dev-loop-execution` 时，本 skill 负责明确要求 `DDD` 至少完成：
   - 读取 issue / prd / pre-tests / tasks
   - 更新 `src/**` 与 `tests/**`
   - 更新 `docs/progress/{epic}/p-{issue}.md`
   - 回写 `docs/milestones.md`
   - 需要时更新 issue 状态与 recovery 证据
5. 在进入下一条领域工作流前，确认 milestone 状态一致：
   - `committed` 的 issue 保持在可扫描队列
   - `in_progress` 的 issue 必须能找到匹配的 progress 证据
   - `blocked` 的 issue 必须记录阻塞原因与下一动作
   - `completed` 的 issue 必须有实现与验证证据
6. 若 issue 仍需局部脑暴，但边界已经属于既有 issue：
   - 走 issue-bound brainstorm，也就是 `IBM` 的 `B`
   - 不回退成新的 pre-brainstorm
   - 不再回写 candidate 执行态
7. 领域工作流完成后，把状态回写到 issue / progress / milestone。

## 不负责

- 不把既有 issue 重新降级成 pre-brainstorm candidate
- 不把 `candidates.md` 当作执行态主事实源
- 不在没有 evidence 的情况下跳过 `pre-tests` / milestone / progress 回写
- 不把已有 issue 无故拆回新的 pre-brainstorm

## 完成

- 当前 issue 已被正确送入 `doc-loop-execution` 或 `dev-loop-execution`。
- 若走 `IBM`，正式 issue 目录与 `pre-tests` 等核心文档已被要求产出或更新。
- 若走 `DDD`，实现、测试、progress 与 milestone 回写要求已明确。
- 相关 milestone / issue / progress 状态没有分叉失真。
- `IBM` 的 `B` 与 pre-brainstorm 的 `brainstorms.md` 已保持边界清晰。
