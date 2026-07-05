---
b1_id: B1-20260629T163137Z
phase_state: completed
source_raw: raw-20260629T163137Z
produced_candidate: C-20260629T163137Z-A
---
# B1_IBM: pr-review-guarded fixes
## Problem
1. 从 develop 跑时 I-* 文件搜不到 → review 路径 fallback 到共享目录
2. ACP 检测在 freely-review 之后，静默失败
## Decision
1. I-* 搜索用 _wt_path（fix worktree）先于 ROOT_DIR
2. ACP 检测提到 freely-review 之前
## Candidate: C-20260629T163137Z-A promoted → M-20260629T163137Z-A
