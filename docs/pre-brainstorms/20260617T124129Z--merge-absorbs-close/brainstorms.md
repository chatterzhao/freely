# Brainstorm: pr-merge-guarded absorbs wt-close frontmatter
## Discovery
wt-close commits frontmatter on develop with FREELY_SKIP_IBM_GATE=1, leaves dirty state.
Correct design: pr-merge-guarded writes frontmatter into merge commit, wt-close just removes worktree.
## Decision
Promote. pr-merge-guarded: _absorb_close_frontmatter before push. wt-close: remove commit logic.
