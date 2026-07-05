# Candidates

## C-20260617T011030Z-A: legacy issue

- candidate_format_version: v2
- title: ACP/A2A 架构重构 — 统一 JSON-RPC 协议、事件溯源持久化、跨 AI CLI tool 差异化、ACP↔A2A 状态桥接、Worker A2A 标准化
- status: promoted
- decision_reason: P0 基础架构修复。当前 A2A Server 空转（协议不匹配）、Worker 绕过 A2A、崩溃后状态全丢（无 WAL）、ACP idle timeout 不感知 A2A task 状态。需一次性重构到最标准形态，不复刻、不过渡。
- next_action: B2_IBM → materialize I-* → dev-loop 实现 Phase A→B→C→D → test-pre-merge 验证 → pr-merge-guarded → wt-close
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - A2A: a2a_task.py 全部走 JSON-RPC 2.0，15 处 --db 移除
  - A2A: TaskStore 状态变更 → 异步 db-cli → WAL（不阻塞内存更新）
  - A2A: kill -9 后重启，未完成 task 从 WAL 恢复
  - A2A: freely-db-cli 新增 task-upsert/task-restore/task-list（复用 db_manager）
  - A2A: AgentCard 可通过 /.well-known/agent.json 访问
  - ACP: session/ping 30s heartbeat，10s 超时
  - ACP: stopReason 区分 end_turn / error / idle_timeout
  - ACP: Per-tool system prompt（opencode/claude/codex 差异化委派指引）
  - Bridge: idle timeout 前查内存 TaskStore，有 alive worker 不杀 session
  - Worker: 通过 A2A tasks/send + tasks/push 收发
  - 降级: SQLite 不可用时纯内存运行，WAL 写失败 skip
- promotion_gate: 6 个文件修改完成 + governance-merge-gate 通过 + 单元测试 (JSON-RPC roundtrip, WAL write/read/replay)
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-sonnet-4-6
  - mode: subagent
  - summary: 审查 A2A 协议合规（JSON-RPC 2.0 + AgentCard + TaskStore）、WAL 持久化设计（事件溯源，不阻塞内存）、现有 SQLite 抽象复用（db_manager + db-cli）、ACP state bridge 设计
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260617T011030Z-A/issue.md
- milestone: M-20260617T011030Z-A
- session_refs: []
