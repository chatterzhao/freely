#!/usr/bin/env bash
set -euo pipefail

state="${1:-}"
[[ "$state" == "prepared" ]] || exit 0

zero_oid='0000000000000000000000000000000000000000'

protected_branch_ref() {
  local refname="$1"
  case "$refname" in
    refs/heads/main|refs/heads/develop|refs/heads/test-pre-merge-*) return 0 ;;
  esac
  return 1
}

protected_branch_name() {
  local refname="$1"
  printf '%s\n' "${refname#refs/heads/}"
}

wt_managed_branch_ref() {
  local refname="$1"
  case "$refname" in
    refs/heads/feature/*|refs/heads/hotfix/*|refs/heads/fix/*|refs/heads/test-pre-merge-*) return 0 ;;
  esac
  return 1
}

commit_has_canonical_receipt() {
  local commit="$1"
  local body=""
  body="$(git show --no-patch --format=%B "$commit" 2>/dev/null || true)"
  [[ -n "$body" ]] || return 1
  grep -Eq '^Freely-Merge-Path: (merge-guarded|merge-guarded-complete|merge-guarded-break-glass)$' <<<"$body"
}

commit_is_merge_commit() {
  local commit="$1"
  local parents=""
  parents="$(git show --no-patch --format=%P "$commit" 2>/dev/null || true)"
  [[ -n "$parents" ]] || return 1
  [[ "$(wc -w <<<"$parents" | tr -d ' ')" -ge 2 ]]
}

while read -r old_oid new_oid refname; do
  [[ -n "${refname:-}" ]] || continue

  # ── Branch creation guard: block manual git worktree add for managed branches ──
  if [[ "$old_oid" == "$zero_oid" ]]; then
    if wt_managed_branch_ref "$refname"; then
      if [[ "${FREELY_WT_CREATE:-}" != "1" ]]; then
        branch_name="$(protected_branch_name "$refname")"
        cat <<MSG >&2
[HOOK] Branch creation blocked: '$branch_name' must be created through ./bin/wt-create.
Direct 'git worktree add' / 'git branch' for feature/*, hotfix/*, fix/*, and test-pre-merge-* branches is not allowed.
Use './bin/wt-create --raw-key <key> --prefix <fix|feature> --skill <path> --slug <slug>' instead.
This ensures every worktree has a valid issue, correct naming, and governance traceability.
Policy source: docs/CONSTITUTION.md §2, docs/LAWS.md §2
MSG
        exit 1
      fi
    fi
    continue
  fi

  protected_branch_ref "$refname" || continue

  if [[ "$new_oid" == "$zero_oid" ]]; then
    continue
  fi

  # No-op: ref points to the same commit (e.g. git reset --hard HEAD)
  if [[ "$old_oid" == "$new_oid" ]]; then
    continue
  fi

  if commit_is_merge_commit "$new_oid" && commit_has_canonical_receipt "$new_oid"; then
    continue
  fi

  branch_name="$(protected_branch_name "$refname")"
  cat <<MSG >&2
[HOOK] Ref update blocked: protected branch '$branch_name' cannot advance to commit '$new_oid' without a canonical protected-merge receipt.
Direct fast-forward, reset, and other ref-only updates are not lawful protected-branch merge entrypoints.
Create a receipt-bearing protected merge commit through ./bin/merge-guarded instead.
Policy source: docs/CONSTITUTION.md §2, docs/LAWS.md §2
MSG
  exit 1
done

exit 0
