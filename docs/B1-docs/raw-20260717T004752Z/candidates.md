---
candidate_id: C-20260717T004752Z-A
status: promoted
source_raw: raw-20260717T004752Z
created_at: 2026-07-16
milestone: M-20260717T004752Z-A
---

# Candidates

## C-20260717T004752Z-A: 监督面观测真源对齐（文档批量 + L240 打点）

- candidate_format_version: v2
- title: 架构文档对齐实现真源 + trace L240 缺口修复
- status: promoted
- decision_reason: 文档系统性落后已在三方审计逐条坐实；L240 为契约自认"必须尽快补齐"的一行缺口；L041/L042 牵涉 monitor 结构以 known-gaps 显式记录。见 brainstorms Option B
- next_action: B2 → RED → dev → GREEN → PR
- revisit_trigger: N/A
- acceptance_criteria:
  - AC1: trace-contract §11 覆盖 runtime 实际打出的全部 checkpoint（脚本提取对照 diff 为空）
  - AC2: heartbeat 机制（SUPERVISOR_HEARTBEAT_TIMEOUT_SECS/2s touch/新生宽限）在 capability-lifecycle 与 watchdog SKILL 有权威描述
  - AC3: task_mode 三态语义 + AI_MODE 区分文档化
  - AC4: bridge 生命周期（lazy/idle/auto-wake/warmup/守卫）与 storm 阈值现值文档化
  - AC5: A-L240 OUT 带 to=A-L010 ok=1（E2E 真实 trace 验证）
  - AC6: AGENTS.md 不再引用不存在的 pre-init-runtime，替代指引可执行
- promotion_gate: 审计 file:line 逐条可考；L240 真实下一跳有当日 trace 实证；scope 不触 monitor 结构
- open_questions: []
- acceptance_reviews:
  - reviewer: inline-audit-crossref
  - mode: inline
  - summary: D1-D6/C7 均出自双 agent 审计与当日实测，无推测项
  - verdict: pass
- promoted_issue_id: I-20260717T004752Z-A
- promoted_issue_path: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T004752Z/issues/I-20260717T004752Z-A.md
- milestone: M-20260717T004752Z-A
- session_refs: []
