---
local_id: I-20260513T010343Z-A
kind: linked
status: commited
phase_state: in_dev
platform_ids:
  github:
    issue_id: '326'
    url: https://github.com/chatterzhao/freely/issues/326
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/pre-brainstorms/20260513T010343Z--raw-key-seconds-cleanup-followthrough/candidates.md
created_at: '2026-05-13T01:03:43Z'
updated_at: '2026-05-13T01:03:43Z'
promoted_from: C-20260513T010343Z-A
source_candidate: docs/pre-brainstorms/20260513T010343Z--raw-key-seconds-cleanup-followthrough/candidates.md#C-20260513T010343Z-A
pre_tests_path: ''
verification_artifact_dir: 'docs/issues/I-20260513T010343Z-A/verification/'
platform_state: open
---

# I-20260513T010343Z-A: 秒级 raw key 格式清理

## Implementation Decision Note

- decision: 所有 YYYYMMDDTHHMMZ 改为 YYYYMMDDTHHMM[SS]Z，regex [0-9]{6} → [0-9]{4,6}
- why_this: I-20260507T143545Z-A 的 timestamp-seconds-upgrade 未完成，遗留 14 处
- alternatives_considered: 不改 docs（拒绝：docs 与代码不一致会导致混淆）
- residual_risk: 无——只是提升 regex 兼容性 + 修正文档描述
