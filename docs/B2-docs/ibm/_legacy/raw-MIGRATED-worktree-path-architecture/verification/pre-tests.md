# Pre-Tests: worktree path architecture fix

## Acceptance Items

### AI-1: wt-create materializes raw issue to worktree
- **Given**: wt-create --raw-key <key> --source platform
- **When**: worktree created
- **Then**: docs/issues/raw-{key}/issue.md exists IN worktree, not in develop
- **adequacy**: verified

### AI-2: wt-close resolves ROOT_DIR from CWD
- **Given**: wt-close run from any directory
- **When**: ROOT_DIR=$(git rev-parse --show-toplevel)
- **Then**: ROOT_DIR points to current git worktree
- **adequacy**: verified

### AI-3: pr-merge-guarded does not amend develop
- **Given**: merge of fix branch with raw issue
- **When**: pr-merge-guarded completes
- **Then**: No _absorb_close_frontmatter call, develop stays clean
- **adequacy**: verified

### AI-4: pr-create-guarded checks worktree phase_state
- **Given**: pr-create-guarded in worktree
- **When**: raw issue phase_state != absorbed
- **Then**: blocked with guidance message
- **adequacy**: verified

### AI-5: End-to-end — develop never dirty
- **Given**: full fix-execution cycle (wt-create → fix → pr-create → pr-merge → wt-close)
- **When**: all steps complete
- **Then**: develop has zero dirty files from frontmatter operations
- **adequacy**: verified (dogfood test)
