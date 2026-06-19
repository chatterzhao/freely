---
issue_id: I-20260616T140126Z-A
name: ai-auth Template Config Files
kind: linked
milestone: M-2026-Q2
epic: ai-auth-template-config
phase_state: completed
verification_artifact_dir: docs/epics/ai-auth-template-config/code-reviews/
acceptance_criteria:
  - templates/ai-auth/claude-apikey-EXAMPLE/settings.json.example exists
  - templates/ai-auth/codex-account-EXAMPLE/config.toml.example exists
  - templates/ai-auth/opencode-apikey-EXAMPLE/settings.json.example exists
  - templates/ai-auth/README.md exists
  - templates/ai-auth/zshrc-aliases.example exists
  - freely init copies templates to .freely/ai-auth/
  - Skill references updated (tool-config-matrix.md, auth-setup.md)
promotion_gate:
  - All 7 template files reviewed
  - freely init integration tested
  - Cross-references validated
source: raw-20260616T140126Z
raw_key: 20260616T140126Z
source_candidate: docs/pre-brainstorms/20260616T140126Z--ai-auth-template/candidates.md
created: 2026-06-18T08:05:54Z
updated: 2026-06-19T06:20:00Z
---
