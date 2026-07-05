# Candidates

## C-20260615T001626Z-A: legacy issue

- candidate_format_version: v2
- title: 移除 A2A 文本 JSON 解析 Fallback (Phase 1+2)
- status: promoted
- decision_reason: |
  父 Epic a2a-replace-handoff 已完成 A2A 协议替换 Handoff 的核心实现。
  当前代码存在双路径（a2a-exit + 文本 JSON 解析 fallback），导致：
  - 两套解析逻辑需要同时维护
  - Prompt 文件需要维护两套指令
  - 行为不一致的风险
  Phase 1+2 修复信号文件 WORKERS 字段并统一所有 Prompt 为 a2a-exit 指令，
  是消除双路径的第一步。
- next_action: 进入 B2_IBM，产出 I-* issue，包含 PRD/pre-tests/tasks/code-review
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - a2a_task.py a2a-exit 写入 WORKERS 到 last-exit-task.env
  - 所有 prompt 文件（manager-agent.md, worker-agent.md, 系统 prompt, repair prompt, delta prompt）已改为 a2a-exit 指令
  - WORKER_STATE_INJECT 中无 JSON block 指令残留
  - FREELY_A2A_TEXT_PARSING_FALLBACK=1 可恢复旧行为
- promotion_gate: |
  - B2_IBM PRD 通过评审
  - pre-tests 覆盖 Phase 1+2 核心场景
  - tasks 分解到可执行粒度
- open_questions:
  - 所有 prompt 文件中 JSON block 指令的完整分布（需要 grep 确认）
  - Phase 2 prompt 变更后对 AI 输出格式的影响评估
  - Phase 3-6 的后续安排
- acceptance_reviews: []
- promoted_issue_path: docs/issues/I-20260615T001626Z-A/issue.md
- milestone: M-20260615T001626Z-A
- session_refs:
  - tool: claude
    session_id: current-session
    jsonl_path: unavailable://session-continuity-not-enabled
    role: worker
