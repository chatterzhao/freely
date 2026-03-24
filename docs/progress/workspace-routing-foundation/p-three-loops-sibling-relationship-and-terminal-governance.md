# Progress: three-loops-sibling-relationship-and-terminal-governance

- issue_id: `I-20260324-0405`
- phase_state: `completed`
- runtime_state: `closed_for_this_batch`
- branch: `feature/three-loops-parallel-relationship-governance-20260324`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-three-loops-parallel-relationship-governance`
- issue_path: `docs/epics/workspace-routing-foundation/three-loops-sibling-relationship-and-terminal-governance/issues/three-loops-sibling-relationship-and-terminal-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}
- summary: 已完成“三个 loop”重构在 active truth、agent/skill、脚本提示词与 runtime-facing contract 中的第一批统一：`auto-loop` 作为 outer orchestration/governance，`doc-loop` / `dev-loop` 作为 sibling execution loops，verification / cleanup / recovery 统一回到 route/phase/governance path；issue 完成，但 worktree 仍待 merge / cleanup / retirement。
- completed:
  - rewrite the active truth set from “三层” wording to “三个 loop”
  - align manager / worker / lead / context-source / auto-loop / watchdog contracts to sibling-loop semantics
  - align script prompt truth and runtime-facing documentation with the sibling-loop model
  - codify supervisor-owned detection of stall, route drift, dead-loop suspicion, and restart-storm escalation
  - preserve historical evidence while limiting edits to active truth
- next:
  - merge this worktree into `develop`
  - continue cleanup / retirement gating before deleting the worktree or branch
