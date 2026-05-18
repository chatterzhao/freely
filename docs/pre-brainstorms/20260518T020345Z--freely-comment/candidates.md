# Candidates — 20260518T020345Z--freely-comment

## C-20260518T020345Z-A: 新增 freely comment 命令

- candidate_format_version: v2
- title: 新增 freely comment 命令：封装评论写入 + phase_state 重定向与防御
- status: needs_research
- decision_reason: Raw issue #538 明确提出了对外 CLI 接口需求，复用现有 `_write_chat_to_issue` 基础设施。实现范围小、边界清晰、可独立交付。
- next_action: B2_IBM materialize → 实现 `cmd_comment` 函数 + main dispatch + usage
- revisit_trigger: 若 _write_chat_to_issue 接口变更或 chat-inbox.py materialize-comment API 变化，需同步更新
- acceptance_criteria:
  - `freely comment --issue <raw-xxx|I-xxx> --message <text>` 执行成功
  - `freely comment --issue <raw-xxx|I-xxx> --message-file <path>` 执行成功
  - phase_state=absorbed/dropped + absorbed_into 存在 → 自动重定向到 I-*
  - phase_state=absorbed/dropped + 无 absorbed_into → 拒绝
  - platform_state=closed → 拒绝
  - 消息写入 freely.db → materialize → consume
  - 在 usage 中可见
- promotion_gate: cmd_comment 实现完成、main case 路由就绪、usage 更新
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
    mode: subagent
    summary: B1 research confirmed the freely comment command is well-scoped, reuses existing _write_chat_to_issue infrastructure, and has clear boundaries. Recommend promotion to B2.
    verdict: pass
- promoted_issue_path: ""
- milestone: M-20260518T020345Z-A
- session_refs: []
