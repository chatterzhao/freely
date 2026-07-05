---
name: config.toml Complete Migration Implementation Decision Note
owner_issue: I-20260616T044030Z-A
implementation_decision_note: true
phase_state: completed
review_id: config-toml-complete-review
---

- issue_id: I-20260616T044030Z-A
- issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260616T044030Z-A/issue.md
- source_candidate: docs/B1-docs/raw-20260616T044030Z30Z/candidates.md

## Implementation Decision Note

- decision: Auto-migration in load_config() — try config.toml, fallback config.env, auto-create config.toml on first successful env read
- why_this: Phase 2 removed fallback breaking daemon startup; auto-migration enables self-healing
- alternatives_considered: Revert to config.env (rejected: regression); Manual migration script (rejected: daemon can't self-heal)
- boundary_non_goals: Does not delete config.env; Does not change write_config format; Does not change .gitignore
- residual_risk: If config.env is corrupted, migration will produce invalid config.toml
