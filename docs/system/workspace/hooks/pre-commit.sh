#!/usr/bin/env bash
set -euo pipefail

[[ -f "./bin/worktree-common.sh" ]] || exit 0
# shellcheck disable=SC1091
source ./bin/worktree-common.sh

branch="$(freely_wt_current_branch)"
[[ -n "$branch" ]] || exit 0

guarded_state_path="$(git rev-parse --git-dir 2>/dev/null || true)"
if [[ -n "$guarded_state_path" ]]; then
  guarded_state_path="$guarded_state_path/freely-guarded-merge-state"
fi

load_guarded_state() {
  [[ -n "$guarded_state_path" && -f "$guarded_state_path" ]] || return 1
  guarded_state_target=""
  guarded_state_source=""
  guarded_state_bypass=""
  while IFS='=' read -r key value; do
    case "$key" in
      target_branch) guarded_state_target="$value" ;;
      source_branch) guarded_state_source="$value" ;;
      bypass_mode) guarded_state_bypass="$value" ;;
    esac
  done <"$guarded_state_path"
  [[ -n "$guarded_state_target" && -n "$guarded_state_source" && -n "$guarded_state_bypass" ]] || return 1
}

require_valid_guarded_completion_state() {
  load_guarded_state || {
    cat <<MSG
[HOOK] Commit blocked: guarded merge completion state is missing or malformed.
Re-run the merge through ./bin/merge-guarded so hooks can verify a canonical completion handshake.
Policy source: docs/LAWS.md §2D
MSG
    exit 1
  }

  if [[ "$guarded_state_target" != "$branch" ]]; then
    cat <<MSG
[HOOK] Commit blocked: guarded merge completion target '$guarded_state_target' does not match current branch '$branch'.
Policy source: docs/LAWS.md §2D
MSG
    exit 1
  fi

  merge_head="$(git rev-parse -q --verify MERGE_HEAD 2>/dev/null || true)"
  source_sha="$(git rev-parse "$guarded_state_source" 2>/dev/null || true)"
  if [[ -z "$merge_head" || -z "$source_sha" || "$merge_head" != "$source_sha" ]]; then
    cat <<MSG
[HOOK] Commit blocked: guarded merge completion source '$guarded_state_source' does not match MERGE_HEAD.
Policy source: docs/LAWS.md §2D
MSG
    exit 1
  fi
}

if freely_wt_is_test_pre_merge_branch "$branch"; then
  if git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1; then
    if [[ "${FREELY_GUARDED_MERGE_COMPLETION:-0}" == "1" ]]; then
      require_valid_guarded_completion_state
      exit 0
    fi
    cat <<MSG
[HOOK] Commit blocked: raw merge completion on '$branch' is forbidden.
Use the guarded completion path instead:

  ./bin/merge-guarded complete "$branch" <source-branch>

Policy source: docs/LAWS.md §2D
MSG
    exit 1
  fi
  cat <<MSG
[HOOK] Commit blocked: direct development on '$branch' is forbidden.
Test pre-merge batches are ephemeral verification surfaces.
- merge feature branches into this batch for testing
- fix failures back in the source feature worktree
- delete the batch when testing ends

Policy source: docs/CONSTITUTION.md §2
MSG
  exit 1
fi

case "$branch" in
  main|develop)
    if git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1; then
      if [[ "${FREELY_GUARDED_MERGE_COMPLETION:-0}" == "1" ]]; then
        require_valid_guarded_completion_state
        exit 0
      fi
      cat <<MSG
[HOOK] Commit blocked: raw merge completion on '$branch' is forbidden.
Use the guarded completion path instead:

  ./bin/merge-guarded complete "$branch" <source-branch>

Do not finish protected-branch merges with bare 'git commit' or equivalent bypass.
Policy source: docs/LAWS.md §2D
MSG
      exit 1
    fi
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
  if [[ -x "./bin/checkpoint-guard" ]]; then
    set +e
    checkpoint_output="$(./bin/checkpoint-guard --staged-only --fail-on-required 2>&1)"
    checkpoint_rc=$?
    set -e
    if [[ "$checkpoint_rc" -eq 2 ]]; then
      cat <<MSG
[HOOK] Commit blocked: staged change set exceeds checkpoint budget.

$checkpoint_output

Split this commit into issue-aligned atomic batches, or move mixed work into separate worktrees.
Policy source: docs/LAWS.md §2D
MSG
      exit 1
    elif [[ "$checkpoint_rc" -ne 0 ]]; then
      echo "$checkpoint_output" >&2
      exit "$checkpoint_rc"
    fi
  fi
  if [[ -x "./bin/pretests-gate" ]]; then
    set +e
    pretests_output="$(./bin/pretests-gate --staged-only 2>&1)"
    pretests_rc=$?
    set -e
    if [[ "$pretests_rc" -ne 0 ]]; then
      cat <<MSG
[HOOK] Commit blocked: staged issue completion does not satisfy bound pre-tests evidence.

$pretests_output

Keep the issue in a non-completed phase until its bound pre-tests acceptance items are passed and artifact-backed.
Policy source: docs/LAWS.md §2D
MSG
      exit "$pretests_rc"
    fi
  fi
  exit 0
fi

if ! freely_wt_validate_branch_base "$branch"; then
  cat <<MSG
[HOOK] Commit blocked: branch '$branch' base check failed.
Expected:
  feature/* from develop
  feature/premerge-* from the active test-pre-merge-* batch (or develop when no test batch is active)
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
