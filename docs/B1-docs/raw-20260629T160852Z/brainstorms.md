---
b1_id: B1-20260629T160852Z
phase_state: completed
source_raw: raw-20260629T160852Z
source_url: https://github.com/chatterzhao/freely/issues/3628
produced_candidate: C-20260629T160852Z-A
created_at: 2026-06-29
---

# B1_IBM: wt-close 支持 raw-{key} 参数 + help 强调不要传 test 分支

## Input
- 来源：GitHub issue #3628 raw-20260629T160852Z
- kind：fix
- 触发：上一个 issue (#3624) 执行 wt-close 时反复传 test-pre-merge 分支名，未意识到 Phase 6b 已自动处理

## Discovery
- 当前 wt-close 只接受 `<branch>` 参数
- wt-create 用 `--raw-key`，两者 API 不对称
- Phase 6b 已实现 test-pre-merge 自动发现和清理（通过 raw key 匹配）
- 但 help 文案完全没有说明这一点
- 用户和 AI agent 都会自然地去分开关闭 test 工位

## Problem
1. API 不对称：wt-create 传 raw key，wt-close 传 branch name
2. help 缺少关键信息：未说明 test-pre-merge 会自动处理
3. 导致用户浪费时间分开关闭 test 工位

## Brainstorm

### Option A: 只改 help 文案
在 usage() 中加说明"传 fix|feature 分支，test-pre-merge 自动关联清理"

### Option B: 新增 raw-{key} 参数 + 改 help
新增 raw key 输入路径，同时强调分支名不要传 test。与 wt-create 的 --raw-key 对齐。

## Decision: Option B
- 理由：与 wt-create --raw-key 对称，减少认知负担
- raw key 输入内部推导 fix|feature 分支名（复用 `freely_wt_dir_name_for_branch`）
- help 在多处强调"传 fix|feature 分支，test 自动处理"

## Candidate
- candidate_id: C-20260629T160852Z-A
- status: promoted
- milestone: M-20260629T160852Z-A
