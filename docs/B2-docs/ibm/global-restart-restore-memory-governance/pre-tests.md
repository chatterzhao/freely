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
- artifact_ref: `docs/B2-docs/ibm/global-restart-restore-memory-governance/code-reviews/20260330-global-restart-restore-memory-feature-verification.md`

### PT-2
- id: `PT-2`
- requirement: `manifest durability uses latest.json plus last-20 history retention under $FREELY_HOME/control-plane/restart`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/global-restart-restore-memory-governance/code-reviews/20260330-global-restart-restore-memory-feature-verification.md`

### PT-3
- id: `PT-3`
- requirement: `previously-running project set is restored while operator-stopped projects are excluded`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/global-restart-restore-memory-governance/code-reviews/20260330-global-restart-restore-memory-feature-verification.md`

### PT-4
- id: `PT-4`
- requirement: `mandatory restore anchors remain required inputs and auxiliary runtime evidence remains optional`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/global-restart-restore-memory-governance/code-reviews/20260330-global-restart-restore-memory-feature-verification.md`

### PT-5
- id: `PT-5`
- requirement: `post-merge protected-branch verification can replay the global restart without turning develop into an implementation surface`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/global-restart-restore-memory-governance/code-reviews/20260330-global-restart-restore-memory-feature-verification.md`
