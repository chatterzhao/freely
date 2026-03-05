#!/usr/bin/env bash
set -euo pipefail

freely_wt_current_branch() {
  git symbolic-ref --quiet --short HEAD || true
}

freely_wt_primary_worktree() {
  git worktree list --porcelain | awk '/^worktree / {print $2; exit}'
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
  if git show-ref --verify --quiet refs/heads/develop; then
    echo "develop"
  else
    echo "main"
  fi
}

freely_wt_sanitize_name() {
  local s="$1"
  s="$(printf '%s' "$s" | sed -E 's/[^A-Za-z0-9._-]+/-/g; s/-+/-/g; s/^-+//; s/-+$//')"
  printf '%s' "$s"
}

freely_wt_root_dir() {
  local primary repo_name parent_dir
  primary="$(freely_wt_primary_worktree)"
  repo_name="$(basename "$primary")"
  parent_dir="$(dirname "$primary")"
  echo "${parent_dir}/${repo_name}-worktrees"
}

freely_wt_assert_strict_root() {
  local root primary
  root="$(freely_wt_root_dir)"
  primary="$(freely_wt_primary_worktree)"
  case "$root" in
    /tmp|/tmp/*)
      cat <<MSG >&2
[HOOK] Worktree root invalid: '$root'
Rules:
- worktree root must be sibling to project: <project_parent>/<project_name>-worktrees
- temp paths (/tmp) are forbidden
MSG
      return 1
      ;;
  esac
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
  safe="$(freely_wt_sanitize_name "$branch")"
  root="$(freely_wt_root_dir)"
  echo "${root}/${safe}"
}

freely_wt_existing_for_branch() {
  local branch="$1"
  git worktree list --porcelain | awk -v b="refs/heads/$branch" '
    $1=="worktree" {wt=$2}
    $1=="branch" && $2==b {print wt; exit}
  '
}

freely_wt_path_in_root() {
  local path="$1"
  local root
  root="$(freely_wt_root_dir)"
  [[ "$path" == "$root" || "$path" == "$root"/* ]]
}

freely_wt_assert_existing_in_strict_root() {
  local branch="$1"
  local existing
  existing="$(freely_wt_existing_for_branch "$branch")"
  [[ -z "$existing" ]] && return 0
  freely_wt_path_in_root "$existing" && return 0
  cat <<MSG >&2
[HOOK] Existing worktree path invalid for branch '$branch':
  $existing
Rules:
- use sibling root only: <project_parent>/<project_name>-worktrees
- temp paths and other fallback locations are forbidden
MSG
  return 1
}

freely_wt_validate_branch_base() {
  local b="$1"
  case "$b" in
    feature/*|release/*)
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
