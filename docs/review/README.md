# Review Records

All review outputs must be saved under this directory.

## Filename Convention (Hard Requirement)

`<timestamp>--<reviewer>--<branch>--<topic>.md`

- `timestamp`: `YYYYMMDD-HHMMSS`
- `reviewer`: tool and model identifier (for example `codex-gpt5-3-high`)
- `branch`: current git branch name
- `topic`: short review scope

## Character Rules

- Allowed: `a-z`, `0-9`, `-`
- Unsupported characters must be replaced with `-`
- Collapse repeated `-` where possible

## Example

`20260228-141530--codex-gpt5-3-high--feature-watch-recovery--hook-policy-review.md`

## Required Header Fields

- Reviewed At (ISO timestamp)
- Reviewer
- Branch
- Commit (if available)
- Scope
- Findings
- Risks
- Decision
