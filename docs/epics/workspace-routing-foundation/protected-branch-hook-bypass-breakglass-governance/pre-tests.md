# Pre-Tests: protected-branch-hook-bypass-breakglass-governance

## Acceptance Targets

### AT-001 constitutional principle frozen

- acceptance target: `CONSTITUTION` 明确 protected-branch hook/gate bypass 默认违规，只有 break-glass 白名单例外
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd` 一致定义原则边界
- blocker taxonomy: `definition_missing`

### AT-002 whitelist ownership frozen

- acceptance target: `LAWS` 是唯一的 break-glass whitelist truth
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd + tasks` 一致写明分层与 owner
- blocker taxonomy: `definition_missing`

### AT-003 reason taxonomy and forbidden examples frozen

- acceptance target: reason taxonomy、最小 required fields 与 forbidden examples 冻结
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd + brainstorm`
- blocker taxonomy: `definition_missing`

### AT-004 guarded completion contract frozen

- acceptance target: `merge-guarded` 冲突后 completion path 的受控 contract 被写明
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd + tasks`
- blocker taxonomy: `definition_missing`

### AT-005 audit contract frozen

- acceptance target: `governance-check` 或等价 gate 的 bypass audit contract 被写明
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd + tasks`
- blocker taxonomy: `definition_missing`

### AT-006 current revert judgment frozen

- acceptance target: 当前 `27faa2e` 与 `a10f6d8` 的 revert judgment 被写成 canonical issue truth
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + brainstorm`
- blocker taxonomy: `definition_missing`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `The constitutional principle for protected-branch bypass is frozen.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/protected-branch-hook-bypass-breakglass-governance/issues/protected-branch-hook-bypass-breakglass-governance.md`

### AT-002
- id: `AT-002`
- requirement: `LAWS is frozen as the only whitelist truth for break-glass reasons and duties.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/protected-branch-hook-bypass-breakglass-governance/prd.md`

### AT-003
- id: `AT-003`
- requirement: `Reason taxonomy, required fields, and forbidden examples are frozen.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/protected-branch-hook-bypass-breakglass-governance/brainstorms/b-protected-branch-hook-bypass-breakglass-governance.md`

### AT-004
- id: `AT-004`
- requirement: `Guarded merge completion no longer falls back to an undefined raw commit path.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/protected-branch-hook-bypass-breakglass-governance/tasks.md`

### AT-005
- id: `AT-005`
- requirement: `A post-hoc audit contract exists for unauthorized bypass on protected-branch merge paths.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/protected-branch-hook-bypass-breakglass-governance/prd.md`

### AT-006
- id: `AT-006`
- requirement: `The current judgment about reverting 27faa2e and a10f6d8 is frozen as canonical owner truth.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/protected-branch-hook-bypass-breakglass-governance/brainstorms/b-protected-branch-hook-bypass-breakglass-governance.md`
