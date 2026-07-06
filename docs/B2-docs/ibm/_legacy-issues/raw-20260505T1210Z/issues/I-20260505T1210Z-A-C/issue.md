---
local_id: I-20260505T1210Z-A-C
issue_title: 'governance gate: platform_state vs phase_state 一致性 + schema 兜底'
kind: linked
phase_state: completed
promoted_from: raw-20260505T121000Z
platform_ids:
  github:
    issue_id: '214'
    url: https://github.com/chatterzhao/freely/issues/214
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/issue-state-refactor/raw-20260505T121000Zissues/I-20260505T1210Z-A-C.md
created_at: '2026-05-05T12:10:02Z'
updated_at: '2026-05-17T08:02:27Z'
session_refs: []
platform_state: closed
---

## Scope

governance-merge-gate 新增 4 条门禁规则：

G1: phase_state=completed 且 platform_state=open → block
G2: phase_state=proposed 且 platform_state=closed → block
G3: platform_state 非空但 platform_ids 为空 → block
S3: phase_state 不在合法集合中 → block

合法值按 kind：
- raw: {proposed, absorbed, dropped}
- I-*: {in_b2_ibm, done_b2_ibm, in_dev, blocked_dev, in_verification, completed}
