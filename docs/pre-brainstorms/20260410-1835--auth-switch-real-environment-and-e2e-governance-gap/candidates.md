# Candidates - 20260410-1835--auth-switch-real-environment-and-e2e-governance-gap

### C-20260410-1835-A
- candidate_format_version: `v2`
- title: Auth switch real-environment and end-to-end adequacy governance
- problem: Recent auth/switch follow-on owners could legally waive both `End-to-End` and `Real-Environment` with `protected_environment_only`, even when their scope touched `auth switch / slot recovery / startup recovery / watchdog / freely start / bin/ai / codex exec` behavior that really needed live executable evidence.
- why_now: Dogfooding proved that the missing signal was not a lack of tests in the abstract but an adequacy gap in how owner pre-tests, IBM guidance, and merge gates treated real command-surface and startup-recovery acceptance.
- acceptance_criteria:
  - `IBM truth explicitly forbids auth/switch/startup-recovery follow-on owners from dual-waiving End-to-End and Real-Environment without artifact-backed live evidence.`
  - `pretests-gate fails when such an owner dual-waives both sections without at least one pass-level real_env or post_merge_dogfood acceptance item.`
  - `A focused regression proves the gate blocks the bad pattern and accepts the corrected pattern.`
- fix_approach: Tighten doc-ibm-execution references plus `pretests-gate` so auth/switch/startup-recovery family owners must keep live executable evidence, then lock that behavior with a focused gate regression.
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260410-1835-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/auth-switch-real-environment-and-e2e-adequacy-governance/issues/auth-switch-real-environment-and-e2e-adequacy-governance.md`
- session_refs: []
- next_action: `Materialize the chosen follow-on adequacy guard into doc-ibm-execution truth, pretests-gate, and a focused gate regression.`
- revisit_trigger: `Any follow-on owner touching auth switch / slot recovery / startup recovery / watchdog can still waive both End-to-End and Real-Environment without an artifact-backed live-evidence acceptance item.`
- source_brainstorm: `docs/pre-brainstorms/20260410-1835--auth-switch-real-environment-and-e2e-governance-gap/brainstorms.md`
- promotion_gate:
  - `Governance-only fix lands in skill/checklist/gate/test truth without touching runtime behavior.`
- open_questions:
  - `Whether this guard should later generalize beyond auth/switch/startup-recovery/watchdog family.`
  - `Whether replacement_evidence should eventually require direct artifact path parsing in addition to acceptance-item evidence.`
- acceptance_reviews:
  - reviewer: `codex`
    verdict: `pass`
    rationale: `Narrow rule directly targets the observed owner-contract drift without broad path-guessing or runtime coupling.`
