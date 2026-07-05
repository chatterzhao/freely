---
local_id: I-20260519-0333-C
issue_title: Testing evidence ladder and gate mapping
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
promoted_from: pre-brainstorms/20260325-0333--testing-evidence-ladder-and-real-environment-gates
source_candidate: docs/B1-docs/raw-20260325-0333/candidates.md#C-20260325-0333-A
milestone: M-20260306-workspace-routing-foundation
canonical_issue_path: docs/epics/testing-evidence-ladder/testing-evidence-ladder-and-gate-mapping/issues/testing-evidence-ladder-and-gate-mapping.md
pre_tests_path: docs/epics/testing-evidence-ladder/testing-evidence-ladder-and-gate-mapping/pre-tests.md
tasks_path: docs/epics/testing-evidence-ladder/testing-evidence-ladder-and-gate-mapping/tasks.md
verification_artifact_dir: docs/epics/testing-evidence-ladder/testing-evidence-ladder-and-gate-mapping/code-reviews
platform_ids:
  github:
    issue_id: '2601'
    url: https://github.com/chatterzhao/freely/issues/2601
    synced_at: '2026-06-13T10:45:32Z'
platform_state: closed
updated_at: '2026-06-13T10:45:32Z'
session_refs:
- tool: cc
  session_id: 20260519-testing-evidence-ladder-slice2-b2
  role: author
primary_platform: github
created_at: '2026-06-13T10:45:32Z'
---

# I-20260519-0333-C: Testing Evidence Ladder and Gate Mapping

Materialize Slice 2 of C-20260325-0333-A umbrella: freeze the testing evidence ladder names, escalation rules, completion/retirement gate mapping, and artifact-plane evidence closeout schema.

- source_candidate: `docs/B1-docs/raw-20260325-0333/candidates.md#C-20260325-0333-A`
- milestone: `M-20260306-workspace-routing-foundation`
- pre_tests_path: `docs/epics/testing-evidence-ladder/testing-evidence-ladder-and-gate-mapping/pre-tests.md`
- verification_artifact_dir: `docs/epics/testing-evidence-ladder/testing-evidence-ladder-and-gate-mapping/code-reviews`

## Ladder Levels

1. **Script regression** — Fast, isolated checks for regressions in scripts/tooling
2. **Integration** — Verification that components work together correctly
3. **End-to-end scenario** — Full workflow scenarios across the system
4. **Application-native real-environment** — Tests running against the real runtime chain
5. **Protected-env post-merge acceptance** — Acceptance verification in a protected environment after merge

## Escalation Rules

| Issue Family | Minimum Level for Completion | Minimum Level for Retirement |
|---|---|---|
| Documentation-only | Script regression | Script regression |
| Script/tooling changes | Integration | Integration |
| Internal governance | Integration | Integration |
| Manager/runtime changes | Application-native real-environment | Integration + post-merge acceptance |
| Watchdog/control-plane | Application-native real-environment | Protected-env post-merge acceptance |

## Blocker Taxonomy (inherited from Slice 1)

- `definition_missing` — pre-tests.md does not define what acceptance means
- `commands_only` — pre-tests.md contains commands but no acceptance target
- `evidence_plan_missing` — pre-tests.md defines acceptance but not how to produce evidence
- `execution_pending_or_failed` — evidence plan exists but execution is incomplete or failed

## Next Action

Dev-loop execution complete. All AT-001 through AT-006 are satisfied and verified. IBM references updated to consume ladder vocabulary by reference.
