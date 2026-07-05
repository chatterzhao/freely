# Candidates - 20260319-0148--context-compaction-salvage-and-retirement

## Context
- Source brainstorm: ./brainstorms.md
- Status: in_research

## Candidates

### C-20260319-0148-A: legacy issue
- title: salvage continuity-guard-only changes from obsolete context-compaction branch
- problem: 旧 context-compaction 分支的大部分治理语义已被主线覆盖，但仍有少量 continuity guard 价值未收编。
- why_now: 若不及时收编，旧工位会持续制造重复判断成本。
- acceptance_hint:
  - 仅收编 `previous_context_compacted`、`Continuity Guard`、首跳 compact 提醒及相关测试
  - 不重复主线已有的 continuity/rotation 治理
  - 收编完成后退休旧分支/worktree
- priority: P0
- status: promoted
- promoted_issue_path: `docs/B2-docs/ibm/context-compaction-continuity-guard-salvage/issues/context-compaction-continuity-guard-salvage.md`
- legacy_id_mapping: I-20260319-0148  # 历史遗留的 issue id
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs:
  - `feature/context-compaction-integration-salvage-20260319`
