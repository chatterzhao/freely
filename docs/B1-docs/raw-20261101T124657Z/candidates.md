---
candidate_id: C-20261101T124657Z-A
status: promoted
source_raw: raw-20261101T124657Z
created_at: 2026-11-01
milestone: M-20261101T124657Z-A
---

# Candidates

## C-20261101T124657Z-A: dsh-freely issue→PR E2E slice

- candidate_format_version: v2
- title: 确定性 Manager→Worker→Reviewer→gate→PR E2E
- status: promoted
- decision_reason: P1 已证明插件可加载；本 slice 只补全链路证据，不重复打包插件。
- next_action: B2 物化 I-A；实现 e2e driver + 真实 DSH profile 验证；走本 slice PR/merge。
- revisit_trigger: DSH 服务 API 变化、Worker/Reviewer preset 不能在同一 profile 共存、或 gate 无法在 E2E repo 跑。
- acceptance_criteria:
  - Manager session 由 P1 插件创建
  - Worker 在临时 repo 写文件并 commit
  - Reviewer 读 diff 给 verdict
  - pretests-gate 有真实 exit code
  - 全程无 ACP；不加载 dsh-superagent
  - 本 slice 走真实 PR/merge
- promotion_gate: B1 边界收敛 + P1 已 merge + DSH 0.2.1-rc.5 web 可用
- b2_acceptance:
  - e2e driver 测试绿
  - 真实 DSH profile 输出 result JSON
  - 本 slice PR
- open_questions:
  - Reviewer verdict 的机器可判定格式
  - Worker/Reviewer 是否能在同一 DSH profile 同时挂载
- acceptance_reviews:
  - reviewer: subagent:14247d38-8cb6-484c-960e-93a66ac8044f
  - mode: subagent
  - summary: 确定性 driver；真实 DSH committed/verdict/gate 0；修 blocker 后复评 pass。
  - verdict: pass
- promoted_issue_id: I-20261101T124657Z-A
- promoted_issue_path: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T124657Z/issues/I-20261101T124657Z-A.md
- milestone: M-20261101T124657Z-A
- session_refs: []
