# Pre-Tests: project-command-semantics-and-restore-work-governance

## Acceptance Structure

### Pre-merge acceptance

- acceptance target: `project command family semantics`
- testing layer: `focused regression + integration`
- target environment: `feature worktree`
- required evidence: runtime command tests, governance assertions, artifact-boundary checks
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. `start` / `stop` / `restart` / `start --force` / `restore-work` 都有不混层的单项目 contract。
2. `restart` 是显式一级 surface，默认不 silent resume interrupted AI work。
3. `start --force` 只允许 project-local safe repair set，不触碰 shared/global assets。
4. `restore-work` 消费 mandatory restore anchors，而不是把 auxiliary evidence 误当 required inputs。
5. process discovery / kill scope 继续锚定 project identity。

### Post-merge integration acceptance

- acceptance target: `develop command-family integration`
- testing layer: `post-merge acceptance`
- target environment: `develop`
- environment type: `protected verification worktree`
- required evidence: develop-side command walkthrough and verification note

1. `develop` 上的 command-family behavior 与本 issue taxonomy 一致。
2. `develop` 验证只做确认，不在受保护分支直接修实现。
3. 若失败，回 feature worktree / 新 feature worktree 修复后 replay。

### Post-merge application-native real-environment acceptance

- acceptance target: `real project runtime lifecycle`
- testing layer: `post-merge acceptance`
- target environment: `develop`
- environment type: `protected verification worktree`
- required evidence: one real project-scoped runtime walkthrough

1. stale pid / idle supervisor / partial readiness 能按 `attach/reuse -> local repair -> fresh bootstrap -> explicit global escalation` 恢复。
2. interrupted local AI work 不会被 silent resume 或 silent discard。

### Post-merge end-to-end dogfood acceptance

- acceptance target: `Freely uses the new project command contract on itself`
- testing layer: `post-merge acceptance`
- target environment: `develop`
- environment type: `protected verification worktree`
- required evidence: dogfood run note with command-family behavior

1. Freely 自举时不再把 project force 与 global reset 混层。
2. 若 dogfood 暴露新的 cross-project blast radius，则回新 lifecycle，而不是口头扩写本 issue。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `project command family has explicit single-project semantics for start stop restart start --force and restore-work`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`

### PT-2
- id: `PT-2`
- requirement: `restart does not silently restore interrupted local AI work`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`

### PT-3
- id: `PT-3`
- requirement: `start --force only touches the safe project-local repair set and never escalates into shared/global cleanup`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`

### PT-4
- id: `PT-4`
- requirement: `restore-work consumes mandatory continuity anchors while auxiliary evidence remains optional`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`

### PT-5
- id: `PT-5`
- requirement: `process discovery and kill scope remain anchored to project identity`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready`
