---
candidate_id: C-20261102T130603Z-A
status: promoted
source_raw: raw-20261102T130603Z
created_at: 2026-11-03
milestone: M-20261102T130603Z-A
---

# Candidates

## C-20261102T130603Z-A: 平台 handler 探活缓存、重试与 execute 阶段结构化失败

- candidate_format_version: v2
- title: 修复 handler 探活抖动导致的 AttributeError
- status: promoted
- decision_reason: `_handler_for` 每次做网络探活且失败返回 None，execute 阶段无守卫直接解引用；一次 PR 流程多次调用既慢又随机失败。缓存成功探活 + `_retry_read` 重试 + execute 阶段 `_ensure_handler` 结构化失败，是最小且可单测的修法。
- next_action: B2 物化 I-20261102T130603Z-A；先写 RED 单测（缓存/重试/结构化错误），再改 platform-adapter。
- revisit_trigger: 若平台探活语义变化（如支持离线判定）需重新评估缓存策略。
- acceptance_criteria:
  - 同一进程内连续 10 次取同一平台 handler 只触发 1 次 detect。
  - 第一次 detect 返回失败、第二次成功时仍返回 handler（有界重试生效）。
  - handler 不可用时 `_ensure_handler` 返回结构化 error，不抛异常。
  - 既有 adapter/PR 流程测试不回归。
- promotion_gate: RED→GREEN + 既有测试全绿 + governance-merge-gate 通过
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 读 _handler_for/_discover_one/guarded_pr_update 与 raw issue 复现记录，确认 execute 阶段无 None 守卫
  - verdict: pass
- promoted_issue_id: I-20261102T130603Z-A
- promoted_issue_path: docs/B2-docs/platform/platform-handler-probe/raw-20261102T130603Z/issues/I-20261102T130603Z-A.md
- milestone: M-20261102T130603Z-A
- session_refs: []
