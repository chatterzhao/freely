# Pre-Tests: freely-db-cli + AGENTS.md + hook fix

## Acceptance Items

### AI-1: freely-db-cli db.ping returns pong
- **Given**: freely-db daemon is running
- **When**: `python3 docs/system/workspace/scripts/runtime/freely-db-cli --project <project> db.ping`
- **Then**: Output is `pong` (not IndentationError)
- **adequacy**: `verified` — manually confirmed during daemon start sequence

### AI-2: AGENTS.md workflow starts with feedback/scan branching
- **Given**: Read AGENTS.md §核心开发流程
- **When**: Compare with `skill:freely-feat-execution` flow definition
- **Then**: Entry section shows feedback and scan as OR-branch entry points, wt-create as stage 1
- **adequacy**: `verified` — structural alignment confirmed

### AI-3: pre-commit hook message names skills
- **Given**: Attempt to commit on develop
- **When**: Hook blocks the commit
- **Then**: Message includes `skill:freely-fix-execution` and `skill:freely-feat-execution`, plus anti-bypass warning
- **adequacy**: `verified` — string match confirmed in message text

## Verification Notes
- All three fixes are single-line or documentation changes, no regression risk
- No runtime behavior changes — pre-tests are structural verification
