# File size guidelines - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Add file size guidelines to AGENTS.md. Code 500/1000 (warn/error). Docs 500 warn. Add bin/check-file-size script.`
- why_this: `freely runtime at 20K lines is unhealthy. Guidelines prevent future files from growing unchecked.`
- alternatives_considered: `1) Linter integration: rejected, too heavy for now. 2) Only AGENTS.md: rejected, need automated check. 3) Guidelines + script: chosen.`
- boundary_non_goals: `No enforcement on legacy files. No refactoring of existing large files.`
- residual_risk: `Script check is advisory. Future gate integration would make it blocking.`
