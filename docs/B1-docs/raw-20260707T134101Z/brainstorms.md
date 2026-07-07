---
b1_id: B1-20260707T134101Z
phase_state: completed
source_raw: raw-20260707T134101Z
produced_candidate: C-20260707T134101Z-A
---
# B1: 平台硬编码清理 + issue-sync 顺序修复
## Discovery: 5 个命令中 8+ 处硬编码
## Decision: 
1. issue-sync commit 后自动 cd test && merge → 消除一致性循环
2. 硬编码 repo 名改为 git remote 动态检测
3. gitee-only loop 改为遍历所有 remote
## Candidate: C-20260707T134101Z-A, promoted
