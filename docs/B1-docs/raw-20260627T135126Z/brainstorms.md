---
b1_id: B1-20260627T135126Z
phase_state: completed
source_raw: raw-20260627T135126Z26Z
source_url: https://github.com/chatterzhao/freely/issues/3596
produced_candidate: C-20260627T135126Z-A
created_at: 2026-06-27
---

# B1_IBM: pr-create rebase→merge + checkpoint scope 放行

## Input
- 来源信息: raw-20260627T135126Z26Z (GitHub #3596)
- 症状: 多工位并行时 pr-create Step 3 rebase 反复冲突，checkpoint scope 误拦 git merge develop

## Problem
1. pr-create-guarded 用 `git pull --rebase` 同步 develop。rebase 逐个回放 commit，多工位并行时间一文件（milestones.md）反复冲突
2. checkpoint-guard MAX_SCOPE_COUNT=4。git merge develop 拉入已合并工位文件超限被拦

## Brainstorm

### Option A: 保持 rebase，提高 scope 阈值
- 优点: 改动最小
- 缺点: rebase 历史改写问题依旧，scope 阈值调高治标不治本

### Option B: rebase→merge + merge 时 scope 放行
- 优点: merge 一次解决所有冲突，不改写历史；通过 MERGE_HEAD 检测精准放行
- 缺点: merge commit 可能引入语义冲突（和 rebase 一样，需靠测试兜底）

## Decision: Option B
pr-create 改为 merge 策略，checkpoint 对 merge commit 放行。两处改动共 10 行，影响面小。

## Candidate
- candidate_id: C-20260627T135126Z-A
- status: promoted
- milestone: M-20260627T135126Z-A
