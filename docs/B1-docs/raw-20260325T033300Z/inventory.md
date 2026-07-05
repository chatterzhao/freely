# Absorbed Capability Inventory: testing-evidence-ladder-and-real-environment-gates

## Purpose

这份 inventory 不重新发明测试治理，而是先吸收 Freely 当前已经存在的 testing truth，再把真正缺失的能力边界收敛成最小 materialization 切口。

## Absorbed Truth Sources

### 1. IBM / issue materialization truth

#### `doc-ibm-execution`

Source:

- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`

Already frozen:

- `pre-tests.md` is not an appendix; it is the issue-level acceptance control surface.
- `pre-tests.md` and `tasks.md` must derive naturally from `prd.md`.
- `pre-tests.md` should default to integration / acceptance behavior, not code-reading TODOs.
- If merge-after verification exists, `pre-tests.md` must distinguish `pre-merge` and `post-merge acceptance`.
- Verification should not need oral explanation to reconstruct acceptance.

Still missing:

- A story-level `pre-tests.md` quality rubric strong enough to reject weak but formally present files.
- A shared testing ladder vocabulary beyond the current "integration / acceptance-first" baseline.
- A stable rule for when a story must escalate from integration to end-to-end or application-native real-environment evidence.

### 2. Integration-acceptance-first governance

Source:

- `docs/B2-docs/ibm/integration-acceptance-first-verification-governance/issues/integration-acceptance-first-verification-governance.md`
- `docs/B2-docs/ibm/integration-acceptance-first-verification-governance/pre-tests.md`
- `docs/progress/workspace-routing-foundation/p-integration-acceptance-first-verification-governance.md`

Already frozen:

- Verification defaults to integration / acceptance evidence first.
- Code review is a secondary verification surface.
- `LAWS.md` and lifecycle truth already align develop merge gates with integration / acceptance evidence.

Still missing:

- Explicit classification for `script regression`, `end-to-end`, `application-native real-environment`, and `protected-env post-merge acceptance`.
- A machine-readable mapping from evidence level to completion / retirement gates.
- A formal distinction between "tests not yet run" and "`pre-tests.md` itself is too weak to define acceptance."

### 3. Real-environment watchdog / manager recovery proof

Source:

- `docs/B2-docs/ibm/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`

Already frozen:

- Some issue families require live integration tests against the real runtime chain.
- "Current account unavailable -> probe -> switch -> bootstrap manager -> resume supervision" is legitimate acceptance scope, not ad hoc dogfood.
- A pure-script recovery control plane can be required before any AI process exists.

Still missing:

- A reusable rule for which issue classes must default to live integration or application-native real-environment evidence.
- A shared harness taxonomy separating focused integration tests from heavier real-environment scenarios.

### 4. Application-native observability / evidence surfaces

Source:

- `docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/issues/application-native-runtime-observation-contract-and-observability-planes.md`
- `docs/progress/workspace-routing-foundation/p-application-native-runtime-observation-contract-and-observability-planes.md`

Already frozen:

- Artifact plane is the canonical truth surface for acceptance evidence.
- Current-state / fleet surfaces should only mirror a minimum acceptance summary plus `acceptance_ref`.
- Shared deep-ref groups are the right projection mechanism for status surfaces.

Still missing:

- A stable schema for testing-closeout evidence classes.
- A rule for what minimal testing summary runtime/status surfaces must mirror and what must remain only in artifact truth.
- A consistent bridge between `pre-tests.md`, completion evidence, and artifact-plane acceptance references.

### 5. Protected and stale-lifecycle verification governance

Source:

- `docs/B1-docs/raw-20260322T161500Z/candidates.md`
- `docs/B1-docs/raw-20260322T180100Z/candidates.md`

Already frozen:

- Protected verification environments and stale pre-test-merge lifecycle both already depend on testing evidence being trustworthy.
- Worktree cleanup / retirement must not outrun unresolved verification obligations.

Still missing:

- A top-level rule for when protected-env evidence is required versus optional.
- A shared test-evidence contract that these lifecycle candidates can consume instead of each defining their own partial bar.

## Consolidated Gap Map

### Gap 1. Story-level `pre-tests.md` quality is under-specified

Current truth says `pre-tests.md` is important, but it still does not define a rejectable quality floor. A file can exist and still fail to restore the acceptance contract.

Minimum missing contract:

- required fields for acceptance target
- required testing layer labels
- required target environment
- required evidence outputs
- blocker taxonomy separating test-definition failure from test-execution failure

### Gap 2. The testing evidence ladder is not yet a first-class capability

Freely has partial language around integration, live integration, post-merge acceptance, and dogfood proof, but no single contract that defines the full ladder and the non-substitutable boundary of each level.

Minimum missing contract:

- `script regression`
- `integration`
- `end-to-end scenario`
- `application-native real-environment`
- `protected-env post-merge acceptance`

For each level, Freely still needs:

- default purpose
- promotion trigger
- what it can prove
- what it cannot replace

### Gap 3. Completion and retirement gates do not yet consume testing truth uniformly

Freely already insists that completion cannot be inferred from clean/merged/verified alone, but testing evidence is not yet normalized enough to let runtime/governance reject weak closeouts consistently.

Minimum missing contract:

- completion verification minimum evidence by issue class
- worktree retirement minimum evidence by issue class
- artifact-plane summary shape
- status-surface mirror shape

### Gap 4. Real-environment testing is still real but not yet capability-shaped

Freely has proven that real-environment validation is necessary for runtime/manager/watchdog classes of bugs, but this requirement still lives mostly in issue-local custom tests.

Minimum missing contract:

- which issue families default to real-environment evidence
- what counts as a real-environment run
- what harness shape is acceptable
- what evidence must be retained

## Proposed Minimal Materialization Sequence

### Slice 1. Story-level `pre-tests.md` quality gate

Why first:

- Every later testing gate depends on `pre-tests.md` being able to reconstruct acceptance.
- This is the narrowest cut that can immediately harden every future issue.

Deliverable shape:

- Freeze a story-level `pre-tests.md` rubric in capability truth.
- Update IBM / lifecycle references to reject "commands-only" `pre-tests.md`.

### Slice 2. Testing evidence ladder and gate mapping

Why second:

- Once `pre-tests.md` quality is stable, Freely can safely define which evidence levels are required by which issue classes.

Deliverable shape:

- Freeze the ladder names, escalation rules, and completion/retirement mapping.
- Reuse artifact plane as canonical evidence home.

### Slice 3. Application-native / real-environment harness contract

Why third:

- Only after ladder/gate truth is stable should Freely standardize how heavy scenarios are executed and retained.

Deliverable shape:

- Define minimal real-environment harness patterns and evidence retention rules.
- Keep runtime/status surfaces as summary-only mirrors.

## Current Recommendation

This candidate should not jump directly to implementation. The next valid Freely move is:

1. materialize a smallest issue for the story-level `pre-tests.md` quality gate
2. keep this broader candidate active as the umbrella capability
3. route later ladder/harness work as follow-on issues only after slice 1 is frozen
