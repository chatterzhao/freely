# Candidates - 20260403-1200--verification-artifact-dir-repair

## C-20260403-1200-A

- candidate_format_version: `v2`
- title: verification_artifact_dir legacy backfill sub-slice
- status: needs_research
- decision_reason: 该切片是 `C-20260403-1100-A` 的子问题，当前尚未 materialize 成独立 owner issue，不能宣称 promoted。
- promoted_issue_path: `pending://owned-by-c-20260403-1100-a`
- milestone: M-20260306-workspace-routing-foundation
- parent_lane_branch: `feature/governance-chain-legacy-repair-20260403-1100`
- parent_candidate_ref: `C-20260403-1100-A`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: legacy issue 文档缺少 `verification_artifact_dir` 会触发治理链失败，但当前缺口尚未绑定到正式 owner issue。
- why_now: 若不先收敛这类字段缺口，`1100` 主线无法形成稳定、可审计的治理链修复批次。
- acceptance_criteria:
  - 识别并记录缺失 `verification_artifact_dir` 的 issue 样本集合
  - 形成字段值映射规则（issue -> code-reviews directory）并验证不会越权改动其他 front matter
  - 明确该切片将被 `1100` owner issue 吸收，而不是独立 promoted
- promotion_gate:
  - 不放宽 `governance-merge-gate` 规则
  - 不声明不存在的 issue/progress 路径
  - 仅在 `1100` owner issue materialize 后再决定 absorbed 或 promoted 形态
- open_questions:
  - 缺失字段的 issue 列表应由脚本自动导出还是人工基于 gate 输出维护一次清单？
  - 对“无 code-reviews 目录”的 legacy issue，应补目录还是标记为上游治理缺口并剔除本切片范围？
  - absorbed 到 `1100` 时，是否需要为这批 backfill 保留单独 verification note？
- next_action: 在 `1100` 主线下先落正式 owner issue；本切片只维护字段缺口清单与映射规则，等待 owner issue 吸收执行。
- revisit_trigger: 当 `1100` owner issue 路径落盘，或 gate 输出再次出现 `verification_artifact_dir` 缺口时立即重启。
- acceptance_reviews:
  - reviewer: `codex-parent-sync`
  - date: `2026-04-03`
  - result: `needs_research-kept-in-pre-brainstorm`
  - notes: `母链已同步该子切片的治理状态，避免继续引用不存在的 promoted issue。`
