---
candidate_id: C-20261124T054201Z-A
status: promoted
source_raw: raw-20261124T054201Z
created_at: 2026-11-24
milestone: M-20261124T054201Z-A
---

## C-20261124T054201Z-A: test-all 失败诊断

- candidate_format_version: v2
- title: test-all 失败时保留并打印测试输出
- status: promoted
- design_verdict: 实现缺陷（设计正确）
- anchor_refs:
  - `bin/test-all:2-4`「Runs the verified subset … prints explicit known-broken list」
  - `CONSTITUTION.md:39`「进入 develop 前必须满足要求的 TEST … 证据」
  - CI run 43827151395 / 45346477702 的 `[FAIL]` 无断言输出
- decision_reason: Option B。成功摘要、失败留完整日志 + artifact，符合 AI 自愈且保持门禁契约。
- next_action: B2 物化 I-*；改 test-all 执行循环保留失败输出，新增 AT 验证。
- revisit_trigger: 若 SUMMARY 行格式下游依赖变化，重新审视输出结构。
- acceptance_criteria:
  - 失败测试的断言信息出现在 CI 输出中（非仅 `[FAIL]`）
  - 每个测试有独立日志；失败日志可预测路径便于 artifact 上传
  - 成功时输出与 SUMMARY 行格式不变（下游门禁不退化）
  - 记录退出码与耗时
- promotion_gate: 改动面有 RED 设计，不改门禁判据。
- open_questions: []
- acceptance_reviews:
  - reviewer: self-b1-audit
  - mode: structured-check
  - summary: B0 判定、三方案对比、Option B 决策与锚点一致。
  - verdict: pass
- promoted_issue_id: I-20261124T054201Z-A
- promoted_issue_path: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261124T054201Z/issues/I-20261124T054201Z-A.md
- milestone: M-20261124T054201Z-A
- session_refs:
  - tool: codebuddy-agent
  - session_id: unavailable://current-session
  - jsonl_path: unavailable://current-session
  - role: worker
