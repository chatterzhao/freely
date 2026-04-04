# Candidates - 20260403-1201--implementation-decision-note-repair

## C-20260403-1201-A

- candidate_format_version: `v2`
- title: implementation decision note legacy backfill sub-slice
- status: `needs_research`
- decision_reason: 该切片已挂接到 materialized parent issue `I-20260403-1100-A`；当前只是 absorbed 或后续独立 materialize 尚未决定，不能标记为 promoted。
- promoted_issue_path: `pending://parent-routing-decision`
- milestone: `M-20260306-workspace-routing-foundation`
- parent_candidate_ref: `C-20260403-1100-A`
- parent_issue_id: `I-20260403-1100-A`
- parent_issue_path: `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: legacy code-review 缺少 implementation decision note 关键字段会触发治理失败；当前缺口已纳入 `I-20260403-1100-A`，但长期 routing 仍未决。
- why_now: 若不先定义补录质量边界，后续批量修复会把 decision note 退化成模板化占位，无法满足 LAWS 对 thoughtfulness 的约束。
- acceptance_criteria:
  - 明确 decision-note 五个必填字段的最小有效内容标准（非空且与变更相关）
  - 给出 legacy review 可补录/不可补录 的判定边界
  - 明确该切片当前受 `I-20260403-1100-A` 管辖，并记录何时 absorbed 或独立 materialize
- promotion_gate:
  - 不放宽 gate 的 decision-note 要求
  - 不声明不存在 issue/progress
  - 仅在 parent routing decision 明确后决定 absorbed 或 promoted
- open_questions:
  - 对历史 review 中“实现已删除或重构”的场景，decision note 应该追溯旧实现还是记录 current-state residual risk？
  - 对纯文档型 review，是否应排除在 decision-note gate 之外，由 owner issue 明确分类？
  - absorbed 后是否需要统一 decision-note 补录模板以减少 reviewer 偏差？
- next_action: 在 `I-20260403-1100-A` 下维护质量边界与样本判定，等待 parent routing decision 决定 absorbed 或独立执行。
- revisit_trigger: 当 `I-20260403-1100-A` 明确本切片的 routing，或 gate 再次报出 decision-note 缺口时立即重启。
- acceptance_reviews:
  - reviewer: `codex-direct-fix`
    verdict: `supports`
    note: `当前保留为 parent-linked needs_research child slice，更符合已 materialized 的 1100 owner truth。`
