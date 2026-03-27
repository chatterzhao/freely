# 候选：prebrainstorm-materialization-audit

- id: `C-20260327-1003-A`
- title: Pre-brainstorm materialization audit and normalization follow-up
- source_brainstorm: `docs/pre-brainstorms/20260327-1003--prebrainstorm-materialization-audit/brainstorms.md`
- status: `candidate`
- adoption_type: `planning_truth`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- decision_reason:
  - 这轮工作的目标是先把 pre-brainstorm 到 milestone / issue 的异常编排面盘清，并区分“只缺状态同步”与“仍需 owner 决策”的条目。
  - 当前已经可以冻结后续治理 lane，但还不适合直接把整份 audit materialize 成单一 issue，因为后续动作会分别回到 milestone reconciliation、pre-brainstorm normalization 与 absorption-or-drop sweep。
  - 因此这里保留为开发治理真源，负责记录异常分类、收口边界与后续 lane。
- scope:
  - 审计 `docs/pre-brainstorms/*` 与 `docs/milestones.md` 的 materialization 漂移
  - 区分 milestone-only gap、normalization drift、partial absorption 与 legacy active debt
  - 给出最小收口方式，避免继续扩大扫描面
- next_action:
  - 先处理纯同步项：回写 milestone 缺口与 pre-brainstorm 字段漂移
  - 剩余条目按 `brainstorms.md` 中定义的 3 个治理 lane 继续推进
- revisit_trigger:
  - 当第 3 / 第 4 类条目需要新的 owner lifecycle，而不是单纯同步状态时，再决定是否 materialize 成独立 issue
