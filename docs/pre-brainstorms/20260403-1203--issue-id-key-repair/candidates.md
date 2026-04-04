# Candidates - 20260403-1203--issue-id-key-repair

## C-20260403-1203-A

- candidate_format_version: `v2`
- title: Add legacy_id_mapping and next_action/revisit_trigger to candidates
- status: needs_research
- decision_reason: 当前子切片尚未 materialize 为 milestone-owned issue，先保留在 pre-brainstorm 并与父治理链绑定，避免伪 promoted。
- promoted_issue_path: `pending://issue-materialization`
- milestone: M-20260306-workspace-routing-foundation
- parent_lane_branch: `feature/governance-chain-legacy-repair-20260403-1100`
- parent_candidate_ref: `C-20260403-1100-A`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: candidate id 与 issue id key 不匹配，且历史候选缺少 `legacy_id_mapping` 与可执行字段；同时本候选此前错误声明 promoted 到不存在的 issue。
- why_now: 分支已完成大量历史补录，但若不修正文档状态会继续制造治理链假阳性与生命周期歧义。
- acceptance_criteria:
  - 历史候选的 `legacy_id_mapping` 补录策略在当前分支有明确边界
  - `needs_research/proposed` 候选具备 `next_action` 与 `revisit_trigger` 基本治理字段
  - 候选状态与产物一致：materialization 前不再宣称 promoted issue
- promotion_gate:
  - 父治理链明确该子切片是 absorbed 还是独立 issue
  - 若独立 materialize，需先创建真实 issue 生命周期文件再切换 promoted
  - 不引入新的治理链断裂
- next_action: 在父治理链 `C-20260403-1100-A` 中确认 legacy 映射策略的长期归属；归属未定前继续以 pre-brainstorm 维护子切片。
- revisit_trigger: 当父治理链进入 issue materialization，或 gate 再次出现 candidate/issue key mismatch 时立即重审。
- open_questions:
  - `legacy_id_mapping` 是否应升级为统一 schema 字段（而非临时补录）？
  - 对已 completed 的历史 candidate，是否需要单独定义“只补录不重开 issue”的标准流程？
- acceptance_reviews:
  - reviewer: `codex-self-review`
  - verdict: `pass-with-fixups`
  - notes: `先修正状态真相并补齐 v2 字段，后续是否独立 issue 由父治理链统一裁决。`
