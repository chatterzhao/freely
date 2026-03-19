# Issue: context-compaction continuity guard salvage

## Metadata
- issue_id: `I-20260319-0148`
- milestone: `M-20260306-workspace-routing-foundation`
- phase_state: `in_dev`
- priority: P0
- depends_on:
  - `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- source_brainstorm: `docs/pre-brainstorms/20260319-0148--context-compaction-salvage-and-retirement/brainstorms.md`
- source_candidates: `docs/pre-brainstorms/20260319-0148--context-compaction-salvage-and-retirement/candidates.md`

## Problem

旧 `context-compaction` 分支不再适合作为继续开发主线，但其独有的 continuity guard 能力仍值得保留。

## Desired Outcome

- 将以下小能力收编进当前主线：
  - `previous_context_compacted`
  - `Continuity Guard`
  - 首跳 prompt 的 compact/continuity 提醒
  - 相关测试
- 收编后退休旧分支/worktree。

## Acceptance

- `develop` 包含上述 continuity guard 能力。
- session rotation 与 routing 测试覆盖这些字段/提示。
- 旧 `feature/context-compaction-delegation-governance-20260318` 被清理。
