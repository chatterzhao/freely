# Tasks: Testing Evidence Ladder and Gate Mapping

- issue_id: I-20260519-0333-C

## Task List

### T-001: Define the five-level testing evidence ladder

- description: Write non-overlapping definitions for script regression, integration, end-to-end scenario, application-native real-environment, and protected-env post-merge acceptance. Each level must include: default purpose, promotion trigger, what it can prove, what it cannot replace.
- owner: I-20260519-0333-C
- status: completed
- artifact: docs/B2-docs/ibm/red-green/raw-20260325T033300Zprd.md

### T-002: Define escalation rules

- description: For each issue family, enumerate the minimum evidence level required. Families: documentation-only, script/tooling, internal governance, manager/runtime, watchdog/control-plane.
- owner: I-20260519-0333-C
- status: completed
- artifact: docs/B2-docs/ibm/red-green/raw-20260325T033300Zprd.md

### T-003: Define completion/retirement gate mapping

- description: Map issue classes to minimum evidence levels for both completion verification and worktree retirement. Add blocker taxonomy integration (evidence_gap vs execution_pending).
- owner: I-20260519-0333-C
- status: completed
- artifact: docs/B2-docs/ibm/red-green/raw-20260325T033300Zprd.md

### T-004: Define artifact-plane evidence closeout schema

- description: Define the minimal summary shape for pre-tests.md completion evidence, including acceptance item references, evidence level met/not-met per AT, closeout verdict, and artifact plane ref.
- owner: I-20260519-0333-C
- status: completed
- artifact: docs/B2-docs/ibm/red-green/raw-20260325T033300Zprd.md

### T-005: Define status-surface mirror rules

- description: Define what testing summary runtime/status surfaces must mirror and what must remain only in artifact-plane truth.
- owner: I-20260519-0333-C
- status: completed
- artifact: docs/B2-docs/ibm/red-green/raw-20260325T033300Zprd.md

### T-006: Update IBM reference documents

- description: Update ibm-completion-gate.md, prd-quality-bar.md, and issue-materialization-checklist.md to consume the ladder vocabulary by reference. No local redefinition.
- owner: I-20260519-0333-C
- status: completed
- artifact: docs/system/workspace/skills/freely-doc-B2_IBM-execution/references/

### T-007: Update candidates.md umbrella status

- description: Update C-20260325-0333-A umbrella status to reflect the materialization decision for Slice 2.
- owner: I-20260519-0333-C
- status: completed
- artifact: docs/B1-docs/raw-20260325T033300Z/candidates.md

### T-008: Update milestones.md

- description: Add I-20260519-0333-C to committed_issues of M-20260306-workspace-routing-foundation; update C-20260325-0333-A phase_state and next_action.
- owner: I-20260519-0333-C
- status: completed
- artifact: docs/milestones.md
