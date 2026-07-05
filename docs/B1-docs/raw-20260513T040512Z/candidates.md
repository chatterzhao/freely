# Candidates

## C-20260513T040512Z-A: legacy issue

- candidate_format_version: v2
- title: task-lifecycle-scan 批量化 — 1+3 阶段扫描替代 O(n) API 逐项查询
- status: promoted
- decision_reason: raw-20260513T040512Z12Z (GitHub #327) 提出 task-lifecycle-scan.py 的 O(n) API 性能问题，1+3 阶段批量化方案明确且风险可控
- next_action: B2 materialized, entering dev-loop
- revisit_trigger: B2_IBM 完成 materialize 后重新评估
- acceptance_criteria:
  - Phase 0: `gh issue list --state all --limit 1000` 批量抓取替代逐项查询
  - Phase 1: 本地 vs 平台分类正确（一致/不一致/仅本地）
  - Phase 2: 反向发现 platform_only 的 raw-{key} issue
  - Phase 3: lifecycle chain trace 零 API 调用，仅用本地缓存结果
  - SKIP_PLATFORM_CHECK 移除
  - 扫描总耗时 < 5s（之前 > 2min）
- promotion_gate:
  - B2_IBM materialize 产出 prd.md、pre-tests.md、tasks.md
  - pre-tests 验证 Phase 0 fallback（gh 不可用时回退到逐项查询）
  - code-review 确认与现有 chain trace 输出格式兼容
- open_questions:
  - Phase 0 的 gh issue list --limit 1000 是否足以覆盖当前 repo （当前远未达到，但需确认）
  - Phase 0 失败时的 fallback 行为是否需要可配置
- acceptance_reviews: []
- promoted_issue_path: "docs/issues/I-20260513T040512Z-A/issue.md"
- milestone: M-20260513T040512Z-A
- session_refs:
  - tool: claude-code
  - session_id: 20260519162405-c2dfea
  - jsonl_path: unavailable://session-level
  - role: worker
