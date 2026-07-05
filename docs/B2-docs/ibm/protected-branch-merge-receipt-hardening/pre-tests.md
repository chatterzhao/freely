# Pre-Tests: protected-branch-merge-receipt-hardening

## Acceptance Targets

### AT-001 residual boundary frozen

- acceptance target: issue-bound artifacts 明确这条 owner 是 residual hardening，不 reopen break-glass policy
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd + brainstorm`
- blocker taxonomy: `definition_missing`

### AT-002 root patch classification frozen

- acceptance target: root staged patch 被明确分成 `keep-as-signal`、`already-absorbed`、`drop-as-regression`
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `brainstorm + tasks`
- blocker taxonomy: `definition_missing`

### AT-003 completion-only boundary frozen

- acceptance target: `merge_completion_only` boundary 被写明，break-glass 不扩张到 initial clean merge
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd + tasks`
- blocker taxonomy: `definition_missing`

### AT-004 receipt parity audit contract frozen

- acceptance target: trailer/ledger parity 所需字段与 failure semantics 冻结
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `issue + prd`
- blocker taxonomy: `definition_missing`

### AT-005 staged regression boundary frozen

- acceptance target: staged-view owner visibility 与 sibling-context immunity 都被保留成 canonical regression boundary
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `prd + tasks`
- blocker taxonomy: `definition_missing`

### AT-006 watchdog revert excluded

- acceptance target: watchdog repo-root resolution 被明确判定为 already-absorbed / out-of-scope
- testing layer: IBM review
- target environment: issue-bound artifacts
- required evidence: `brainstorm + issue`
- blocker taxonomy: `definition_missing`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `This owner only handles protected-branch merge residual hardening.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/issues/protected-branch-merge-receipt-hardening.md`

### AT-002
- id: `AT-002`
- requirement: `The root staged patch is classified before any implementation is accepted.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/brainstorms/b-protected-branch-merge-receipt-hardening.md`

### AT-003
- id: `AT-003`
- requirement: `Break-glass remains merge-completion-only.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/prd.md`

### AT-004
- id: `AT-004`
- requirement: `Receipt trailer and ledger parity fields are frozen as an auditable contract.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/prd.md`

### AT-005
- id: `AT-005`
- requirement: `Staged-view and sibling-context regression boundaries are frozen before dev-loop changes.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/tasks.md`

### AT-006
- id: `AT-006`
- requirement: `Watchdog repo-root resolution is explicitly excluded from this owner.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/issues/protected-branch-merge-receipt-hardening.md`
