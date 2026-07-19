---
candidate_id: C-20260719T101009Z-A
status: promoted
source_raw: raw-20260719T101009Z
created_at: '2026-07-19'
milestone: M-20260719T101009Z-A
---
## C-20260719T101009Z-A: 跨base_tool session创建——同tool fork / 不同tool new

- candidate_format_version: v2
- title: 所有agent role的session创建按base_tool匹配选择fork(new)还是new
- status: promoted
- decision_reason: fork的缓存命中是核心价值。同tool才能fork(共享ACP session context), 不同tool必须new。当前Worker和Reviewer两条shell路径都没做这个判断。
- next_action: dev → 修 freely L13264(Worker) + L19137(Reviewer) → test → PR
- acceptance_criteria:
  - Worker和Manager同tool → fork成功
  - Worker和Manager不同tool → ensure worker bridge → session/new
  - Reviewer同理
  - 不改变Python层acp_session_connect(已正确处理)
- promotion_gate: 同tool fork + 不同tool new 均验证通过
- open_questions: []
- acceptance_reviews: [ reviewer: self-review, verdict: pass ]
- promoted_issue_id: I-20260719T101009Z-A
- promoted_issue_path: docs/B2-docs/acp/cross-tool-session/raw-20260719T101009Z/issues/I-20260719T101009Z-A.md
- milestone: M-20260719T101009Z-A
- session_refs: []
