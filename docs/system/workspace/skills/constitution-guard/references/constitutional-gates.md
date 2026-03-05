# Constitutional Gates

- Branch and merge paths must follow constitution table.
- Promotion to `develop` must be gated by executed `TEST` evidence (including integration acceptance), not `PRE_TEST` alone.
- Protected branches remain add/commit blocked.
- Worktree root must be sibling `{project-name}-worktrees`.
- No worktree inside project root.
- Before merge/promotion/release/cleanup, `./bin/wt-status-all` must report all worktrees `CLEAN`.
- If third-party API is used, provider contract remains external source of truth and local code must adapt.
- If code/docs diverge, code/test correction is first path; normative doc changes require dedicated feature/worktree plus linked implementation evidence.
- Version stage tags follow branch/stage mapping.
- Recovery, subagent, and backup requirements remain active.
