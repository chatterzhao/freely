#!/usr/bin/env bash
set -euo pipefail

policy_ref='docs/CONSTITUTION.md §2'

while read -r local_ref local_sha remote_ref remote_sha; do
  [[ -z "${local_ref:-}" ]] && continue

  local_branch="${local_ref#refs/heads/}"
  remote_branch="${remote_ref#refs/heads/}"

  if [[ "$local_branch" == test-pre-merge-* ]]; then
    cat >&2 <<MSG
[HOOK] Push blocked: test pre-merge batch '$local_branch' is local-only.
Create the batch from current develop, use it for temporary verification, then delete it.
Do not publish test-pre-merge branches to remote.
Policy source: $policy_ref
MSG
    exit 1
  fi

  case "$local_branch" in
    main|develop)
      continue
      ;;
    feature/*|release/*|hotfix/*)
      if [[ "$remote_branch" == "$local_branch" ]]; then
        continue
      fi
      cat >&2 <<MSG
[HOOK] Push blocked: branch '$local_branch' can only push to the same branch on remote.
Attempted remote ref: ${remote_ref:-<none>}

Merge/promotion must happen from the target branch worktree, not by pushing across branch names.
Policy source: $policy_ref
MSG
      exit 1
      ;;
    *)
      cat >&2 <<MSG
[HOOK] Push blocked: unsupported branch type '$local_branch'.
Use feature/*, release/*, hotfix/* or protected integration branches.
Policy source: $policy_ref
MSG
      exit 1
      ;;
  esac
done

exit 0
