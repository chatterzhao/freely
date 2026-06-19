# Pre-Tests: ai-auth Template Config Files

## Acceptance Target
Verify all 7 acceptance criteria are met

## Testing Layer
- Template file syntax validation
- `freely init` integration test
- Cross-reference link check

## Target Environment
- Local development worktree
- Any new `freely init` project

## Required Evidence

### TC-1: Template files exist
- [ ] `templates/ai-auth/claude-apikey-EXAMPLE/settings.json.example` — valid JSON
- [ ] `templates/ai-auth/codex-account-EXAMPLE/config.toml.example` — valid TOML
- [ ] `templates/ai-auth/opencode-apikey-EXAMPLE/settings.json.example` — valid JSON
- [ ] `templates/ai-auth/README.md` — renders correctly
- [ ] `templates/ai-auth/zshrc-aliases.example` — readable alias format

### TC-2: freely init integration
- [ ] `freely init --project /tmp/test-project` creates `.freely/ai-auth/`
- [ ] Directory structure matches template source
- [ ] Hint message printed to stdout

### TC-3: Cross-references
- [ ] `tool-config-matrix.md` references templates/ai-auth/
- [ ] `auth-setup.md` references templates/ai-auth/

## Blocker Taxonomy
| Blocker Type | Check |
|-------------|-------|
| definition_missing | Pre-tests cover all 7 AC items |
| commands_only | Specific test commands listed above |
| evidence_plan_missing | Evidence format specified |
| execution_pending_or_failed | N/A - pre-execution |
