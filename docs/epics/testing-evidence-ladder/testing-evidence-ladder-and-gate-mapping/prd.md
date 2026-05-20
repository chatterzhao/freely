# PRD: Testing Evidence Ladder and Gate Mapping

## Goal

Freeze the testing evidence ladder names, escalation rules, and completion/retirement gate mapping for Freely. After Slice 1 (story-level `pre-tests.md` quality gate) established that `pre-tests.md` must be able to reconstruct acceptance, Slice 2 defines *which* evidence levels exist and *when each is required* — so that completion and retirement gates can consume testing truth uniformly rather than relying on per-issue judgment.

## Requirements

1. **Define the five-level testing evidence ladder** with non-overlapping names, default purpose, promotion triggers, and non-substitutable boundaries:
   - Script regression
   - Integration
   - End-to-end scenario
   - Application-native real-environment
   - Protected-env post-merge acceptance

2. **Define escalation rules**: for each level, specify what it can prove and what it cannot replace. A lower level passing does not satisfy a gate that requires a higher level.

3. **Define completion verification minimum evidence by issue class**: map issue families to the minimum evidence level required before `phase_state: completed` may be set.

4. **Define worktree retirement minimum evidence by issue class**: map issue families to the minimum evidence level required before a worktree may be retired.

5. **Define artifact-plane evidence closeout schema**: the minimal summary shape that `pre-tests.md` completion evidence must produce, referencing artifact plane as canonical truth.

6. **Define status-surface mirror rules**: what testing summary runtime/status surfaces must mirror and what must remain only in artifact-plane truth.

## Scope

- Freeze ladder names, escalation rules, completion/retirement mapping
- Reference artifact plane as canonical evidence home (inherited from `application-native-runtime-observation-contract-and-observability-planes`)
- Define blocker taxonomy for evidence gap (inherited from Slice 1's `definition_missing`, `commands_only`, `evidence_plan_missing`, `execution_pending_or_failed`)
- Update IBM reference documents to consume ladder vocabulary

## Non-Goals

- Real-environment harness implementation (Slice 3)
- Runtime/status surface implementation
- Changes to existing `pre-tests.md` quality gate (Slice 1)
- Tooling or automation changes
- Creating a separate pre-brainstorm (convergence is complete)

## Dev-Loop Handoff

### 前置条件

- Slice 1 (story-level `pre-tests.md` quality gate) is completed and verified
- `C-20260325-0333-B` is closed with `phase_state: completed`

### 实现顺序

1. Receive the five-level ladder definition as capability truth
2. Write escalation rules per level
3. Write completion/retirement gate mapping per issue class
4. Write artifact-plane evidence closeout schema
5. Write status-surface mirror rules
6. Update IBM reference documents to reference ladder vocabulary

### 验收标准

- All five ladder levels have non-overlapping definitions with default purpose, promotion trigger, what they can prove, and what they cannot replace
- Escalation rules are stable: for each issue family, the minimum required evidence level is enumerable
- Completion verification and worktree retirement are each gated by minimum evidence level per issue class
- Artifact-plane evidence closeout schema is defined
- Blockers can be machine-readably classified as l1 evidence_gap (level not met) or l2 execution_pending (tests defined but not yet run)
- IBM references consume ladder vocabulary without redefining it
