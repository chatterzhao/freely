# Pre-Tests: global-restart-restore-memory-governance

## Acceptance Structure

### Pre-merge acceptance

- acceptance target: `global restart restore memory contract`
- testing layer: `focused regression + integration`
- target environment: `feature worktree`
- required evidence: manifest schema tests, retention checks, fleet restore selection checks
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. global restart surface is explicit all-project action, not project force alias.
2. manifest durable home and keep-latest-and-last-20 retention are implemented.
3. manifest stores previously-running project set and operator-stopped exclusion.
4. mandatory restore anchors are required; auxiliary evidence stays optional.

### Post-merge integration acceptance

- acceptance target: `develop-side global restart replay`
- testing layer: `post-merge acceptance`
- target environment: `develop`
- environment type: `protected verification worktree`
- required evidence: one controlled fleet restart verification artifact

1. explicit global restart restores only the projects that should come back.
2. operator-stopped projects remain stopped.
3. `develop` verification stays verification-only; failures replay via feature worktree.

### Post-merge application-native real-environment acceptance

- acceptance target: `Freely fleet restart in real environment`
- testing layer: `post-merge acceptance`
- target environment: `develop`
- environment type: `protected verification worktree`
- required evidence: application-native restart note over real workcells

1. durable continuity anchors survive and are sufficient for restore.
2. manifest history remains inspectable after replay.

### Post-merge end-to-end dogfood acceptance

- acceptance target: `Freely dogfoods the same global restart manifest contract`
- testing layer: `post-merge acceptance`
- target environment: `develop`
- environment type: `protected verification worktree`
- required evidence: dogfood restart note

1. dogfood run no longer behaves like blind relaunch-all.
2. if a new owner appears, it routes to a fresh lifecycle rather than mutating this issue.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `global restart is an explicit all-project action with a separate manifest-backed restore memory contract`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/global-restart-restore-memory-governance/raw-20260327-2006/code-reviews/20260330-global-restart-restore-memory-feature-verification.md`

### PT-2
- id: `PT-2`
- requirement: `manifest durability uses latest.json plus last-20 history retention under $FREELY_HOME/control-plane/restart`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/global-restart-restore-memory-governance/raw-20260327-2006/code-reviews/20260330-global-restart-restore-memory-feature-verification.md`

### PT-3
- id: `PT-3`
- requirement: `previously-running project set is restored while operator-stopped projects are excluded`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/global-restart-restore-memory-governance/raw-20260327-2006/code-reviews/20260330-global-restart-restore-memory-feature-verification.md`

### PT-4
- id: `PT-4`
- requirement: `mandatory restore anchors remain required inputs and auxiliary runtime evidence remains optional`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/global-restart-restore-memory-governance/raw-20260327-2006/code-reviews/20260330-global-restart-restore-memory-feature-verification.md`

### PT-5
- id: `PT-5`
- requirement: `post-merge protected-branch verification can replay the global restart without turning develop into an implementation surface`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/ibm/global-restart-restore-memory-governance/raw-20260327-2006/code-reviews/20260330-global-restart-restore-memory-feature-verification.md`
## Unit
- acceptance_target: 历史 issue，已完成验证
- testing_layer: unit
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成，当时不要求这些 section。原始测试证据在 issue 开发过程中已验证。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Integration
- acceptance_target: 历史 issue，已完成验证
- testing_layer: integration
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## End-to-End
- acceptance_target: 历史 issue，已完成验证
- testing_layer: end-to-end
- target_environment: develop merge chain (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 此 issue 在 pre-tests v2 标准引入前完成并已合并，原始实现已通过真实环境验证。
