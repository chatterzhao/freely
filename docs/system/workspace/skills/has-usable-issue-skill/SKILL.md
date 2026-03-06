---
name: has-usable-issue-skill
description: 当当前输入已经命中 usable issue 时，决定进入 doc-loop 还是 dev-loop，并维护 issue-bound 状态一致性。
---

# skill:has-usable-issue-skill

## 适用边界

- milestone、issue、progress 或 recovery 中已经存在可继续执行的 issue。
- 当前回合需要决定进入 `doc-loop-execution` 还是 `dev-loop-execution`。

## 工作流

1. 确认 usable issue 的证据来源：
   - `docs/milestones.md` 的 `committed_issues`
   - 已存在的 issue path
   - 已存在的 progress / recovery 记录
2. 判断该 issue 当前缺口：
   - 若缺少 issue-bound brainstorm、mapping、验收边界、`PRE_TEST` 基线 -> 进入 `skill:doc-loop-execution`
   - 若文档与验收边界已足够，当前主要任务是实现 / 测试 / 回写 -> 进入 `skill:dev-loop-execution`
3. 在进入下一条领域工作流前，确认 milestone 状态一致：
   - ready / committed 的 issue 保持在 `committed_issues`
   - `in_progress` 的 issue 必须能找到匹配的 progress 证据
   - `blocked` 的 issue 必须记录阻塞和下一动作
4. 若 issue 仍需局部脑暴，但边界已经属于既有 issue：
   - 走 issue-bound brainstorm
   - 不回退成新的 pre-brainstorm
5. 领域工作流完成后，把状态回写到 issue / progress / milestone。

## 不负责

- 不直接替代 doc-loop 的产物写作
- 不直接替代 dev-loop 的实现与测试
- 不把已有 issue 无故拆回新的 pre-brainstorm

## 完成

- 当前 issue 已被正确送入 `doc-loop-execution` 或 `dev-loop-execution`。
- 相关 milestone / issue / progress 状态没有分叉失真。
