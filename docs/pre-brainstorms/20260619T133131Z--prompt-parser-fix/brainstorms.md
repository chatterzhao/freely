# Brainstorm: prompt parser format mismatch blocks all worker launches
## Manager outputs 'Worktree: /path' single-line; parsers expect multi-line 'Worktree:' then '- /path'
## Fix: add single-line patterns + file-location fallback
## Decision: promote
