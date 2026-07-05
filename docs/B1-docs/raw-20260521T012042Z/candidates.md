# Candidates

## C-20260521T012042Z-A: legacy issue

- candidate_format_version: v2
- title: Manager keepalive 扫描 launched worker + Worker ACP 初始化超时自愈
- status: promoted
- priority: P1
- source_raw: raw-20260521T012042Z42Z
- decision_reason: 2026-05-20 Runtime Crash Postmortem 暴露两个关联的 worker 生命周期管理缺陷。子问题 1（keepalive 不扫描）有明确修复方向；子问题 2（ACP init 超时）与 C-20260519T015638Z-A 重叠需协调。合并为一个 candidate 因为共享同一代码域且修复链互补。
- next_action: 子问题 1 B2 已完成（见 `docs/B2-docs/stale-pid-keepalive/`），进入 dev 实现；子问题 2 与 C-20260519T015638Z-A 协调研究根因
- revisit_trigger: 子问题 2 的根因研究有结论时重新评估
- acceptance_criteria:
  ### 子问题 1 — keepalive 扫描 launched worker [B2_COMPLETE]
  - [b2_done] Manager keepalive 每次扫描所有 `status=launched` 的 worker
  - [b2_done] 对每个 launched worker 的 PID 执行 `kill -0`（或等价的进程存在检测）
  - [b2_done] `kill -0` 失败 → 标记 `exit_kind=stale_pid` 并更新 handoff DB
  - [b2_done] `kill -0` 成功但 `last_activity_at` 超时 → 交由 `mark_stale()` 现有机制处理
  - [b2_done] 行为不变：正常存活的 launched worker 不被误标记
  - [b2_done] 兼容性：不影响 `consumed`、`blocked`、`completed` 等其他状态
  ### 子问题 2 — Worker ACP 初始化超时自愈 [NEEDS_RESEARCH]
  - ACP bridge 限制并发 session 数，超限时拒绝新连接（而非静默超时）
  - Worker 初始化超时后自动重试或通知 Manager
  - Manager 收到初始化超时信号后主动标记该 worker 失败，不继续空等
  - 与 C-20260519T015638Z-A 的 ACP 超时研究结论一致（若根因相同则吸收到该 candidate）
- promotion_gate:
  - [done] 子问题 1 的 B2 设计完成，包含 manager keepalive 修改点、handoff DB 交互、兼容性分析
  - [ ] 子问题 2 根因判定完成（独立解决或吸收到 C-20260519T015638Z-A）
  - [ ] 与 C-20260519T015638Z-A 的协调结论记录在案
  - [ ] governance-check passes
- b2_deliverables:
  - prd: `docs/B2-docs/stale-pid-keepalive/prd.md`
  - pre-tests: `docs/B2-docs/stale-pid-keepalive/pre-tests.md`
  - tasks: `docs/B2-docs/stale-pid-keepalive/tasks.md`
  - code-reviews: `docs/B2-docs/stale-pid-keepalive/code-reviews/`
- open_questions:
  - Manager 是否有权限访问所有活跃 worker 的 PID？(同用户/同进程组/跨容器)
  - `kill -0` 在 worker 已 zombie 时的行为是否可靠？
  - ACP init 超时的根因到底是 bridge 过载、API 限流还是 Agent 启动失败？
  - 子问题 2 是否应直接吸收到 C-20260519T015638Z-A？取决于根因判定
- overlap / dependency:
  - C-20260519T015638Z-A (systematic stale_pid, gh-601): 研究 worker 在产出 handoff 前退出的根因。子问题 1 互补，子问题 2 重叠需协调。
- acceptance_reviews: []
- promoted_issue_path: "docs/issues/I-20260521T012042Z-A/issue.md"
- milestone: M-20260521T012042Z-A
- session_refs:
  - tool: claude-code
  - session_id: unavailable://session-context-only
  - jsonl_path: unavailable://session-context-only
  - role: worker
