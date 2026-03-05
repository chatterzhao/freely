# Constitutional Gates

- Branch and merge paths must follow constitution table.
- Promotion to `develop` must be gated by executed `TEST` evidence (including integration acceptance), not `PRE_TEST` alone.
- Protected branches remain add/commit blocked.
- Worktree root must be sibling `{project-name}-worktrees`.
- No worktree inside project root.
- Version stage tags follow branch/stage mapping.
- Recovery, subagent, and backup requirements remain active.
