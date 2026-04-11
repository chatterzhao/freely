# Candidates - 20260410-1835--auth-switch-real-environment-and-e2e-governance-gap

### C-20260410-1835-A
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- next_action: `Materialize the chosen follow-on adequacy guard into doc-ibm-execution truth, pretests-gate, and a focused gate regression.`
- revisit_trigger: `Any follow-on owner touching auth switch / slot recovery / startup recovery / watchdog can still waive both End-to-End and Real-Environment without an artifact-backed live-evidence acceptance item.`
- acceptance_criteria:
  - `IBM truth explicitly says these follow-on owners cannot dual-waive End-to-End and Real-Environment with protected_environment_only alone.`
  - `pretests-gate fails when such an owner does dual-waive without at least one pass-level real_env or post_merge_dogfood acceptance item.`
  - `A focused regression proves the gate blocks the bad pattern and accepts the corrected pattern.`
- promotion_gate:
  - `Governance-only fix lands in skill/checklist/gate/test truth without touching runtime behavior.`
- open_questions:
  - `Whether this guard should later generalize beyond auth/switch/startup-recovery/watchdog family.`
  - `Whether replacement_evidence should eventually require direct artifact path parsing in addition to acceptance-item evidence.`
- acceptance_reviews:
  - reviewer: `codex`
    verdict: `pass`
    rationale: `Narrow rule directly targets the observed owner-contract drift without broad path-guessing or runtime coupling.`
