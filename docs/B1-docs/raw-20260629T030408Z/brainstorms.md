---
b1_id: B1-20260629T030408Z
phase_state: completed
source_raw: raw-20260629T030408Z
source_url: https://github.com/chatterzhao/freely/issues/3617
produced_candidate: C-20260629T030408Z-A
created_at: 2026-06-29
---

# B1_IBM: 完成 feat → feature 重命名

## Input
- 来源: raw-20260629T030408Z (GitHub #3617, Gitee IJXH5I)
- 之前的重命名 (raw-20260625T235017Z) 将 skill 名从 `freely-feat-execution` 改为 `freely-feature-execution`，但不彻底

## Problem
- wt-create 仍校验 `freely-feat-execution`，拒绝 `freely-feature-execution`
- 7 个活跃脚本 + 2 个 hook 文件 + AGENTS.md 仍引用旧名
- 用户创建 feature 工位时被拒："Invalid --skill 'freely-feature-execution'"

## Brainstorm
### Option A: 回退到 feat
- 放弃，已明确 feature 是更好的命名（三字母 feat 与 fix 易混淆）

### Option B: 完成重命名
- 全局搜索替换 `freely-feat-execution` → `freely-feature-execution`
- AGENTS.md `feat:` → `feature:`
- 8 个活跃代码文件，17 处引用

## Decision: Option B
- 改名已完成大半，回退成本更高
- 仅剩 8 个文件未更新，改动范围可控
- 纯字符串替换，无逻辑变更

## Candidate
- candidate_id: C-20260629T030408Z-A
- status: promoted
- milestone: M-20260629T030408Z-A
