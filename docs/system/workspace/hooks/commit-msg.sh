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
  cat >&2 <<MSG
[HOOK] Commit blocked: empty subject line.
MSG
  exit 1
}

is_protected_branch() {
  # Receipt-gated merges are ONLY main/develop. test-pre-merge-* is a
  # discardable sandbox: every round syncs dev commits into it with a plain
  # merge, so requiring a guarded-merge receipt there would block all work.
  case "$1" in
    main|develop) return 0 ;;
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
    cat >&2 <<MSG
[HOOK] Commit blocked: subject line exceeds 100 characters ($subject_len).
MSG
    exit 1
  elif [[ "$subject_len" -gt 72 ]]; then
    echo "[HOOK] Warning: subject line exceeds 72 characters ($subject_len)." >&2
  fi

  if [[ "$subject" =~ \.$ ]]; then
    cat >&2 <<MSG
[HOOK] Commit blocked: subject line must not end with a period.
MSG
    exit 1
  fi

  total_lines="$(wc -l < "$commit_msg_file" | tr -d ' ')"
  if [[ "$total_lines" -gt 1 ]]; then
    second_line="$(sed -n '2p' "$commit_msg_file")"
    if [[ -n "${second_line}" ]]; then
      cat >&2 <<MSG
[HOOK] Commit blocked: second line must be blank (separate subject from body).
MSG
      exit 1
    fi
  fi

  if grep -q '[[:space:]]$' "$commit_msg_file"; then
    cat >&2 <<MSG
[HOOK] Commit blocked: trailing whitespace detected.
MSG
    exit 1
  fi

  exit 0
fi

if is_protected_branch "$branch"; then
  # sed (not grep|tail): with `set -euo pipefail`, a missing trailer made the
  # grep pipeline fail and aborted the hook BEFORE printing any rejection
  # reason. sed always succeeds and yields an empty string when absent.
  merge_path="$(printf '%s\n' "$msg" | sed -n 's/^Freely-Merge-Path: *//p' | tail -1)"
  bypass_mode="$(printf '%s\n' "$msg" | sed -n 's/^Freely-Bypass-Mode: *//p' | tail -1)"
  source_branch_t="$(printf '%s\n' "$msg" | sed -n 's/^Freely-Source-Branch: *//p' | tail -1)"

  [[ -n "$merge_path" ]] || {
    cat >&2 <<MSG
[HOOK] Commit blocked: protected branch merge requires Freely-Merge-Path trailer.
MSG
    exit 1
  }

  case "$merge_path" in
    pr-merge-guarded|pr-merge-guarded-complete) ;;
    *)
      cat >&2 <<MSG
[HOOK] Commit blocked: invalid Freely-Merge-Path '$merge_path'.
Valid: pr-merge-guarded, pr-merge-guarded-complete
MSG
      exit 1
      ;;
  esac

  [[ -n "$bypass_mode" ]] || {
    cat >&2 <<MSG
[HOOK] Commit blocked: protected branch merge requires Freely-Bypass-Mode trailer.
MSG
    exit 1
  }

  case "$bypass_mode" in
    forbidden) ;;
    *)
      cat >&2 <<MSG
[HOOK] Commit blocked: invalid Freely-Bypass-Mode '$bypass_mode'.
Valid: forbidden
MSG
      exit 1
      ;;
  esac

  [[ -n "$source_branch_t" ]] || {
    cat >&2 <<MSG
[HOOK] Commit blocked: protected branch merge requires Freely-Source-Branch trailer.
MSG
    exit 1
  }

  # Trailers are just text. Independently require the CONTROLLED handshake
  # written by `freely pr-merge-guarded`: FREELY_GUARDED_MERGE_COMPLETION=1
  # plus a matching freely-guarded-merge-state file in git-dir. Without it a
  # hand merge with self-filled trailers is still rejected.
  if [[ "${FREELY_GUARDED_MERGE_COMPLETION:-0}" != "1" ]]; then
    cat >&2 <<MSG
[HOOK] Commit blocked: protected branch merge lacks the controlled handshake.
Use: freely pr-merge-guarded develop <source-branch>
MSG
    exit 1
  fi

  _state_file="$git_dir/freely-guarded-merge-state"
  if [[ ! -f "$_state_file" ]]; then
    cat >&2 <<MSG
[HOOK] Commit blocked: guarded merge completion state is missing.
Re-run the merge through freely pr-merge-guarded.
MSG
    exit 1
  fi
  _state_source="$(sed -n 's/^source_branch=//p' "$_state_file" | tail -1)"
  _state_target="$(sed -n 's/^target_branch=//p' "$_state_file" | tail -1)"
  _state_bypass="$(sed -n 's/^bypass_mode=//p' "$_state_file" | tail -1)"
  if [[ -z "$_state_source" || -z "$_state_target" || -z "$_state_bypass" ]]; then
    cat >&2 <<MSG
[HOOK] Commit blocked: guarded merge completion state is malformed.
MSG
    exit 1
  fi
  if [[ "$_state_target" != "$branch" || "$_state_source" != "$source_branch_t" ]]; then
    cat >&2 <<MSG
[HOOK] Commit blocked: guarded merge completion state does not match this merge
  state target='$_state_target' source='$_state_source'
  message source='$source_branch_t' branch='$branch'
MSG
    exit 1
  fi

fi
