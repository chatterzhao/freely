# Candidates - 20260403-1202--candidate-touched-repair

## C-20260403-1202-A

- candidate_format_version: `v2`
- title: Fix issue reference format in review files
- status: needs_research
- decision_reason: 该子切片尚未 materialize 为 milestone-owned issue，先保持在 pre-brainstorm 阶段并绑定父治理链，避免伪造 promoted 状态。
- promoted_issue_path: `pending://issue-materialization`
- milestone: M-20260306-workspace-routing-foundation
- parent_lane_branch: `feature/governance-chain-legacy-repair-20260403-1100`
- parent_candidate_ref: `C-20260403-1100-A`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: review 文件使用了混合 issue 字段（`issue:` vs `issue_id:`），且本候选之前错误地声明为已 promoted，导致治理链语义失真。
- why_now: 当前 worktree 已完成字段修复改动，但生命周期仍缺少合法 owner 锚点；必须先修正文档真相，避免把子切片误当独立已落地 issue。
- acceptance_criteria:
  - review 文档中的 issue 标识字段使用统一命名（`issue_id`）
  - 候选状态与物理产物一致：不存在的 issue 路径不再被标记为 promoted
  - 子切片与 `C-20260403-1100-A` 的关系在文档里可追溯
- promotion_gate:
  - 父治理链明确该子切片的落位策略（absorbed 或独立 materialize）
  - 若独立 materialize，必须先创建真实 `issue/prd/pre-tests/tasks` 再改 `status: promoted`
  - 不引入新的治理链断裂
- next_action: 在父治理链 `C-20260403-1100-A` 中确认该子切片的归属策略；确认前仅维护 pre-brainstorm 级事实，不新增伪 issue 引用。
- revisit_trigger: 当父治理链开始正式 issue materialization，或 gate 再次报出 review issue 字段回归时立即重审。
- open_questions:
  - 该子切片应被吸收到单一 `governance-chain-legacy-repair` owner，还是拆分为独立 owner issue？
  - legacy 文档允许长期保留 `issue` 别名，还是必须全量迁移为 `issue_id`？
- acceptance_reviews:
  - reviewer: `codex-parent-sync`
  - verdict: `pass-with-fixups`
  - notes: `母链已同步该子切片的治理状态，后续是否独立 owner 仍由父治理链统一裁决。`
