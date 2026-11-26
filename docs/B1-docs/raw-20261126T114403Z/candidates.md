---
candidate_id: C-20261126T114403Z-A
status: promoted
source_raw: raw-20261126T114403Z
created_at: 2026-11-26
milestone: M-20261126T114403Z-A
---

# Candidates

## C-20261126T114403Z-A: close-orphans 批量模式复用平台读取

- candidate_format_version: v2
- title: 新增 `issue-sync close-orphans --all-completed` 批量入口
- status: promoted
- design_verdict: 实现未完成
- anchor_refs:
  - `docs/system/workspace/commands.md:263`「按 local_id 关闭全部平台副本…失败非零并打印重试命令」
  - `docs/system/workspace/scripts/sync/platform-adapter.py:1308`「This resolver unions the platform truth with the document mapping, so the retirement step and the gate agree on the same set.」
  - `docs/system/workspace/scripts/tests/test-close-orphans-command.py:59-63`「dispatcher registers close-orphans」「retry command is actionable」
- decision_reason: 单 id 入口的副本判据正确但吞吐不足；批量编排仍委托 adapter，保持真源单一。
- next_action: 进入 B2 物化 I-20261126T114403Z-A → RED → dev → GREEN → PR
- revisit_trigger: 若平台读取可零成本复用（例如 daemon 常驻 records 缓存），重新审视批量入口的必要性
- acceptance_criteria:
  - `--all-completed` 模式下 `list_open_issue_records()` 只读一次（stub 计数断言）
  - 仅处理本地 `phase_state ∈ {completed, dropped}` 的文档，非终态不关闭
  - 逐 id 输出 closed/absent/error 汇总，任一平台失败 rc=3 且打印可执行 retry 命令
  - 单 id 模式行为逐字不变（既有 AT 13/13 回归）
  - 与逐 id 模式结果集合差集为空
- promotion_gate: B1 §0 判定为「实现未完成」且外部锚点 ≥2 已引用，candidate 边界不含门禁放宽
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus
  - mode: main-agent
  - summary: B1 §0 广搜确认 adapter 为副本判据唯一真源，批量入口只做编排，不放宽任何终态判据；与 #4687 单 id 入口同族。
  - verdict: pass
- promoted_issue_id: I-20261126T114403Z-A
- promoted_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261126T114403Z/issues/I-20261126T114403Z-A.md
- milestone: M-20261126T114403Z-A
- session_refs: []
