# Fix gh merge receipt
- issue_id: I-20260617T133709Z-A
- decision: Pass receipt as --body to gh pr merge
- why_this: --subject drops multiline, hook blocks pull
- alternatives_considered: Amend after merge — rejected: too complex
- residual_risk: None
