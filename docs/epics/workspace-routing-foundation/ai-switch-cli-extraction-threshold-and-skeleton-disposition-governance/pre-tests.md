# Pre-tests

## Acceptance Contract

- acceptance_target: `Issue-bound IBM for extraction timing and skeleton disposition of the future ai-switch-cli backend`
- testing_layer: `doc`
- target_environment: `canonical repo docs in the active feature worktree before any standalone backend extraction starts`
- required_evidence:
  - `prd.md` freezes an executable extraction-start checklist and the control-plane/backend split without circular prerequisites
  - `issues/*.md` and issue-bound brainstorm document the follow-on extraction owner handoff package
  - `tasks.md` reflects current IBM work instead of pre-materialization steps
  - `docs/milestones.md` keeps candidate mirror semantics explicit so committed issue authority is not confused with candidate queue presentation
- blocker_taxonomy:
  - `definition_missing`: extraction threshold, boundary, or skeleton disposition still depends on chat memory
  - `commands_only`: docs enumerate commands but do not explain the decision contract for split/no-split
  - `evidence_plan_missing`: no explicit handoff package or start checklist for the follow-on extraction owner
  - `execution_pending_or_failed`: canonical docs still contain circular gate wording, stale tasks, or ambiguous milestone mirror semantics

## Pre-merge acceptance

1. IBM docs must make the extraction threshold concrete enough that a later owner can decide “split now / do not split yet” without relying on chat memory.
2. IBM docs must clearly separate Freely control-plane responsibilities from backend responsibilities.
3. The docs must explicitly classify `/Users/zhaoyu/Downloads/code/my-codex-account-switch/codex-account-switch` as non-canonical until a formal extraction owner starts.
4. The docs must define the allowed handling paths for the skeleton:
   - rename in place to `ai-switch-cli`
   - discard and create fresh repo
5. The docs must not claim standalone extraction has already begun.
6. The docs must not reopen the frozen Codex slot bundle contract or pretend other tools already have verified parity.
7. The docs must name the generic helper surfaces that should be stabilized before extraction, including write-before-backup for user-home config mutation.

## Post-merge acceptance

1. A follow-on owner can open a dedicated extraction worktree without re-researching whether the threshold has been met.
2. Freely runtime and docs can continue evolving current embedded backend logic without ambiguity about what still remains canonical.
3. Future repo migration of the local skeleton can be audited against a written rule instead of operator memory.

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `extraction threshold is explicit and executable`
- evidence_level: `doc`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/prd.md`

### PT-2
- id: `PT-2`
- requirement: `Freely control-plane vs backend boundary is explicit`
- evidence_level: `doc`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/prd.md`

### PT-3
- id: `PT-3`
- requirement: `local codex-account-switch skeleton is classified and constrained by written disposition rules`
- evidence_level: `doc`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/prd.md`
