# Pre-Tests: skill standardization
- issue_id: I-20260508T005431Z-A

## Unit
- acceptance target: `deploy-skills --dry-run shows all skills OK`
- testing layer: unit
- target environment: feature/raw-20260508T005431Z-skill-standardize
- required evidence: `deployed=33 updated=0 failed=0`
- blocker taxonomy: execution_pending_or_failed

## Unit
- acceptance target: `chat-issue-routing has name/description frontmatter`
- testing layer: unit
- target environment: feature/raw-20260508T005431Z-skill-standardize
- required evidence: `head -6 SKILL.md shows frontmatter`
- blocker taxonomy: execution_pending_or_failed

## Unit
- acceptance target: `continuity-watchdog uses relative paths for cross-skill refs`
- testing layer: unit
- target environment: feature/raw-20260508T005431Z-skill-standardize
- required evidence: `grep "\.\./" SKILL.md`
- blocker taxonomy: execution_pending_or_failed

## Integration
- acceptance target: `AGENTS.md has Skill 管理 section with deploy rule`
- testing layer: integration
- target environment: feature/raw-20260508T005431Z-skill-standardize
- required evidence: `grep "deploy-skills" AGENTS.md`
- blocker taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: Doc-only change. deploy-skills --dry-run confirms all 33 skills synced.

## Acceptance Items
### AT-001 deploy script
- id: deploy-script
- requirement: deploy-skills deploys only changed skills
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: inline
- status: pass
- artifact_ref: bin/deploy-skills
