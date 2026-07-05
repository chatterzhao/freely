---
local_id: I-20260513T010343Z-A
kind: linked
phase_state: completed
completed_at: "2026-05-19T23:20:00Z"
absorbed_at: '2026-05-16T14:27:11Z'
platform_ids:
  github:
    issue_id: '326'
    url: https://github.com/chatterzhao/freely/issues/326
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B1-docs/raw-20260513T010343Z/candidates.md
created_at: '2026-05-13T01:03:43Z'
updated_at: '2026-05-17T12:25:53Z'
promoted_from: C-20260513T010343Z-A
source_candidate: docs/B1-docs/raw-20260513T010343Z/candidates.md#C-20260513T010343Z-A
pre_tests_path: ''
verification_artifact_dir: docs/B2-docs/ibm/raw-key-seconds-cleanup/code-reviews/
platform_state: closed
---

# I-20260513T010343Z-A: 秒级 raw key 格式清理

## Implementation Decision Note

- decision: 所有 YYYYMMDDTHHMMZ 改为 YYYYMMDDTHHMM[SS]Z，regex [0-9]{6} → [0-9]{4,6}
- why_this: I-20260507T143545Z-A 的 timestamp-seconds-upgrade 未完成，遗留 14 处
- alternatives_considered: 不改 docs（拒绝：docs 与代码不一致会导致混淆）
- boundary_non_goals: 不改变 raw key 整体格式规范，仅修复遗漏
- residual_risk: 无——只是提升 regex 兼容性 + 修正文档描述
