# Pre-Tests: develop-guarded-merge-entrypoint-enforcement-governance

## Acceptance Targets

### AT-001 raw develop merge is blocked before downstream gates

- acceptance target: `develop` 上没有 canonical guarded handshake 的 merge commit 会被 `pre-merge-commit` 立即拒绝，并明确提示改用 `freely pr-merge-guarded`
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- required evidence: `raw merge blocked with pr-merge-guarded guidance`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 guarded handshake still reaches governance materialization gate

- acceptance target: 当 canonical guarded state 和 completion marker 存在时，`pre-merge-commit` 仍继续执行 governance materialization gate，而不是被入口 enforcement 提前短路
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- required evidence: `guarded-state positive control still surfaces no-candidate-driven lifecycle evidence`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 guarded handshake still reaches promotion ownership gate

- acceptance target: duplicate promotion ownership 仍在 guarded handshake 存在时被 `pre-merge-commit` 拦下
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- required evidence: `duplicate develop promotion ownership is already active`
- blocker taxonomy: `execution_pending_or_failed`

### AT-004 canonical pr-merge-guarded paths remain valid under real hooks

- acceptance target: `pr-merge-guarded` 正常初始 merge 与 break-glass completion 继续通过真实 hook
- testing layer: governance
- target environment: `docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt` plus `docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
- required evidence: `normal receipt path pass` and `break-glass completion pass`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Raw develop merge commits without the canonical guarded handshake fail closed and point to freely pr-merge-guarded.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`

### AT-002
- id: `AT-002`
- requirement: `Entrypoint enforcement does not suppress governance materialization gate execution once guarded state exists.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`

### AT-003
- id: `AT-003`
- requirement: `Entrypoint enforcement does not suppress promotion ownership gating once guarded state exists.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`

### AT-004
- id: `AT-004`
- requirement: `Canonical pr-merge-guarded initial merge and break-glass completion still pass under the real hook contract.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
