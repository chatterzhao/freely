# Issue platform sync architecture - verification
- issue_id: `I-20260426-0000-A`

## Implementation Decision Note
- decision: `Unified bin/issue-sync as the sole local→platform bridge. raw-* and I-* issues distinguished by [RAW]/[I-] title prefix + kind/phase labels + metadata body on platforms. I-* body is self-contained summary with links to B1 artifacts (hybrid model).`
- why_this: `Previous implementation was create-only, scattered across 3 scripts, with no raw↔I-* distinction on platforms. The hybrid model (self-contained summary + links) gives platform readers enough context without duplicating pre-brainstorm docs.`
- alternatives_considered: `1) Full self-contained (copy all B1 docs): rejected, duplication. 2) Links only: rejected, platform readers see empty shells. 3) Summary + links (hybrid): chosen.`
- boundary_non_goals: `No platform→local scan changes (task-source-scan.py unchanged). No issue format migration for existing 161 I-* issues (backfill is gradual).`
- residual_risk: `Existing issues lack issue_title frontmatter; _issue_title() fallback chain covers this. Gitee operations untested (token-dependent).`

## Verification
- bash -n: `pass` (freely, pr-merge-guarded, issue-sync)
- bin/issue-sync status I-20260426-0000-A: `pass` (reads frontmatter, shows platform_ids)
- chat --issue raw-* redirect: `pass` (detects absorbed_into, routes to I-*)
- pr-merge-guarded post-merge sync: `pass` (detects changed issues in merge diff)
- ISSUES.md deleted: `pass` (no code references, 0 grep hits)
