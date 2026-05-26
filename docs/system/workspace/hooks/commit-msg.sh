#!/usr/bin/env bash
set -euo pipefail

commit_msg_file="$1"

[[ -f "$commit_msg_file" ]] || exit 0

msg="$(cat "$commit_msg_file")"

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
[[ -n "$branch" ]] || exit 0

git_dir="$(git rev-parse --git-dir 2>/dev/null || true)"

subject="$(head -n1 "$commit_msg_file" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')"
subject_len="${#subject}"

[[ -n "$subject" ]] || {
  cat <<MSG
[HOOK] Commit blocked: empty subject line.
MSG
  exit 1
}

is_protected_branch() {
  case "$1" in
    main|develop|test-pre-merge-*) return 0 ;;
  esac
  return 1
}

is_merge_in_progress() {
  [[ -n "$git_dir" && -f "$git_dir/MERGE_HEAD" ]]
}

is_merge_commit_msg() {
  [[ "$subject" =~ ^Merge[[:space:]]branch[[:space:]] ]]
}

is_merge_commit() {
  is_merge_in_progress || is_merge_commit_msg
}

if ! is_merge_commit; then
  if [[ "$subject_len" -gt 100 ]]; then
    cat <<MSG
[HOOK] Commit blocked: subject line exceeds 100 characters ($subject_len).
MSG
    exit 1
  elif [[ "$subject_len" -gt 72 ]]; then
    echo "[HOOK] Warning: subject line exceeds 72 characters ($subject_len)." >&2
  fi

  if [[ "$subject" =~ \.$ ]]; then
    cat <<MSG
[HOOK] Commit blocked: subject line must not end with a period.
MSG
    exit 1
  fi

  total_lines="$(wc -l < "$commit_msg_file" | tr -d ' ')"
  if [[ "$total_lines" -gt 1 ]]; then
    second_line="$(sed -n '2p' "$commit_msg_file")"
    if [[ -n "${second_line}" ]]; then
      cat <<MSG
[HOOK] Commit blocked: second line must be blank (separate subject from body).
MSG
      exit 1
    fi
  fi

  if grep -q '[[:space:]]$' "$commit_msg_file"; then
    cat <<MSG
[HOOK] Commit blocked: trailing whitespace detected.
MSG
    exit 1
  fi

  exit 0
fi

if is_protected_branch "$branch"; then
  merge_path="$(printf '%s\n' "$msg" | grep -E '^Freely-Merge-Path:' | tail -1 | sed 's/^Freely-Merge-Path: *//')"
  bypass_mode="$(printf '%s\n' "$msg" | grep -E '^Freely-Bypass-Mode:' | tail -1 | sed 's/^Freely-Bypass-Mode: *//')"
  source_branch_t="$(printf '%s\n' "$msg" | grep -E '^Freely-Source-Branch:' | tail -1 | sed 's/^Freely-Source-Branch: *//')"

  [[ -n "$merge_path" ]] || {
    cat <<MSG
[HOOK] Commit blocked: protected branch merge requires Freely-Merge-Path trailer.
MSG
    exit 1
  }

  case "$merge_path" in
    pr-merge-guarded|pr-merge-guarded-complete) ;;
    *)
      cat <<MSG
[HOOK] Commit blocked: invalid Freely-Merge-Path '$merge_path'.
Valid: pr-merge-guarded, pr-merge-guarded-complete
MSG
      exit 1
      ;;
  esac

  [[ -n "$bypass_mode" ]] || {
    cat <<MSG
[HOOK] Commit blocked: protected branch merge requires Freely-Bypass-Mode trailer.
MSG
    exit 1
  }

  case "$bypass_mode" in
    forbidden) ;;
    *)
      cat <<MSG
[HOOK] Commit blocked: invalid Freely-Bypass-Mode '$bypass_mode'.
Valid: forbidden
MSG
      exit 1
      ;;
  esac

  [[ -n "$source_branch_t" ]] || {
    cat <<MSG
[HOOK] Commit blocked: protected branch merge requires Freely-Source-Branch trailer.
MSG
    exit 1
  }

fi
