# Candidates: ai-auth Template Configs

**raw-key**: 20260616T140126Z

## Candidate C-20260616T140126Z-1: ai-auth Template Config Files

**status**: proposed
**milestone**: unassigned
**acceptance_criteria**:
1. `templates/ai-auth/claude-apikey-EXAMPLE/settings.json.example` exists with correct model, env, permissions
2. `templates/ai-auth/codex-account-EXAMPLE/config.toml.example` exists with correct config
3. `templates/ai-auth/opencode-apikey-EXAMPLE/settings.json.example` exists with provider config notes
4. `templates/ai-auth/README.md` exists with slot system overview
5. `templates/ai-auth/zshrc-aliases.example` exists with aliases
6. `freely init` copies templates to `.freely/ai-auth/`
7. Skill references updated (tool-config-matrix.md, auth-setup.md)

**promotion_gate**:
- All 7 template files created and reviewed
- `freely init` integration tested
- Cross-references validated in skill docs

**open_questions**:
- Overwrite vs. skip on re-init for `.freely/ai-auth/`
- Whether to include kiro-cli templates
- Permission matrix scope in examples

**advisory**: Candidate is straightforward with clear scope. Recommend promote to I-20260616T140126Z-A after acceptance review.

## Decision Log

| Date | Decision | Reason |
|------|----------|--------|
| 2026-06-18 | proposed | Initial brainstorm complete, awaiting acceptance review |
