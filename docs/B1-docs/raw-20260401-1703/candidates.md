# 候选：runtime-adapter-axis-and-per-tool-adapter-selection

- id: `C-20260401-1703-A`
- candidate_format_version: `v2`
- title: Materialize runtime adapter axis and per-tool adapter selection
- source_brainstorm: `docs/B1-docs/raw-20260401-1703/brainstorms.md`
- problem: Freely 已经完成 ACP optional adapter boundary 的研究收口，但当前 runtime 仍没有 first-class `adapter axis`。`AI_TOOL`、tool-specific launch glue、continuity writeback 与 status surface 仍纠缠在一起，导致后续无论是否要接 ACP，都缺少一个安全的最小实现切口。
- why_now:
  - `I-20260401-1545-A` 已明确后续第一刀必须先抽 `adapter axis`
  - 当前 `tool-launchers.sh` 仍主要是 `tool -> launcher case`
  - 如果继续直接做某个工具的 ACP bridge，会把 adapter concern 和 tool concern 再次混层
- acceptance_criteria:
  - 明确 runtime 第一刀 implementation owner 只负责抽出 `adapter axis`，不直接实现 ACP bridge
  - 明确最小 config / launch / status / continuity 触点
  - 明确 current tools 默认仍走 `direct`
  - 明确未实现 adapter 必须 fail fast，不得伪装支持
  - 明确后续 first-tool ACP prototype 依赖本 owner 完成
- promotion_gate:
  - 不改变 Freely continuity / recovery canonical truth
  - 不把 `direct` 降级成临时兼容层
  - 不把 `adapter axis` 和 first-tool ACP bridge 合并成一个 owner
  - 只在 runtime 改动面和 acceptance 已足够清晰时 materialize
- open_questions:
  - `AI_TOOL_ADAPTER` 是否足够作为最小 config truth，还是还需要 `supported_adapters` / `default_adapter` 一起在 tool metadata 冻结
  - fail-fast unsupported adapter 最适合落在 `freely` 还是 `tool-launchers.sh`
  - first-tool ACP prototype 最可能以哪个 current-repo tool 作为后续样本
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The narrowest safe next slice is to extract adapter selection from tool selection while keeping all current tools on direct and failing fast for unsupported adapters.`
    verdict: `promote`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/runtime-adapter-axis-and-per-tool-adapter-selection/issues/runtime-adapter-axis-and-per-tool-adapter-selection.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- expected_outcome:
  - 一个正式 implementation owner，先把 runtime `adapter axis` 从 tool-specific launch glue 中抽出来
  - 一套明确的 issue-level acceptance，用于后续真实代码变更与测试
  - 为 future ACP prototype 准备好不混层的 runtime contract
- decision_reason:
  - ACP boundary 已稳定，继续停留在研究不会再增加信息增益
  - 当前 runtime 的真实阻塞点不是 ACP schema，而是没有 first-class adapter selection
  - 先做 adapter axis extraction，能把后续 direct/acp 双轨接入变成渐进式改造
- next_action:
  - this candidate is now materialized as `I-20260401-1703-A`; the active owner freezes the first implementation slice and prepares runtime/config/status/test touchpoints for dev-loop
- revisit_trigger:
  - re-open candidate-level research only if extracting `adapter axis` proves inseparable from broader runtime governance refactor, or if ACP boundary assumptions change materially
