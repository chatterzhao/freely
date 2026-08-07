---
b1_id: B1-20260807T105604Z
phase_state: completed
source_raw: raw-20260807T105604Z
source_url: https://github.com/chatterzhao/freely/issues/4105
produced_candidate: C-20260807T105604Z-A
created_at: 2026-08-07
---

# B1_IBM: 解除 .codex/config.toml 跟踪

## Input
- raw-20260807T105604Z（GitHub #4105 / Gitee IK7802）
- 现象：`.gitignore:78` 已声明 `.codex/`，但 `.codex/config.toml` 在规则加入前被跟踪；本地个人字段（model/sandbox_mode/approval_policy 等）修改使 develop working tree dirty，daemon start / guarded merge 被 clean-tree 检查拒绝。

## Problem
- 根因不是 clean-tree 检查过严，也不是缺少模板，而是历史遗留的跟踪状态与 `.gitignore` 语义冲突。
- 只补 `.gitignore` 条目（已存在）或加 example 模板都不能解决“文件仍被跟踪”这个根因。

## Brainstorm
### Option A: git rm --cached 解除跟踪（选定）
- 从 index 移除跟踪，本地文件保留；之后 `.codex/` 忽略规则自然生效。
- 不引入新文件、不改运行时、不动 clean-tree 检查，是最小修复。

### Option B: git update-index --skip-worktree
- 只隐藏本地差异，克隆/换机不生效，容易造成“假干净”和误提交。

### Option C: 添加 example 模板并保持跟踪
- 无法解决跟踪本身；模板是额外产品面，超出 cleanup 范围。

### Option D: 放宽 clean-tree 检查忽略 .codex
- 治标不治本，且会扩大运行时检查豁免面。

## Decision: Option A
- 理由：最小、正确、符合 `.gitignore` 语义；只动 git 索引状态，无产品面变化。
- scope：单文件 untrack，不做模板化。

## Candidate
- candidate_id: C-20260807T105604Z-A
- status: promoted
- milestone: M-20260807T105604Z-A
