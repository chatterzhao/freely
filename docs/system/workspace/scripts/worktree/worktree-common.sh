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

# ── Dev↔Test consistency gate ─────────────────────────────
# Called by pr-create-guarded, pr-review-guarded, pr-merge-guarded, wt-close.
# Checks that the dev worktree and its paired test worktree have identical commits.
# If not → blocks with merge/cherry-pick + re-run test-GREEN guidance.
#
# Usage: freely_wt_assert_dev_test_consistent <raw_key>
#   raw_key: timestamp portion of the raw key (e.g. 20260629T025659Z)
#
# Exit 0 if consistent (or no test worktree exists).
# Exit 1 with a detailed error message if inconsistent.
freely_wt_assert_dev_test_consistent() {
  local _raw_key="$1"
  [[ -n "$_raw_key" ]] || return 0

  # Find the test worktree for this raw key
  local _test_wt
  _test_wt=$(git worktree list --porcelain 2>/dev/null | awk -v k="test-pre-merge-$_raw_key" '
    $1=="worktree" { wt=$2 }
    $1=="branch" && $2 ~ k { print wt; exit }
  ')
  [[ -z "$_test_wt" || ! -d "$_test_wt" ]] && return 0  # no test worktree, skip

  # Find the dev worktree (fix/* or feature/* with same raw key)
  local _dev_wt _dev_branch
  while IFS= read -r line; do
    case "$line" in
      worktree*) _dev_wt="${line#worktree }" ;;
      branch*)
        local _br="${line#branch }"
        case "$_br" in
          *fix/raw-*$_raw_key*|*feature/raw-*$_raw_key*)
            _dev_branch="${_br#refs/heads/}"
            break
            ;;
        esac
        _dev_wt=""
        ;;
    esac
  done < <(git worktree list --porcelain 2>/dev/null)

  [[ -z "$_dev_wt" || -z "$_dev_branch" ]] && return 0  # no dev worktree, skip

  # Check 1: test has commits not in dev
  local _missing
  _missing=$(git -C "$_test_wt" log --oneline --no-merges "$_dev_branch..HEAD" 2>/dev/null || true)
  if [[ -n "$_missing" ]]; then
    cat >&2 <<FREELY_CONSISTENCY_ERR
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  开发与测试工位不一致 — 测试工位有提交未同步到开发工位    ║
╠══════════════════════════════════════════════════════════════╣
║  开发工位: $_dev_wt ($_dev_branch)
║  测试工位: $_test_wt
║                                                              ║
║  以下提交在测试工位但不在开发工位:                              ║
║  $_missing
║                                                              ║
║  请用 merge（首选）或 cherry-pick 同步:                        ║
║    cd $_dev_wt
║    git merge $_dev_branch                                     ║
║    # 或 cherry-pick 特定 commit:                               ║
║    git cherry-pick \$(git -C $_test_wt log --format=%H --no-merges $_dev_branch..HEAD)
║                                                              ║
║  同步后必须重跑 test-GREEN（skill:freely-test-execution）。     ║
║  开发与测试一致 + 全部 green 后才能继续。                       ║
╚══════════════════════════════════════════════════════════════╝
FREELY_CONSISTENCY_ERR
    return 1
  fi

  # Check 2: dev has commits not in test
  _missing=$(git -C "$_test_wt" log --oneline --no-merges "HEAD..$_dev_branch" 2>/dev/null || true)
  if [[ -n "$_missing" ]]; then
    cat >&2 <<FREELY_CONSISTENCY_ERR
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  开发与测试工位不一致 — 开发工位有提交未同步到测试工位    ║
╠══════════════════════════════════════════════════════════════╣
║  开发工位: $_dev_wt ($_dev_branch)
║  测试工位: $_test_wt
║                                                              ║
║  开发与测试工位必须一致，否则测试结果没有意义——                  ║
║  测的不是最终要合并的代码。                                    ║
║                                                              ║
║  以下提交在开发工位但不在测试工位:                              ║
║  $_missing
║                                                              ║
║  请用 merge（首选）或 cherry-pick 同步:                        ║
║    cd $_test_wt
║    git merge $_dev_branch                                     ║
║    # 或 cherry-pick 特定 commit:                               ║
║    git cherry-pick \$(git -C $_dev_wt log --format=%H --no-merges HEAD..$_dev_branch)
║                                                              ║
║  同步后必须在测试工位重跑 test-GREEN（skill:freely-test-execution）。
║  全部 passed 后才能继续。                                      ║
╚══════════════════════════════════════════════════════════════╝
FREELY_CONSISTENCY_ERR
    return 1
  fi

  return 0
}
