#!/usr/bin/env bash
set -euo pipefail

[[ -f "./bin/worktree-common.sh" ]] || exit 0
# shellcheck disable=SC1091
source ./bin/worktree-common.sh

branch="$(freely_wt_current_branch)"
[[ -n "$branch" ]] || exit 0

case "$branch" in
  main|develop|pre-test-merge)
    cat <<MSG
[HOOK] Commit blocked: direct development on '$branch' is forbidden.
This repo enforces worktree mode for feature development.
Use the standard git worktree flow from the project root:

Run:
  cd <your-project-name-path>
  git worktree add -b feature/<task-name> ../<your-project-name>-worktrees/feature-<task-name> develop
  cd ../<your-project-name>-worktrees/feature-<task-name>

The final 'develop' argument already selects the correct base branch.

When the work is finished and merged, clean up with:
  git worktree remove ../<your-project-name>-worktrees/feature-<task-name>
  git branch -d feature/<task-name>

If you skip this workflow, hooks will create the worktree when possible and print guidance.
Do not keep committing in the current directory.
Policy source: docs/CONSTITUTION.md §2
MSG
    exit 1
    ;;
esac

if ! freely_wt_is_primary_worktree; then
  exit 0
fi

if ! freely_wt_validate_branch_base "$branch"; then
  cat <<MSG
[HOOK] Commit blocked: branch '$branch' base check failed.
Expected:
  feature/* from develop
  feature/premerge-* from pre-test-merge (or develop when pre-test-merge is not active)
  release/* from develop
  hotfix/* from main
Policy source: docs/CONSTITUTION.md §2
MSG
  exit 1
fi

existing_for_branch="$(freely_wt_existing_dedicated_for_branch "$branch")"
if [[ -n "$existing_for_branch" ]]; then
  rel_target="$(freely_wt_relative_target_for_branch "$branch")"
  cat <<MSG
[HOOK] Commit blocked in primary worktree.
Branch '$branch' has dedicated sibling worktree:
  $existing_for_branch

Start work in worktree:
  cd "$existing_for_branch"

Standard cleanup after merge:
  git worktree remove ${rel_target}
  git branch -d "$branch"
Policy source: docs/CONSTITUTION.md §2
MSG
  git worktree list
  exit 1
fi

rel_target="$(freely_wt_relative_target_for_branch "$branch")"
cat <<MSG
[HOOK] Commit blocked in primary worktree.
No dedicated sibling worktree found for '$branch'.

Create it from the project root with the standard command:
  cd <your-project-name-path>
  git worktree add ../<your-project-name>-worktrees/${branch//\//-} "$branch"
  cd ../<your-project-name>-worktrees/${branch//\//-}

When the work is finished and merged:
  git worktree remove ${rel_target}
  git branch -d "$branch"
Policy source: docs/CONSTITUTION.md §2
MSG
exit 1
