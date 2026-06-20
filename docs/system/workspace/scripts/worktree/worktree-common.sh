#!/usr/bin/env bash
set -euo pipefail

freely_wt_current_branch() {
  git symbolic-ref --quiet --short HEAD || true
}

freely_wt_is_test_pre_merge_branch() {
  local branch="${1:-}"
  [[ "$branch" == test-pre-merge-* ]]
}

freely_wt_first_test_pre_merge_branch() {
  git for-each-ref --format='%(refname:short)' 'refs/heads/test-pre-merge-*' 2>/dev/null | head -n 1
}

freely_wt_primary_worktree() {
  local _wt_raw
  _wt_raw="$(git worktree list --porcelain 2>/dev/null || true)"
  printf '%s\n' "$_wt_raw" | awk '/^worktree / {print $2; exit}'
}

freely_wt_current_path() {
  pwd -P
}

freely_wt_is_primary_worktree() {
  local primary current
  primary="$(freely_wt_primary_worktree)"
  current="$(freely_wt_current_path)"
  [[ "$current" == "$primary" ]]
}

freely_wt_pick_parking_branch() {
  local test_pre_merge_branch=""
  if git show-ref --verify --quiet refs/heads/develop; then
    echo "develop"
  elif test_pre_merge_branch="$(freely_wt_first_test_pre_merge_branch)" && [[ -n "$test_pre_merge_branch" ]]; then
    echo "$test_pre_merge_branch"
  else
    echo "main"
  fi
}

freely_wt_sanitize_name() {
  local s="$1"
  s="$(printf '%s' "$s" | sed -E 's/[^A-Za-z0-9._-]+/-/g; s/-+/-/g; s/^-+//; s/-+$//')"
  printf '%s' "$s"
}

freely_wt_dir_name_for_branch() {
  local branch="$1"
  local safe prefix stamp suffix dir_name
  safe="$(freely_wt_sanitize_name "$branch")"

  prefix="$(printf '%s\n' "$safe" | sed -nE 's/^(.*[^0-9-])-?([0-9]{8}-[0-9]{4,6})(-.*)?$/\1/p')"
  stamp="$(printf '%s\n' "$safe" | sed -nE 's/^(.*[^0-9-])-?([0-9]{8}-[0-9]{4,6})(-.*)?$/\2/p')"
  suffix="$(printf '%s\n' "$safe" | sed -nE 's/^(.*[^0-9-])-?([0-9]{8}-[0-9]{4,6})(-(.*))?$/\4/p')"

  if [[ -z "$stamp" ]]; then
    prefix="$(printf '%s\n' "$safe" | sed -nE 's/^(.*[^0-9-])-?([0-9]{8})(-.*)?$/\1/p')"
    stamp="$(printf '%s\n' "$safe" | sed -nE 's/^(.*[^0-9-])-?([0-9]{8})(-.*)?$/\2/p')"
    suffix="$(printf '%s\n' "$safe" | sed -nE 's/^(.*[^0-9-])-?([0-9]{8})(-(.*))?$/\4/p')"
  fi

  if [[ -z "$stamp" || -z "$prefix" ]]; then
    printf '%s' "$safe"
    return 0
  fi

  dir_name="$stamp"
  [[ -n "$prefix" ]] && dir_name="${dir_name}-${prefix}"
  [[ -n "$suffix" ]] && dir_name="${dir_name}-${suffix}"
  freely_wt_sanitize_name "$dir_name"
}

freely_wt_root_dir() {
  local primary repo_name parent_dir
  primary="$(freely_wt_primary_worktree)"
  repo_name="$(basename "$primary")"
  parent_dir="$(dirname "$primary")"
  echo "${parent_dir}/${repo_name}-worktrees"
}

freely_wt_repo_name() {
  basename "$(freely_wt_primary_worktree)"
}

freely_wt_relative_root_dir() {
  echo "../$(freely_wt_repo_name)-worktrees"
}

freely_wt_assert_strict_root() {
  local root primary
  root="$(freely_wt_root_dir)"
  primary="$(freely_wt_primary_worktree)"
  case "$root" in
    "$primary"|"$primary"/*)
      cat <<MSG >&2
[HOOK] Worktree root invalid: '$root'
Rules:
- worktree root must be sibling to project: <project_parent>/<project_name>-worktrees
- creating worktrees inside project directory is forbidden
MSG
      return 1
      ;;
  esac
}

freely_wt_target_path_for_branch() {
  local branch="$1"
  local safe root
  safe="$(freely_wt_dir_name_for_branch "$branch")"
  root="$(freely_wt_root_dir)"
  echo "${root}/${safe}"
}

freely_wt_relative_target_for_branch() {
  local branch="$1"
  local safe root
  safe="$(freely_wt_dir_name_for_branch "$branch")"
  root="$(freely_wt_relative_root_dir)"
  echo "${root}/${safe}"
}

freely_wt_existing_for_branch() {
  local branch="$1" _wt_raw
  _wt_raw="$(git worktree list --porcelain 2>/dev/null || true)"
  printf '%s\n' "$_wt_raw" | awk -v b="refs/heads/$branch" '
    $1=="worktree" {wt=$2}
    $1=="branch" && $2==b {print wt; exit}
  '
}

freely_wt_path_in_root() {
  local candidate_path="$1"
  local root
  root="$(freely_wt_root_dir)"
  [[ "$candidate_path" == "$root" || "$candidate_path" == "$root"/* ]]
}

freely_wt_assert_existing_in_strict_root() {
  local branch="$1"
  local existing
  existing="$(freely_wt_existing_for_branch "$branch")"
  if [[ -n "$existing" && "$existing" == "$(freely_wt_primary_worktree)" ]]; then
    return 0
  fi
  [[ -z "$existing" ]] && return 0
  freely_wt_path_in_root "$existing" && return 0
  cat <<MSG >&2
[HOOK] Existing worktree path invalid for branch '$branch':
  $existing
Rules:
- use sibling root only: <project_parent>/<project_name>-worktrees
MSG
  return 1
}

freely_wt_validate_branch_base() {
  local b="$1"
  case "$b" in
    feature/premerge-*)
      local test_pre_merge_branch=""
      test_pre_merge_branch="$(freely_wt_first_test_pre_merge_branch)"
      if [[ -n "$test_pre_merge_branch" ]]; then
        git merge-base --is-ancestor "$test_pre_merge_branch" "$b"
      else
        git merge-base --is-ancestor develop "$b"
      fi
      ;;
    feature/*)
      git show-ref --verify --quiet refs/heads/develop || return 0
      git merge-base --is-ancestor develop "$b"
      ;;
    release/*)
      git show-ref --verify --quiet refs/heads/develop || return 0
      git merge-base --is-ancestor develop "$b"
      ;;
    hotfix/*)
      git show-ref --verify --quiet refs/heads/main || return 0
      git merge-base --is-ancestor main "$b"
      ;;
    *)
      return 0
      ;;
  esac
}

freely_wt_resolve_target_path() {
  local branch="$1"
  local target hash_suffix
  target="$(freely_wt_target_path_for_branch "$branch")"
  if [[ -e "$target" ]]; then
    hash_suffix="$(printf '%s' "$branch" | sha1sum | awk '{print substr($1,1,8)}')"
    echo "${target}-${hash_suffix}"
    return 0
  fi
  echo "$target"
}
