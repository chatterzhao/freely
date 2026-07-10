---
local_id: raw-20260701T051138Z38Z
kind: raw
phase_state: absorbed
absorbed_into: raw-20260701T051138Z38Z
platform_ids:
  github:
    issue_id: '3686'
    url: https://github.com/chatterzhao/freely/issues/3686
    synced_at: ''
  gitee:
    issue_id: IJY1DY
    url: https://gitee.com/zhaoquan/freely/issues/IJY1DY
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-01T05:12:00Z'
updated_at: '2026-07-01T05:12:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n
## 问题

全仓 workflow 流程链表述为：
`feedback → workflow skill → wt-create → B1 → B2 → ...`

但 workflow skill 是流程入口——应该在 feedback 之前加载。改为：
`[skill] workflow → [cmd] feedback → [cmd] wt-create → B1 → B2 → ...`

## 涉及文件（全部）
1. workflow-guarded-execution SKILL.md — 全链路 + L40定位描述 + 阶段0判题
2. dev-loop-execution SKILL.md — 全链路
3. test-execution SKILL.md — 全链路
4. test-RED-execution SKILL.md — 全链路
5. doc-B1_IBM-execution SKILL.md — 全链路
6. doc-B2_IBM-execution SKILL.md — 全链路
7. AGENTS.md — 全链路 + 阶段0表格
