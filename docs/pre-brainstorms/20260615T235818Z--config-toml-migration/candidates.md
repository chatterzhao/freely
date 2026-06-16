# Candidates: config.toml Migration

## C-20260615T235818Z-config-toml

- milestone: M-20260615T235818Z-config-toml-migration
- status: `promoted`
- acceptance_criteria:
  - config.toml as primary format
  - Old config.env backward compatibility (Phase 1)
  - Complete migration — no config.env fallback (Phase 2)
- next_action: Phase 2 merged to develop
- revisit_trigger: If any config.env fallback code is discovered in runtime paths
- promoted_issue_id: I-20260615T235818Z-config-toml
- promoted_issue_path: docs/issues/I-20260615T235818Z-config-toml/issue.md
- promotion_gate:
  - Phase 1: TOML reader + backward compat (completed, merged)
  - Phase 2: Remove all config.env fallback code (this merge)
