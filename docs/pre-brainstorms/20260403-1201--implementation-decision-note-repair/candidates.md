# Candidates - 20260403-1201--implementation-decision-note-repair

## C-20260403-1201-A

- candidate_format_version: `v2`
- title: implementation decision note legacy backfill sub-slice
- status: needs_research
- decision_reason: 该切片仍是 `C-20260403-1100-A` 的子问题；当前不存在 materialized owner issue，不能标记为 promoted。
- promoted_issue_path: `pending://owned-by-c-20260403-1100-a`
- milestone: M-20260306-workspace-routing-foundation
- parent_lane_branch: `feature/governance-chain-legacy-repair-20260403-1100`
- parent_candidate_ref: `C-20260403-1100-A`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: legacy code-review 缺少 implementation decision note 关键字段会触发治理失败，但该缺口尚未绑定到正式 owner issue。
- why_now: 若不先定义补录质量边界，后续批量修复会把 decision note 退化成模板化占位，无法满足 LAWS 对 thoughtfulness 的约束。
- acceptance_criteria:
  - 明确 decision-note 五个必填字段的最小有效内容标准（非空且与变更相关）
  - 给出 legacy review 可补录/不可补录 的判定边界
  - 明确该切片将由 `1100` 主线 owner issue 吸收，不再声称当前已 promoted
- promotion_gate:
  - 不放宽 gate 的 decision-note 要求
  - 不声明不存在 issue/progress
  - 仅在 `1100` owner issue materialize 后决定 absorbed 或 promoted
- open_questions:
  - 对历史 review 中“实现已删除或重构”的场景，decision note 应该追溯旧实现还是记录 current-state residual risk？
  - 对纯文档型 review，是否应排除在 decision-note gate 之外，由 owner issue 明确分类？
  - absorbed 后是否需要统一 decision-note 补录模板以减少 reviewer 偏差？
- next_action: 等待 `1100` owner issue 落盘；在此之前仅维护质量边界与样本判定，不独立推进 promoted lifecycle。
- revisit_trigger: 当 `1100` owner issue 路径落盘，或 gate 再次报出 decision-note 缺口时立即重启。
- acceptance_reviews:
  - reviewer: `codex-direct-fix`
  - date: `2026-04-03`
  - result: `needs_research-kept-in-pre-brainstorm`
  - notes: `已移除不存在 promoted issue 的声明，并显式挂接到 1100 母链。`
