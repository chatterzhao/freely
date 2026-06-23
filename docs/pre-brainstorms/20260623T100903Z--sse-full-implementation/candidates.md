# Candidates

## C-20260623T100903Z-A: 彻底实现 SSE — SSE 客户端 + 替代轮询 + 废弃 delivery_status

- candidate_format_version: v2
- title: 彻底实现 SSE：SSE 客户端 + 替代轮询 + 废弃 delivery_status + Manager 实时决策闭环 + _restore_tasks 修复
- status: promoted
- decision_reason: #3381 完整分析（14 条评论）的最终结论——SSE 缺失是当前 5/6 问题的中枢。实现 SSE 客户端后 delivery_status 列可删除、79 条 stale pending 消失、Manager 的 review→pass/fail→complete/redelegate 决策闭环能正常运行。5 阶段递进方案（客户端基础→双写过渡→废弃轮询→服务端修复→文档验证）确保每阶段可独立验证，双写过渡期提供安全网。
- next_action: 进入 B2_IBM → 产出 PRD（5 阶段设计详案）+ pre-tests + tasks + code-review → milestone → dev-loop 实现
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - 阶段 1：a2a_task.py `stream_task()` 可连接 SSE 端点、解析 TaskStatusUpdateEvent/TaskArtifactUpdateEvent、处理 stream close、支持 resubscribe 重连
  - 阶段 1：连接池最多 10 并发，有心跳和指数退避重连
  - 阶段 2：Manager 通过 SSE 事件队列收到 Worker 状态变更，双写过渡期间 SSE 和轮询结果一致
  - 阶段 3：delivery_status 列和相关代码完全移除，79 条旧记录一次性迁移完成
  - 阶段 3：list-pending-delivery 调用、after_run delivery 标记代码、PENDING_DELIVERY_COUNT 全部移除
  - 阶段 4：_restore_tasks() 改为恢复 SSE 订阅 + 进程 liveness 检查（死进程标记 failed）
  - 阶段 4：filesystem_fallback 加 [DEPRECATED] 注释 + warn 日志
  - 阶段 5：manager-agent.md 移除 "curl -N 后台运行"，替换为 "SSE 自动推送"
  - 阶段 5：端到端验证通过——daemon start → Manager SSE 监督 Worker → Worker 完成 → Manager decision loop 正常运行
- promotion_gate:
  - brainstorms.md 完成（discovery → research → decision）✅
  - 5 阶段方案有明确的依赖和验证标准 ✅
  - 独立 acceptance review 通过 ✅
  - 无 open_questions ✅
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.8
  - mode: subagent
  - summary: 审查 #3381 全部 14 条评论，确认 SSE 缺失是所有问题中枢的结论正确。验证 5 阶段方案覆盖所有 SSE 直接关联点（客户端、轮询替代、delivery_status 废弃、_restore_tasks 修复、filesystem_fallback deprecated）。确认 A2A 协议标准对齐。双写过渡方案提供安全网，风险可控。
  - verdict: pass
- promoted_issue_path: docs/epics/sse-full-implementation/issues/I-20260623T100903Z-A.md
- milestone: M-20260623T100903Z-A
- session_refs:
  - tool: claude-code
  - session_id: ses_10db3c52bffeGN8LMZ4sJ03H7f
  - role: manager/analyst
  - analysis_issue: https://github.com/chatterzhao/freely/issues/3381
  - followup_issue: https://github.com/chatterzhao/freely/issues/3388
