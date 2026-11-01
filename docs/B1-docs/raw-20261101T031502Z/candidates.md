---
candidate_id: C-20261101T031502Z-A
status: needs_research
source_raw: raw-20261101T031502Z
created_at: 2026-11-01
milestone: M-20261101T031502Z-A
---

# Candidates

## C-20261101T031502Z-A: 已完成工单的 follow-up ownership 与 handback 协议

- candidate_format_version: v2
- title: 定义 Worker 对已完成工单后续线程的 follow-up ownership 与 handback 协议
- status: needs_research
- decision_reason: 对比发现 Super-agent 用 Subscription + followupOwners + handback 把“同一 Thread 的后续消息归谁处理”做成运行时事实；Freely 的 Worker 没有线程订阅，PR/Issue 后续讨论只能经 Manager/A2A 或重新进入 intake，容易出现重复开单、漏接或上下文断档。该缺口在 agent 协作层，属于 Freely 自身产品架构，值得先做行为盘点再定协议。
- next_action: 先做行为盘点（不改代码）：枚举 PR comment、review、CI、issue comment、chat 插话五类后续消息当前落到 scan 还是 intake；定义 owner 判定、handback 结构、幂等键、超时释放与人工 stop 的优先级；产出协议草案与 pre-tests 设计，再决定是否进入 B2。
- revisit_trigger: 出现同一 PR/Issue 的后续评论被重复开单、被漏接，或 Manager 因中转 follow-up 出现上下文丢失/重复委派时，立即重启本 candidate；若连续两个里程碑未出现该类事件，可降级为观察项。
- acceptance_criteria:
  - 五类后续消息各自有明确的 owner 判定规则，且能回答“这条消息现在归谁”
  - 越界消息只能 handback 一次，并携带理由与目标工单，不产生重复任务
  - 已停止/已关闭工单不会被后续消息自动复活，除非满足显式条件
  - 协议草案给出幂等键与超时释放规则，可用 pre-tests 验证
- promotion_gate: 行为盘点完成 + 协议草案通过 Reviewer 审查 + 至少一个真实后续线程场景的端到端演练通过
- open_questions:
  - follow-up ownership 应落在 A2A task 元数据还是独立的轻量账本
  - 线程订阅的边界是“同一 PR/Issue”还是“同一 raw issue 关联的所有线程”
  - 与人工 stop、wt-close 的优先级如何排序
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 基于 Super-agent `002/003`、`prompts/subscriptions.md` 与 Freely `a2a/*`、`agents/*`、`scan-lifecycle-design.md` 对照，确认缺口真实存在且属于协作层，不是文档表述差异
  - verdict: pass
- promoted_issue_id: pending://C-20261101T031502Z-A
- promoted_issue_path: pending://needs-b2-materialization
- milestone: M-20261101T031502Z-A
- session_refs: []

## C-20261101T031502Z-B: Manager 路由层注意力预算与结构化下派

- candidate_format_version: v2
- title: 度量并约束 Manager 路由层的注意力预算，结构化下派与提问
- status: needs_research
- decision_reason: Super-agent 把 Router 设计成“只分派、不实现、不读代码”，并用结构化 Attention 把人的动作收敛成一个问题；Freely 的 Manager 同时承担 scan、派工、纠偏、收口与人工插话，缺少可检查的“不读实现细节”约束与上下文成本度量，长期看是单点瓶颈。
- next_action: 先度量：统计 Manager 每轮 patrol 注入的 scan/A2A/文档引用体积、读实现的次数、转为 Worker 的指令比例；再定义“Manager 不做实现判断”的可检查边界与结构化 Attention 字段（问题、目标会话、所需动作），用度量结果决定是否改 prompt/skill。
- revisit_trigger: Manager 单轮上下文接近 rotation 阈值、或同一轮同时处理超过 3 个工单导致漏派/错派时，重启本 candidate；若度量显示路由开销占比很低，则本 candidate 降级为观察项。
- acceptance_criteria:
  - 给出 Manager 每轮 patrol 的上下文成本基线（token/字符/文档数）与测量方法
  - 明确 Manager 可以读什么、不可以读什么，并有可检查的 prompt/skill 约束
  - 结构化 Attention 至少包含问题、目标会话、所需人类动作三个字段，且能去重
  - 度量结果能支撑“改”或“不改”的结论，而不是只给建议
- promotion_gate: 基线度量完成 + 边界规则通过 Reviewer 审查 + 一个真实 patrol 周期的对照数据
- open_questions:
  - 上下文成本以字符、token 还是文档数为口径
  - “不读实现细节”应由 prompt 约束还是工具面限制
  - 结构化 Attention 与现有 `input-required` reason 枚举如何合并
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 基于 Super-agent `prompts/orchestrator.md`/`dispatch.md`/`shared.md` 与 Freely `agents/manager-agent.md`、`three-loop` dispatch gate 对照，确认 Manager 职责更宽且缺少成本度量
  - verdict: pass
- promoted_issue_id: pending://C-20261101T031502Z-B
- promoted_issue_path: pending://needs-b2-materialization
- milestone: M-20261101T031502Z-A
- session_refs: []
