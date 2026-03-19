# 20260318-1825 -- autonomous worktree hygiene and checkpoint supervision

## Context
Freely 自治开发 Freely 自己时，worktree / branch / checkpoint commit 卫生如果失控，会直接导致 manager 无法可靠监督、worker 持续扩写、脏树无法 promote、会话恢复失真。

## Problem
当前仓库虽已有 checkpoint-guard、wt-fleet-status、manager/worker/runtime 分层，但缺一条更强的自治控制面：当 worker 长时间脏树扩张或未及时 checkpoint 时，manager 应如何结构化介入，是否需要专门的 hygiene worker / skill / runtime hook。

## Goals
- 明确 manager / worker / runtime 在 worktree hygiene 与 commit hygiene 上的职责边界。
- 判断是否需要新增专门 agent / skill 来承接 hygiene 监督。
- 若需要，优先做 CLI-first / runtime-first 的可执行能力，而不是聊天提醒。

## Questions
1. 现有 checkpoint-guard + manager supervision alert 为什么还不足以保证持续干净？
2. manager 是否应长期委派一个 hygiene worker，还是由 runtime/hook 在关键节点直接干预？
3. 这条能力应落在 agent、skill、runtime hook、还是多个层次组合？
4. 如何避免提交质量机械化，同时保证坏批次可回滚？

## Candidate directions
- A. 新增 `skill:worktree-hygiene-supervision`，供 manager/worker 共用。
- B. 新增 hygiene worker 角色，由 manager 在 dirty/checkpoint 预警时专门委派。
- C. 强化 runtime hook：当 `checkpoint_required=true` 且连续多轮未收口时，下一轮强制切 `commit/checkpoint/review` 优先级。
- D. 混合方案：runtime 先硬化最小门禁，manager 再在项目级上委派 hygiene worker。

## Initial judgment
倾向 D。仅 skill 太软，仅专门 worker 太晚；需要 runtime/hook 先收紧，再让 manager 有明确 delegation target。
