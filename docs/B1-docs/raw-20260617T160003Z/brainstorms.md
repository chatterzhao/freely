# Brainstorm: wt-close --force overwrites pr-merge-guarded frontmatter

## Discovery

### Source
- raw-20260617T160003Z03Z (GitHub #2934)
- 发现方式：收口 fleet 时观察到 develop 变脏，追溯发现 wt-close --force 覆盖了 pr-merge-guarded 的 absorbed frontmatter

### 问题

`2a72b794` (refactor: pr-merge-guarded absorbs wt-close frontmatter — develop never dirty) 将 close frontmatter 写入从 wt-close 移到了 pr-merge-guarded。Merge commit 携带 phase_state=absorbed、force_closed_at、absorbed_into。

但 wt-close Phase 3 (lines 292-306) 的 `--force` 路径从未更新——仍然无条件覆盖 force_closed_at/reason，导致：
1. pr-merge-guarded 的正确信息被覆盖为 "wt-close --force: worktree retired without completed phase_state"
2. develop 残留未提交的 frontmatter 修改

### 影响范围
仅影响 `wt-close --force` 路径。正常 wt-close（不加 --force）不触发 Phase 3，无此问题。

## Research

### 根因
重构时漏掉了 Phase 3 的守卫。Phase 3.5 的注释说 "No local develop commit needed" 但 Phase 3 已经写入了文件。

## Decision

**修复**：Phase 3 执行前检查 phase_state。若已是 "absorbed"（pr-merge-guarded 已处理），跳过写入。

**一行的逻辑改动**，零风险。
