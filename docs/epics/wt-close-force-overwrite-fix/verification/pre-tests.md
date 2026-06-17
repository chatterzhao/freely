# Pre-Tests: wt-close --force frontmatter guard

## Acceptance Items

### AI-1: wt-close --force skips when absorbed
- **Given**: raw issue phase_state=absorbed (pr-merge-guarded done)
- **When**: wt-close --force <branch>
- **Then**: "frontmatter already absorbed by pr-merge-guarded, skipping force-close trace"
- **adequacy**: verified

### AI-2: wt-close --force still writes when not absorbed
- **Given**: raw issue phase_state != absorbed (e.g., abandoned worktree)
- **When**: wt-close --force <branch>
- **Then**: force_closed trace written
- **adequacy**: verified

### AI-3: develop stays clean
- **Given**: pr-merge-guarded already merged
- **When**: wt-close --force
- **Then**: No dirty files on develop (no frontmatter overwrite)
- **adequacy**: verified
