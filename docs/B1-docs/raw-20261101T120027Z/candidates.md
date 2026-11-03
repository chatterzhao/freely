---
candidate_id: C-20261101T120027Z-A
status: promoted
source_raw: raw-20261101T120027Z
created_at: 2026-11-01
milestone: M-20261101T120027Z-A
---

# Candidates

## C-20261101T120027Z-A: @freely/dsh-freely DSH 打包形态

- candidate_format_version: v2
- title: 实现 @freely/dsh-freely P1 打包插件
- status: promoted
- decision_reason: DSH 打包是 Freely 的分发形态，不是 Super-agent 对比 candidate；独立 raw/PR 避免和 runtime 重构混在一起。
- next_action: B2 物化 I-20261101T120027Z-A；完成 P1 插件；issue→PR 另开 slice。
- revisit_trigger: DSH 服务 API 跨版本变化、headless/desktop 需要支持、或 E2E 无法在 web profile 跑通。
- acceptance_criteria:
  - 插件加载并创建三角色 preset/session
  - 工具白名单/persona/bridge 可用
  - 插件加载、三 preset/白名单/persona、bridge、gate exit 透传
- promotion_gate: P1 插件/服务注入/spike 通过 + 独立 review + DSH API pin
- b2_acceptance:
  - 插件 web profile 真加载
  - 三 preset/工具白名单/persona
  - freely_status/freely_gate exit code 透传
  - 缺服务 fail-closed
- open_questions:
  - DSH 服务 API 稳定性
  - Python bridge 生命周期
- acceptance_reviews:
  - reviewer: subagent:67b0fffb-4111-44f7-a1c4-f071446af710
  - mode: subagent
  - summary: DSH web profile 加载/session/工具/白名单/gate 已验；API pin/profile 矩阵已补；边界手术后 P1 只留打包插件，判 pass
  - verdict: pass
- promoted_issue_id: I-20261101T120027Z-A
- promoted_issue_path: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T120027Z/issues/I-20261101T120027Z-A.md
- milestone: M-20261101T120027Z-A
- session_refs: []
