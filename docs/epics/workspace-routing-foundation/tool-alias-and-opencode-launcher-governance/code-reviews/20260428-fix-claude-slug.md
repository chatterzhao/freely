# Fix Claude session dir slug - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Remove s|^-|| from _tool_session_dir claude slug. The leading / in absolute path becomes leading - in slug.`
- why_this: `Claude stores sessions at ~/.claude/projects/<slug>/ where slug = absolute path with /→-. The old code stripped the leading -, producing wrong path.`
- alternatives_considered: `1) Keep stripping: rejected, path doesn't exist. 2) Remove strip: chosen, matches actual dir.`
- boundary_non_goals: `No change to Codex or OpenCode paths.`
- residual_risk: `None — purely path correction.`
