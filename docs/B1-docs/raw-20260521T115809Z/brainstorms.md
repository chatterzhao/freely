# Brainstorm: pr-merge-guarded forbidden branch name

## Context
Merge commit shows "Merge branch 'forbidden'" instead of actual source branch name.

## Analysis
Line 307 in pr-merge-guarded: `render_merge_message "pr-merge-guarded" "forbidden" "$source_branch" "" "" ""`
The function only reads $1 (merge_path) and $2 (source_branch). "forbidden" fills $2.

## Fix
Remove "forbidden" parameter: `render_merge_message "pr-merge-guarded" "$source_branch"`
