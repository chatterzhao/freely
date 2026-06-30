---
b1_id: B1-20260630T095936Z
phase_state: completed
source_raw: raw-20260630T095936Z
source_url: https://github.com/chatterzhao/freely/issues/3649
produced_candidate: C-20260630T095936Z-A
created_at: 2026-06-30
---

# B1_IBM: dev↔test consistency check — cherry-pick → git merge

## Input
- raw issue: `docs/issues/raw-20260630T095936Z/issue.md`
- 发现方式: PR #3648 开发过程中触发死锁

## Discovery — 问题验证

### 观测事实
1. `freely_wt_assert_dev_test_consistent()` 在两个方向上都提示用户用 `git cherry-pick` 同步
2. `reference-transaction` hook 把 `test-pre-merge-*` 视为保护分支，阻止 cherry-pick（非 merge commit 缺少 Freely-Merge-Path）
3. 系统形成死锁：提示 cherry-pick → hook 阻止 → 用户无从下手
4. test→dev 方向的 cherry-pick 提示是危险的：测试工位是丢弃式沙箱，不应有独立提交回流到开发工位
5. 用 `git merge --no-ff` + `Freely-Merge-Path: pr-merge-guarded` 可以绕过 hook，是正确做法（PR #3648 已验证）

### 时效性判断
- 当前仍在发生（上一轮 PR 触发）
- 直接影响开发者体验
- **结论: 值得投入修复**

## Problem — 根因分析

根因：consistency check 编写时假定 cherry-pick 可行，但 hook 在后续版本中强化了 test-pre-merge 保护，提示未同步更新。

## Brainstorm — 方案

### Option A: 改提示文本（最小改动）
- dev→test: cherry-pick → git merge --no-ff + Freely-Merge-Path
- test→dev: cherry-pick → 硬拒绝 + 正确流程指引
- 不改变检查逻辑，只改错误消息

### Option B: 改 hook 放宽 test-pre-merge
- 让 test-pre-merge 接受 cherry-pick
- 缺点: 破坏保护语义，test-pre-merge 不应接受非 merge 提交

## Decision: Option A
- 不改 hook 保护语义
- 提示文本与实际可行的操作对齐
- test→dev 方向硬拒绝，防止测试工位污染开发工位

## Candidate
- candidate_id: C-20260630T095936Z-A
- status: promoted
- milestone: M-20260630T095936Z-A
