# B1_IBM: raw-key-driven wt-close + issue-sync

## Discovery

wt-close 不清理 companion test-pre-merge 工位，issue-sync close 找不到 platform id 时静默跳过。

## Research

系统所有层都携带 raw-key：工位目录、分支名、raw issue、I-* issue。不需要额外存储关系——raw-key 是通用标识符。

## Decision

wt-close: 从 fix/raw-{key}-{slug} 解析 raw-key，推导 test-pre-merge-{key}-{slug}，存在就关。
issue-sync: 当 platform_ids 为空时，通过 raw-key 搜索 GitHub API，找不到则报错。
