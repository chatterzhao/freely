---
candidate_id: C-20260630T002621Z-A
status: promoted
source_raw: raw-20260630T002621Z
created_at: 2026-06-30
milestone: M-20260630T002621Z-A
---

## C-20260630T002621Z-A: 主管持续监督 — Phase 1 cycle 轮询

- candidate_format_version: v2
- title: 主管持续监督 — freely cycle + Worker HALT 协议 + Reviewer 直连
- status: promoted
- decision_reason: 6 个 PR 中 RED 全部糊弄而 Manager 不知。对标 Conveyor cycle + 新增卡点评审。Manager=红绿灯（监控+派 Reviewer），Reviewer=独立评审（fork session，直接对 Worker 发 GO/FIX），Worker=执行+阶段完成主动 HALT。pr-review-guarded 被 per-phase reviewer 替代。pr-merge+wt-close 归 Manager（develop 工位）
- next_action: 进入 B2_IBM → 物化 I-* issue → pre-tests → RED（feature RED = 设计测试确认功能未实现）→ dev → GREEN → PR
- revisit_trigger: Phase 1 完成后评估 SessionReader 可靠性 + Worker HALT 协议稳定性，决定 Phase 2 自动 dispatch
- acceptance_criteria:
  - `freely cycle --raw-key <key>` 检测 a2a blocked → dispatch reviewer
  - Reviewer 语义审核（不靠文件存在性）：检查前置 phase 是否按序完成 + 当前 phase 产出质量
  - Reviewer 直接对 Worker 发 GO/FIX（a2a prompt + state=working）
  - Manager 不检测 phase——phase 语义判断由 Reviewer 负责
  - Worker 每 phase = 一个 ACP prompt，prompt 结束 → a2a blocked → 空闲
  - tool-registry.toml 新增 interrupt_method/resume_method/session_probe
  - pr-merge + wt-close 归 Manager（develop 工位），Worker 管 fix|feature 工位上的所有开发 phase
- promotion_gate: Phase 1 实现 + 真实 Worker session 验证 + pre-tests 全 GREEN + merge
- open_questions:
  - ACP session/prompt 探针注入的可靠性和延迟
  - Worker prompt 注入 HALT 协议的时机（wt-create 时？agent prompt 模板？）
- acceptance_reviews:
  - reviewer: claude
  - mode: in-session
  - summary: B1 预研覆盖现状分析、对标分析（Conveyor/CAO/Superharness）、四个方案对比、分 Phase 交付策略。Phase 1 范围明确（旁观不介入），留有 Phase 2/3 扩展空间
  - verdict: pass
- promoted_issue_path: docs/epics/supervisor-cycle/phase1-cycle-poll/raw-20260630T002621Z/issues/I-20260630T002621Z-A.md
- milestone: M-20260630T002621Z-A
- session_refs: []
