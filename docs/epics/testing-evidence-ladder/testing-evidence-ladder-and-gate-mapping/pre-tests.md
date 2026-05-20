# Pre-Tests: Testing Evidence Ladder and Gate Mapping

- issue_id: I-20260519-0333-C
- acceptance_target: Freeze the testing evidence ladder, escalation rules, and completion/retirement gate mapping for Freely
- testing_layer: integration + review
- target_environment: docs review (no runtime component in this slice)
- required_evidence: frozen ladder definitions, escalation rules, gate mapping, updated references
- blocker_taxonomy: definition_missing | commands_only | evidence_plan_missing | execution_pending_or_failed

## Rationale

This slice is purely documentary — it freezes vocabulary, rules, and mappings into capability truth. There is no code to run. Acceptance is verified by review of the artifacts: that the ladder is internally consistent, non-overlapping, consumable by gates, and correctly referenced from IBM materials.

## Integration

### Acceptance Item Review

- [x] Five ladder levels each have non-overlapping: default purpose, promotion trigger, what it can prove, what it cannot replace
- [x] Escalation rules enumerate the minimum evidence level for each issue family
- [x] Completion verification minimum evidence is defined per issue class
- [x] Worktree retirement minimum evidence is defined per issue class
- [x] Artifact-plane evidence closeout schema is defined
- [x] Blocker taxonomy distinguishes evidence_gap from execution_pending
- [x] IBM reference documents consume ladder vocabulary without redefining it

## End-to-End

### Traceability Walkthrough

- [x] Given the issue class taxonomy, each class maps to a minimum evidence level for both completion and retirement
- [x] Given an artifact-plane closeout, a reviewer can determine whether the minimum evidence level was met
- [x] Given a blocker with taxonomy label, a consumer can distinguish "tests not yet run" from "tests not yet defined"
- [x] Given a ladder level definition, a reader can determine what it does and does not prove

## Real-Environment

N/A — this slice produces frozen definitions and mappings only. No runtime component.

## Acceptance Items

### AT-001: Five-level ladder completeness

- id: AT-001
- requirement: All five ladder levels (script regression, integration, end-to-end scenario, application-native real-environment, protected-env post-merge acceptance) are defined with non-overlapping boundaries
- adequacy: Each level has explicit default purpose, promotion trigger, what it can prove, what it cannot replace
- evidence_level: integration (document review)
- status: completed

### AT-002: Escalation rules

- id: AT-002
- requirement: Escalation rules enumerate for each issue family the minimum evidence level
- adequacy: Enumeration covers at least: documentation-only changes, script/tooling changes, internal governance changes, manager/runtime changes, watchdog/control-plane changes
- evidence_level: integration (document review)
- status: completed

### AT-003: Completion gate minimum evidence

- id: AT-003
- requirement: completion verification maps each issue class to a minimum evidence level; absence of that level blocks completion declaration
- adequacy: Mapping covers all issue classes from AT-002; blocker taxonomy distinguishes level-not-met from execution-pending
- evidence_level: integration (document review)
- status: completed

### AT-004: Retirement gate minimum evidence

- id: AT-004
- requirement: worktree retirement maps each issue class to a minimum evidence level
- adequacy: Mapping covers all issue classes from AT-002; a worktree cannot be retired if its minimum evidence level is unsatisfied
- evidence_level: integration (document review)
- status: completed

### AT-005: Artifact-plane evidence closeout schema

- id: AT-005
- requirement: The closeout evidence schema defines the minimal summary shape that pre-tests.md completion evidence must produce, referencing artifact plane as canonical truth
- adequacy: Schema includes acceptance item references, evidence level met/not-met per AT, closeout verdict, and artifact plane ref
- evidence_level: integration (document review)
- status: completed

### AT-006: IBM reference consumption

- id: AT-006
- requirement: IBM references (ibm-completion-gate.md, prd-quality-bar.md, issue-materialization-checklist.md) consume the ladder vocabulary without redefining it
- adequacy: Each reference either imports the ladder by reference (preferred) or includes a stable pointer; no local redefinition of ladder levels
- evidence_level: integration (document review)
- status: completed
