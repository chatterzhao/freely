# Implementation Decision Note: ai-auth Template Configs
- issue_id: I-20260616T140126Z-A
- kind: decision-note

## Decision
Create template config files under `templates/ai-auth/` with `.example` suffix, covering three tool families (claude-apikey, codex-account, opencode-apikey). Integrate with `freely init` for automated deployment.

## Why This
- Template-first approach avoids committing secrets while providing working examples
- `.example` suffix prevents accidental use as live config
- Matches existing slot system conventions (naming, directory structure)
- `freely init` integration ensures templates reach users with minimal friction

## Alternatives Considered
1. **Live config creation during init**: Risk of creating invalid slots; user would need to edit anyway
2. **Online documentation only**: Users must context-switch to browser; no local reference
3. **Single example file per tool**: Incomplete coverage; users need templates for all common auth modes

## Boundary / Non-Goals
- No automatic slot validation against templates
- No migration path for existing slots
- No kiro-cli or cc templates (future work)

## Residual Risk
- Template drift: if slot config format changes, examples must be updated
- Overwrite on re-init could lose user annotations (mitigated by `.example` suffix — users copy, not edit)
