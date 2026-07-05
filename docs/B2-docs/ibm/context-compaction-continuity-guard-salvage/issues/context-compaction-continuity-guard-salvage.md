# Issue: context-compaction continuity guard salvage

## Metadata
- issue_id: `I-20260319-0148`
- epic-name: `workspace-routing-foundation`
- story-name: `context-compaction-continuity-guard-salvage`
- verification_artifact_dir: `docs/B2-docs/ibm/context-compaction-continuity-guard-salvage/code-reviews`
- milestone: `M-20260306-workspace-routing-foundation`
- phase_state: `completed`
- priority: P0
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/ibm/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- source_brainstorm: `docs/B1-docs/raw-20260319/brainstorms.md`
- source_candidate: `docs/B1-docs/raw-20260319/candidates.md`

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

## Verification

- `git merge-base --is-ancestor 5ccb115 develop`
- `git branch --list '*context-compaction*'`
- `bash docs/system/workspace/scripts/tests/test-freely-session-rotation`
- `./bin/governance-check`

## Closure Judgment

- 旧 `context-compaction` 分支独有的 continuity guard 已被 canonical `develop` 吸收：`runtime/freely` 现在会写入 `previous_context_compacted`、输出 `Continuity Guard` 段落，并在相关 prompt 中保留 compact/continuity 提醒。
- `test-freely-session-rotation` 已把这些 salvaged 字段和行为锁进主线回归，不再需要依赖旧分支继续保留实现所有权。
- 当前本地不存在保留中的 `feature/context-compaction*` branch，因此这条 salvage 线可以作为已完成的吸收/退役事务收口为 `completed`。

## Next

- 本 issue 已完成；后续 continuity/rotation 演进回到主线 continuity governance issue family，不重新打开旧 context-compaction salvage 线。
