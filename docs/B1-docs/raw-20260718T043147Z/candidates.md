---
candidate_id: C-20260718T043147Z-A
status: promoted
source_raw: raw-20260718T043147Z
created_at: '2026-07-18'
milestone: M-20260718T043147Z-A
---

## C-20260718T043147Z-A: 将 Worker slot 从 opencode 换为 claude-apikey-ds-pro-auto

- candidate_format_version: v2
- title: 换 Worker ACP slot 修复 initialize 超时
- status: promoted
- decision_reason: opencode acp 是 HTTP server，acp-bridge.py 用 stdio PTY JSON-RPC，协议不兼容导致 initialize 永远超时。最小修复是换为 stdio-based claude ACP tool。
- next_action: B2 物化 I-* issue → dev（修改 agent-table.toml） → 验证 worker bridge 可正常 initialize
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - agent-table.toml 的 worker_slot 从 opencode-apikey-ds-flash-auto 改为 claude-apikey-ds-pro-auto
  - daemon 重启后 worker ACP bridge initialize 成功（无超时错误）
  - Manager 可以成功委派至少一个 Worker（worker task 从 submitted → working）
- promotion_gate: agent-table.toml 改动完成，且 worker bridge initialize 验证通过
- open_questions: []
- acceptance_reviews:
  - reviewer: self-review（根因明确，方案最小可验证，无需外部 reviewer）
  - mode: inline
  - summary: 根因通过手动测试 opencode acp 行为确认。修复方案为最小单行配置变更，无代码风险。
  - verdict: pass
- promoted_issue_id: I-20260718T043147Z-A
- promoted_issue_path: docs/B2-docs/config/toml-parsing-robustness/raw-20260718T043147Z/issues/I-20260718T043147Z-A.md
- milestone: M-20260718T043147Z-A
- session_refs: []
