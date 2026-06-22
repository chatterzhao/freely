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

_caller_is_wt_create() {
  # Walk process ancestry: check if wt-create is in the parent chain.
  # git worktree add runs git-under-hook → this hook → check if any ancestor is wt-create.
  local pid ppid cmd
  pid=$PPID
  while [[ "$pid" -gt 1 ]]; do
    cmd=$(ps -o comm= -p "$pid" 2>/dev/null || true)
    case "$cmd" in
      wt-create|bash*)  # bash* covers "bash ./bin/wt-create" invocation
        # Verify by checking if the process command line contains wt-create
        local full_cmd
        full_cmd=$(ps -o args= -p "$pid" 2>/dev/null || true)
        case "$full_cmd" in
          *wt-create*) return 0 ;;
        esac
        ;;
    esac
    ppid=$(ps -o ppid= -p "$pid" 2>/dev/null | tr -d ' ' || true)
    [[ -n "$ppid" && "$ppid" -gt 0 ]] || break
    pid=$ppid
  done
  return 1
}

_caller_is_wt_close() {
  # Walk process ancestry: check if wt-close is in the parent chain.
  local pid ppid cmd
  pid=$PPID
  while [[ "$pid" -gt 1 ]]; do
    cmd=$(ps -o comm= -p "$pid" 2>/dev/null || true)
    case "$cmd" in
      wt-close|bash*)
        local full_cmd
        full_cmd=$(ps -o args= -p "$pid" 2>/dev/null || true)
        case "$full_cmd" in
          *wt-close*) return 0 ;;
        esac
        ;;
    esac
    ppid=$(ps -o ppid= -p "$pid" 2>/dev/null | tr -d ' ' || true)
    [[ -n "$ppid" && "$ppid" -gt 0 ]] || break
    pid=$ppid
  done
  return 1
}

commit_has_canonical_receipt() {
  local commit="$1"
  local body=""
  body="$(git show --no-patch --format=%B "$commit" 2>/dev/null || true)"
  [[ -n "$body" ]] || return 1
  grep -Eq '^Freely-Merge-Path: (pr-merge-guarded|pr-merge-guarded-complete)$' <<<"$body"
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
  # Skip aborted/no-op transactions where both oids are zero
  if [[ "$old_oid" == "$zero_oid" && "$new_oid" == "$zero_oid" ]]; then
    continue
  fi
  if [[ "$old_oid" == "$zero_oid" ]]; then
    if wt_managed_branch_ref "$refname"; then
      branch_name="$(protected_branch_name "$refname")"
      # Only allow wt-create to create managed branches — verify caller via process tree
      if ! _caller_is_wt_create; then
        cat <<MSG >&2
[HOOK] Branch creation blocked: '$branch_name'

  fix/feature/hotfix/test-pre-merge 分支禁止手动创建。
  完整开发流程（详见 AGENTS.md §核心开发流程）：

  阶段2: 创建 raw issue → ./bin/freely feedback --repo <user/repo> --title '...' --body '...'
  阶段3: 创建工位   → ./bin/wt-create --raw-key <key> --source <platform|chat-inbox|local> \\
                          --skill <freely-fix-execution|freely-feat-execution> --slug <slug>

MSG
        exit 1
      fi
      # Validate branch name contains raw-key for all managed branches
      # fix/feature/hotfix: raw-YYYYMMDDTHHMMSSZ-slug
      # test-pre-merge: test-pre-merge-YYYYMMDDTHHMMSSZ-slug
      if ! echo "$branch_name" | grep -qE '(raw-|I-)?[0-9]{8}[-T][0-9]{4,6}Z[-]'; then
        cat <<'NAME_BLOCK' >&2
[HOOK] Branch name rejected: '$branch_name'

  所有 fix/feature/hotfix/test-pre-merge 分支名必须含 raw-key (YYYYMMDDTHHMMSSZ)。
NAME_BLOCK
        exit 1
      fi
    fi
    continue
  fi

  # Branch deletion: BLOCK for ALL managed branches — must use wt-close
  # Checked BEFORE protected_branch_ref guard so fix/feature/hotfix are also covered.
  if [[ "$new_oid" == "$zero_oid" ]]; then
    if wt_managed_branch_ref "$refname"; then
      # Allow wt-close to delete managed branches
      if _caller_is_wt_close; then
        continue
      fi
      branch_name="$(protected_branch_name "$refname")"
      cat <<'DELETE_BLOCK' >&2
[HOOK] Branch deletion BLOCKED: '$branch_name'

  fix/feature/hotfix/test-pre-merge 分支禁止手动删除。
  必须通过 wt-close 收口（验 phase_state → 关平台 issue → 删 worktree → 删分支）。

  Usage: ./bin/wt-close <branch>

DELETE_BLOCK
      exit 1
    fi
    continue
  fi

  protected_branch_ref "$refname" || continue

  # No-op: ref points to the same commit (e.g. git reset --hard HEAD)
  if [[ "$old_oid" == "$new_oid" ]]; then
    continue
  fi

  if [[ -n "${FREELY_SKIP_IBM_GATE:-}" ]]; then
    # --reason gate: env var bypass must carry valid business reason
    if ! echo "${FREELY_SKIP_IBM_GATE}" | grep -q "^违规绕过门禁中，理由充分，是："; then
      cat >&2 <<'REASON_GATE'
[GATE] 检测到你试图通过 FREELY_SKIP_IBM_GATE 违规绕过门禁

  如果是因为实现没有达到门禁要求，请按要求去完成，而不是想着违规绕过。

  只有确实有合理的业务理由，才允许绕过。
  FREELY_SKIP_IBM_GATE 的值必须匹配格式:
    FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：<业务理由>"

  示例: FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：紧急修复已通过完整治理流程的合并冲突" git ...
REASON_GATE
      exit 1
    fi
    continue
  fi

  if commit_is_merge_commit "$new_oid" && commit_has_canonical_receipt "$new_oid"; then
    continue
  fi

  branch_name="$(protected_branch_name "$refname")"
  cat <<MSG >&2
[HOOK] Ref update blocked: protected branch '$branch_name' cannot advance.

  Target commit:  $new_oid
  Receipt check:  FAILED (Freely-Merge-Path missing or not canonical)

  This block prevents semantic conflicts — merges that git's text-based
  auto-merge accepts but that silently regress prior fixes.

  Diagnostic steps:
    1. Check if the merge overwrote a prior fix:
         git show $new_oid
         git log --oneline $new_oid --not $old_oid | head -5
    2. If the commit IS a protected merge, re-run with pr-merge-guarded:
         ./bin/pr-merge-guarded $branch_name <source-branch>
       This ensures the merge receipt is properly injected.
    3. If this is an emergency bypass, use FREELY_SKIP_IBM_GATE="违规绕过门禁中，理由充分，是：<业务理由>"
       (governance-only changes only — code changes will be rejected).

  Direct fast-forward, reset, and ref-only updates are not lawful
  protected-branch merge entrypoints.
MSG
  exit 1
done

exit 0
