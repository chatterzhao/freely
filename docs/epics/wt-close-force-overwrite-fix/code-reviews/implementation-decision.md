# Implementation Decision: wt-close --force frontmatter guard
- issue_id: I-20260617T160003Z-A
- decision: Add phase_state check in wt-close Phase 3 — skip force-close trace if already absorbed by pr-merge-guarded
- why_this: pr-merge-guarded writes correct absorption metadata into merge commit. wt-close --force was unconditionally overwriting it, leaving develop dirty with inaccurate frontmatter. A single if-guard fixes the regression without changing any other behavior.
- alternatives_considered: Remove Phase 3 entirely — rejected, still needed for worktrees closed without pr-merge-guarded (e.g., abandoned work). Move Phase 3 after Phase 3.5 — rejected, Phase 3.5 is just a comment.
- boundary_non_goals: Not changing how pr-merge-guarded writes frontmatter. Not changing non-force wt-close path.
- residual_risk: None. Guard only triggers when phase_state is already absorbed, which means pr-merge-guarded already handled it.
