# Candidates

## C-20260612T000223Z-A: A2A 协议替换 Freely Handoff 架构重构

- candidate_format_version: v2
- title: A2A 协议替换 Freely Handoff 架构重构
- status: proposed
- decision_reason: |
  Freely 自举开发中暴露 Handoff 机制缺陷：
  - 大量 launch_failed, launchable check failed
  - Manager 盲目委派导致 Worker 启动失败
  - scan 列表做完就停摆
  A2A 协议提供标准化能力声明、完整状态机、实时推送，可从根本上解决这些问题。
- next_action: 进入 B2_IBM，产出 I-* issue，包含 PRD/pre-tests/tasks/code-review
- revisit_trigger: N/A（已决定推进）
- acceptance_criteria:
  - A2A 协议设计文档完成
  - Agent Card 扩展设计覆盖 Freely 特有概念
  - exit_kind → A2A Task 状态映射完成
  - 原型验证通过 basic handoff 场景
- promotion_gate: |
  - B2_IBM PRD 通过架构评审
  - pre-tests 覆盖核心迁移场景
  - tasks 分解到可执行粒度
- open_questions:
  - Freely Agent Card 如何声明 worktree 隔离能力
  - exit_kind 映射到 A2A Task 状态是否完整
  - SSE 推送是否需要额外的认证机制
  - 外部 Agent 如何通过 A2A 与 Freely 交互
- acceptance_reviews: []
- promoted_issue_path: docs/issues/I-20260612T000223Z-A/issue.md
- milestone: M-20260612T000223Z-A
- session_refs:
  - tool: claude-fable-5
    session_id: current-session
    jsonl_path: unavailable://session-continuity-not-enabled
    role: worker
