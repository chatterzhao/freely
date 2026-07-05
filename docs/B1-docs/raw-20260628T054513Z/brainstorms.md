---
b1_id: B1-20260628T054513Z
phase_state: completed
source_raw: raw-20260628T054513Z13Z
source_url: https://github.com/chatterzhao/freely/issues/3603
produced_candidate: C-20260628T054513Z-A
created_at: 2026-06-28
---

# B1_IBM: checkpoint-guard scope 硬阻塞 → 建议警告

## Input
- 来源：GitHub #3603

## Problem
pre-commit hook 用 MAX_CHANGED_FILES/MAX_SCOPE_COUNT 做硬阻塞。文件数不能准确反映 scope，逼迫拆分同一问题的修改。

## Brainstorm
### Option A: 保留硬阻塞
拒绝：文件数≠scope 爆炸，行业无先例

### Option B: 改为警告
采纳：不阻塞提交，输出 scope 诊断供开发者评审

## Decision: Option B

## Candidate
- candidate_id: C-20260628T054513Z-A
- status: promoted
- milestone: M-20260628T054513Z-A
