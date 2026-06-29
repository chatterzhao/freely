---
issue_id: I-20260629T164530Z-A
issue_path: docs/epics/wt-close-raw-key/raw-key-flag/raw-20260629T164530Z/issues/I-20260629T164530Z-A.md
phase_state: done_b2_ibm
---
- issue_id: I-20260629T164530Z-A
## Implementation Decision Note
- decision: 用 --raw-key/--branch flag 替代 positional 参数，_extract_raw_key 用 grep -oE 精确提取
- why_this: 与 wt-create --raw-key 对齐，与 --platform-only 等 flag 正交
- alternatives_considered: positional 参数已证明与 flag 冲突
- boundary_non_goals: 不改变 Phase 1-7 核心流程
- residual_risk: 低，grep -oE 精确匹配 raw key 格式
