---
candidate_id: C-20261103T111400Z-A
status: promoted
source_raw: raw-20261103T111400Z
created_at: 2026-11-03
milestone: M-20261103T111400Z-A
---

# Candidates

## C-20261103T111400Z-A: open raw 文档物化 + 历史 platform_ids 回填（docs-only）

- candidate_format_version: v2
- title: open issue 本地可追溯 + 历史编号回填
- status: promoted
- decision_reason: 前置 lane 只解决了 open 集合相等与漂移关闭；本地可追溯和编号完整性必须由 docs-only lane 承接，否则 parity 校验（--require-local-docs）持续失败。
- next_action: 物化 13 个 open raw 文档；回填 13 个历史文档；用 `test-platform-open-parity.py --require-local-docs` 验收。
- revisit_trigger: 出现跨 raw key 的代码变更需求时，不可继续用 docs-only lane，需按 issue 拆 lane。
- acceptance_criteria:
  - 13 个 open raw key 均存在 docs/B1-docs/raw-{key}/issue.md，platform_ids.github/gitee 均非空且与平台实际编号一致。
  - 历史编号回填仅在有唯一标题前缀匹配时发生。
  - `test-platform-open-parity.py --require-local-docs` 通过。
  - 变更路径仅 docs/。
- promotion_gate: parity --require-local-docs GREEN + governance skip 合法（纯治理文档）
- open_questions: 无
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 审计 13 个 open key 与 13 个历史编号缺口；确认 GATE 1 阻塞跨 key 文档混入代码 lane，拆 docs-only lane 是唯一合规路径
  - verdict: pass
- promoted_issue_id: I-20261103T111400Z-A
- promoted_issue_path: docs/B2-docs/platform/issue-parity/raw-20261103T111400Z/issues/I-20261103T111400Z-A.md
- milestone: M-20261103T111400Z-A
- session_refs: []
