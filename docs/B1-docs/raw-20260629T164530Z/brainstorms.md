---
b1_id: B1-20260629T164530Z
phase_state: completed
source_raw: raw-20260629T164530Z30Z
source_url: https://github.com/chatterzhao/freely/issues/3632
produced_candidate: C-20260629T164530Z-A
created_at: 2026-06-29
---

# B1_IBM: wt-close --raw-key flag 重构

## Input
- 来源：GitHub #3632 raw-20260629T164530Z30Z
- kind：fix

## Discovery
- 上版 PR #3629 把 raw key 塞在 positional 参数，与 --platform-only 冲突
- --platform-only 无法使用 raw key（因为没分支，raw key 解析失败）
- git branch --list 输出含 `+ ` 前缀未 strip
- have unbound variable `raw_key`

## Decision: --raw-key flag + --branch flag
- 与 --platform-only 等操作模式正交
- 兼容 raw-{key}、fix/raw-{key}-{slug}、feature/raw-{key}-{slug} 输入
- 修复 + 前缀和 unbound variable

## Candidate
- candidate_id: C-20260629T164530Z-A
- status: promoted
- milestone: M-20260629T164530Z-A
