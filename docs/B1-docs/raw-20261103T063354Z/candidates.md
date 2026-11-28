---
candidate_id: C-20261103T063354Z-A
status: promoted
source_raw: raw-20261103T063354Z
created_at: 2026-11-03
milestone: M-20261103T063354Z-A
---

## C-20261103T063354Z-A: PR 收尾用配置平台名
- candidate_format_version: v2
- title: 消除 pr-merge 的 unknown: origin 伪错误
- status: promoted
- design_verdict: 实现偏差
- anchor_refs:
  - scripts/sync/platform-adapter.py:916 configured_platforms()
  - scripts/worktree/pr-merge-guarded:490-508 git remote 循环
  - raw-20261103T063354Z 现象原文与两次 merge 回执
- decision_reason: remote 名与 platform 名混用产生伪错误，掩盖真实失败信号。
- acceptance_criteria:
  - RED 证明 baseline 仍按 git remote 调用 close-pr origin。
  - GREEN: 收尾循环使用 adapter configured-platforms，只传 github/gitee 中的非 github 平台。
  - 失败输出结构化告警与可操作重试命令，不再 `|| true` 吞错。
  - 不改 adapter close_pr 语义、不改平台写通道。
- promotion_gate: 实证 unknown: origin 在两次 merge 中复现。
- next_action: 进入 B2 → RED → dev。
- revisit_trigger: 若未来 adapter 支持按 branch 关 PR，再收窄第二参数。
- open_questions: []
- acceptance_reviews:
  - reviewer: main-agent
  - mode: B0-five-layer-audit
  - verdict: pass
- promoted_issue_id: I-20261103T063354Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261103T063354Z/issues/I-20261103T063354Z-A.md
- milestone: M-20261103T063354Z-A
- session_refs: []
