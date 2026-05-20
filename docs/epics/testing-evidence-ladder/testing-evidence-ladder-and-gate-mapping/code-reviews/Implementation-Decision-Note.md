# Implementation Decision Note: Testing Evidence Ladder and Gate Mapping (Slice 2)

## Decision

Materialize Slice 2 of C-20260325-0333-A as standalone B2_IBM artifacts — freeze the testing evidence ladder names, escalation rules, completion/retirement gate mapping, and artifact-plane evidence closeout schema. Do not gate on Slice 3 (real-environment harness) readiness.

## Why This

1. The revisit_trigger for Slice 2 (Slice 1 completed and verified) is satisfied as of C-20260325-0333-B `phase_state: completed`.
2. The absorbed inventory from pre-brainstorm already converged the ladder shape: five levels, non-overlapping, with per-level purpose/promotion/capability boundary.
3. Without frozen ladder vocabulary, IBM references and lifecycle gates cannot consume testing truth uniformly — each issue continues to define its own bar.
4. The materialization is purely documentary with no code changes, making it low-risk and independently verifiable.

## Alternatives Considered

| Alternative | Reason against |
|---|---|
| Wait for Slice 3 (real-environment harness) | Increases sequencing risk — ladder/gate mapping must precede harness standardization |
| Merge into existing `pre-test-merge` lifecycle candidate | Different scope — lifecycle is about stale transaction management, not evidence levels |
| Keep as pre-brainstorm indefinitely | Blocks downstream consumers (IBM references, completion/retirement gates) from consuming stable vocabulary |
| Create a new umbrella candidate | Unnecessary — C-20260325-0333-A already covers this scope; this is a planned slice |

## Boundary / Non-Goals

- This materialization does NOT implement Slice 3 (real-environment harness contract).
- This does NOT modify any runtime behavior, tooling, automation, or governance hooks.
- This does NOT redefine work already frozen in Slice 1 (story-level pre-tests.md quality gate).
- IBM reference updates are limited to importing ladder vocabulary by reference — no local redefinition.

## Residual Risk

| Risk | Mitigation |
|---|---|
| Issue class taxonomy may shift as Freely grows | Escalation rules are defined at the family level, not per-issue; new families can be added without changing the ladder |
| Artifact-plane evidence schema may need revision after Slice 3 | Schema is defined as minimal summary shape; Slice 3 can extend without breaking the baseline |
| Ladder names may drift from actual usage | Names are frozen in this materialization and referenced by IBM docs; any rename requires a follow-on issue |
