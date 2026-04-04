# Candidates - 20260403-1200--verification-artifact-dir-repair

## C-20260403-1200-A

- candidate_format_version: `v2`
- title: verification_artifact_dir legacy backfill sub-slice
- status: `needs_research`
- decision_reason: 该切片已挂接到 materialized parent issue `I-20260403-1100-A`，但 absorbed 还是后续独立 materialize 仍未决，因此不能宣称 promoted。
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
- problem: legacy issue 文档缺少 `verification_artifact_dir` 会触发治理链失败；当前缺口虽然已纳入 `I-20260403-1100-A`，但具体 absorbed 路线仍需继续收敛。
- why_now: 若不先收敛这类字段缺口，`1100` 主线无法形成稳定、可审计的治理链修复批次。
- acceptance_criteria:
  - 识别并记录缺失 `verification_artifact_dir` 的 issue 样本集合
  - 形成字段值映射规则（issue -> code-reviews directory）并验证不会越权改动其他 front matter
  - 明确该切片当前受 `I-20260403-1100-A` 管辖，并记录何时 absorbed 或独立 materialize
- promotion_gate:
  - 不放宽 `governance-merge-gate` 规则
  - 不声明不存在的 issue/progress 路径
  - 仅在 parent routing decision 明确后再决定 absorbed 或 promoted 形态
- open_questions:
  - 缺失字段的 issue 列表应由脚本自动导出还是人工基于 gate 输出维护一次清单？
  - 对“无 code-reviews 目录”的 legacy issue，应补目录还是标记为上游治理缺口并剔除本切片范围？
  - absorbed 到 `1100` 时，是否需要为这批 backfill 保留单独 verification note？
- next_action: 在 `I-20260403-1100-A` 下维护字段缺口清单与映射规则，等待 parent routing decision 明确 absorbed 或独立执行。
- revisit_trigger: 当 `I-20260403-1100-A` 明确本切片的 routing，或 gate 输出再次出现 `verification_artifact_dir` 缺口时立即重启。
- acceptance_reviews:
  - reviewer: `codex-subagent-review`
    verdict: `supports`
    note: `当前保留为 parent-linked needs_research child slice，更符合已 materialized 的 1100 owner truth。`
