# Candidates - 20260320-2105--status-family-baseline-rename-and-future-aggregation

## Context
- Source brainstorm: ./brainstorms.md
- Status: candidate

## Candidates

### C-20260320T210500Z-A: legacy issue
- title: Baseline-status command and status family governance
- problem: 当前 `freely status` 已经不再代表“当前状态”，而是更像基线/持久快照。与此同时 `live-status` 和 `fleet-status` 已经形成独立状态面，导致 `status` 命名与职责错位。
- why_now: 刚刚新增 `live-status` 后，这个错位已经从轻微变成显性；如果不先把 baseline 语义固定，后续再想把 `status` 做成聚合入口会更容易回退或混淆。
- acceptance_hint:
  - 当前 `freely status` 正式改名为 `freely baseline-status`
  - `freely status` 直接成为 family 聚合入口，支持 `--view baseline|live|fleet|all`
  - 当前活跃技能、README、关键 issue 与测试迁移到 `baseline-status`
  - 文档明确三类状态面的职责：baseline / live / fleet，并把 `status` 作为统一命名空间
- priority: P0
- status: promoted
- decision_reason: 边界已经足够清楚，且刚好处在新增 `live-status` 之后，适合立即收口；继续拖延只会增加历史引用面。
- promoted_issue_path: `docs/B2-docs/ibm/baseline-status-command-and-status-family-governance/issues/baseline-status-command-and-status-family-governance.md`
- next_action: materialize issue，并完成命名迁移、聚合入口与关键测试回归
- revisit_trigger: 若后续需要 JSON family 输出或更细的过滤/排序，再回到同一预研线继续推进
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
