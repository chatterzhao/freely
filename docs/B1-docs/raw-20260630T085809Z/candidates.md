---
candidate_id: C-20260630T085809Z-A
status: promoted
source_raw: raw-20260630T085809Z
created_at: 2026-06-30
milestone: M-20260630T085809Z-A
---

## C-20260630T085809Z-A: A2A Server 健康检查修复

- candidate_format_version: v2
- title: 修复 A2A Server 健康检查协议错误、日志轰炸、Shell 注入、超时和日志格式
- status: promoted
- decision_reason: Option A — 改造健康检查为 socket connect 检查，消除协议不匹配根因；同步修复 log suppression / shell injection / timeout / timestamps
- next_action: B2_IBM — 产出 pre-tests.md 和 implementation decision note
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - 健康检查改为 socket 存在性检查（connect 成功 = 就绪），不再发送 HTTP 请求
  - Shell 注入修复：socket 路径通过环境变量 `FREELY_A2A_SOCKET` 传递
  - h11 日志抑制生效：`"h11"` logger 设为 ERROR 级别
  - A2A 启动超时从 10 秒延长到 30 秒
  - A2A Server 日志包含时间戳
- promotion_gate: 修改 freely 脚本 + a2a_server.py，语法验证通过，启动测试无 "Invalid HTTP" 日志
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-code
  - mode: inline
  - summary: 审查 A2A Server 启动日志，确认 44,835 行 Invalid HTTP 根因、122 次崩溃模式、健康检查协议不匹配
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260630T085809Z-A/issue.md
- milestone: M-20260630T085809Z-A
- session_refs: []
