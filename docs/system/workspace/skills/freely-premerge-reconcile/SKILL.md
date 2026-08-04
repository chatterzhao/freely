---
name: freely-premerge-reconcile
description: >-
  在不回退治理的情况下协调高风险合并冲突。从 test-pre-merge-* 创建
  临时 premerge 分支，按语义意图解决冲突后合并回测试批次并清理。

  Use when: test-pre-merge-* 合并失败或出现语义回归风险。
  触发词："合并冲突"、"premerge"、"语义回归"、"reconcile"。
---

# skill:freely-premerge-reconcile

## 触发条件
- 正常合并到某个 `test-pre-merge-*` 批次因高冲突文件失败。
- 冲突解决后有策略回退风险。

## 前置条件
- 从当前活跃的 `test-pre-merge-*` 批次开始。
- 创建专用分支：
  - `git branch feature/premerge-YYYYMMDDTHHMM[SS]Z--<topic> <active-test-pre-merge-branch>`
  - `cd <your-project-path>`
  - 优先：`freely wt-create feature/premerge-YYYYMMDDTHHMM[SS]Z--<topic> --base <active-test-pre-merge-branch>`
  - 手工兜底：`git worktree add ../<your-project-worktrees>/<branch-dir> feature/premerge-YYYYMMDDTHHMM[SS]Z--<topic> && freely sync-tooling --source-project <your-project-path> --project ../<your-project-worktrees>/<branch-dir>`
  - `cd ../<your-project-worktrees>/<branch-dir>`
  - 对 `feature/premerge-20260307T1015Z--topic`，`<branch-dir>` 应为 `20260307T1015Z-feature-premerge-topic`

## 工作流
1. 通过受控集成协调：
   - 将需要的提交 merge 或 cherry-pick 到 `feature/premerge-*`
   - 以语义优先决策解决冲突
2. 对每个冲突，遵循 `references/conflict-decision-template.md`。
3. 在此分支上运行最小回归。
4. 仅合并回原测试批次：
   - `git checkout <active-test-pre-merge-branch>`
   - `git merge --no-ff feature/premerge-...`
5. 通过 `skill:freely-branch-management` 检查清单运行语义回归检查。
6. 清理：
   - 删除 premerge 分支和 worktree
   - 在进度/恢复笔记中记录结果。

## 冲突规则
- 优先与当前宪法/法律的语义兼容性。
- 如旧结构与当前治理冲突，保留治理并调整旧内容。

## 完成
- 原 `test-pre-merge-*` 批次包含协调后的变更。
- 回归检查通过。
- Premerge 分支/worktree 已删除。
