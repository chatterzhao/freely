# Pre-Tests: tool-authorization-bootstrap-and-post-consent-materialization-governance

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `issue truth clearly separates activation consent, project authorization bootstrap, tool trust, and adapter policy`
- evidence_level: `doc-read`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/tool-authorization-bootstrap-and-post-consent-materialization-governance/issues/tool-authorization-bootstrap-and-post-consent-materialization-governance.md`

### PT-2
- id: `PT-2`
- requirement: `the owner freezes a per-tool authorization/bootstrap matrix instead of a tool-agnostic umbrella claim`
- evidence_level: `doc-read`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/tool-authorization-bootstrap-and-post-consent-materialization-governance/brainstorms/b-tool-authorization-bootstrap-and-post-consent-materialization-governance.md`

### PT-3
- id: `PT-3`
- requirement: `the owner freezes shared degradation semantics and runtime refactor seams for future CLI/TUI/GUI/settings reuse`
- evidence_level: `doc-read`
- status: `pass`
- artifact_ref: `docs/epics/freely-product-architecture/tool-authorization-bootstrap-and-post-consent-materialization-governance/issues/tool-authorization-bootstrap-and-post-consent-materialization-governance.md`

### PT-4
- id: `PT-4`
- requirement: `candidate, milestone, issue, and progress artifacts form a lawful architecture-owner chain`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `./bin/governance-check`

## Pre-merge Focused Regression / Smoke

1. acceptance target:
   - this owner is materialized as documentation-first contract truth without overreaching into runtime implementation
2. testing layer:
   - lifecycle and wording review
3. target environment:
   - feature worktree
4. required evidence:
   - `./bin/governance-check`
5. blocker taxonomy:
   - `definition_missing`
   - `boundary_overlap`
   - `lifecycle_writeback_missing`
6. failure handling / replay expectation:
   - narrow the contract, correct overlap with sibling owners, and keep implementation out of scope

## Post-merge Integration Acceptance

1. acceptance target:
   - canonical `develop` carries the same architecture contract and milestone traceability
2. testing layer:
   - lifecycle replay
3. target environment:
   - `develop`
4. required evidence:
   - `./bin/governance-check`
5. blocker taxonomy:
   - `execution_pending_or_failed`
   - `contract_drift`
6. failure handling / replay expectation:
   - reopen only if the architecture contract still overlaps older owners or if implementation follow-ons cannot be split cleanly
