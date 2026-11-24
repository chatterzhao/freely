---
candidate_id: C-20261124T054217Z-A
status: promoted
source_raw: raw-20261124T054217Z
created_at: 2026-11-24
milestone: M-20261124T054217Z-A
---

## C-20261124T054217Z-A: issue-sync update 失败传播
- candidate_format_version: v2
- title: 汇总双平台写结果，部分失败非零退出
- status: promoted
- design_verdict: 实现缺陷
- anchor_refs:
  - `cmd-update.sh:32`「_gitee_update ... || echo FAILED」+ `:35` echo complete
  - 宪法 fail-closed / 双平台一致性原则
- decision_reason: Option B，双平台都检查返回值并汇总，任一失败非零退出。
- next_action: B2 物化；改 cmd-update；AT 覆盖。
- revisit_trigger: 若平台写统一迁入 adapter 的批量结果接口，重新评估。
- acceptance_criteria:
  - Gitee 写失败 → 命令非零退出且输出含 partial_failure 汇总
  - GitHub 写失败 → 同样非零（不只 Gitee）
  - 双平台成功 → 输出与当前一致（含 update complete）
  - 不重复写、不重试
- promotion_gate: 改动面有 RED 设计；不改其它平台写命令。
- open_questions: []
- acceptance_reviews:
  - reviewer: self-b1-audit
  - mode: structured-check
  - summary: B0 判定、三方案对比与锚点一致。
  - verdict: pass
- promoted_issue_id: I-20261124T054217Z-A
- promoted_issue_path: docs/B2-docs/gate/platform/raw-20261124T054217Z/issues/I-20261124T054217Z-A.md
- milestone: M-20261124T054217Z-A
- session_refs:
  - tool: codebuddy-agent
  - session_id: unavailable://current-session
  - jsonl_path: unavailable://current-session
  - role: worker
