---
candidate_id: C-20260628T005815Z-A
status: promoted
source_raw: raw-20260628T005815Z
created_at: 2026-06-28
milestone: M-20260628T005815Z-A
---

## C-20260628T005815Z-A: chat 重构 — comment + discuss + archive skill

- candidate_format_version: v2
- title: 将 freely chat 拆分为 comment（评论）和 discuss（讨论），新增讨论归档 skill
- status: promoted
- decision_reason: 三种互不兼容的场景合并在一个 chat 命令里共享本地 DB，导致评论延迟、讨论无法结构化、入口混淆。拆分为独立命令各自走最合适的存储路径。
- next_action: 进入 B2_IBM → 实现设计 → dev-loop 开发
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - comment: freely comment --issue raw-{key} 直写所有平台，本地不留，成功后通知活跃工位
  - discuss: freely discuss 新建/继续 session，群聊 @ 引用，本地 DB + 平台 Discussions 同步
  - discuss agent: agent-table.toml 配置 discuss_slot + pool=1，使用新讨论执行 skill
  - archive skill: freely discuss --archive 手工触发，分析讨论 → comment 或 feedback 创建 raw issue
  - 讨论关闭: 导出成功后关闭平台 Discussions + 本地 platform_state: closed
  - close issue 拒绝: comment 对已关闭 issue 直接拒绝
  - 门禁: pr-create-guarded / wt-close 全平台检查未处理评论
  - 跨平台同步: SHA256 去重 + adapter 补建 + AI 语义合并差异
  - 旧 chat 拆除: --issue → comment, --conversation → discuss, chat-inbox materialize 删除
- promotion_gate: B2_IBM 完成，设计评审通过，实现方案完整可执行
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.8
  - mode: plan-subagent
  - summary: 审查 chat 拆分设计，验证 comment/discuss/export 三模块边界清晰，平台兼容策略合理
  - verdict: pass
- promoted_issue_path: docs/epics/chat-refactor/issues/I-20260628T005815Z-A.md
- milestone: M-20260628T005815Z-A
- session_refs: []
