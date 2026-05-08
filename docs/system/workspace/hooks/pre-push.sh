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
      if [[ "$local_branch" == "develop" && -x "./bin/governance-merge-gate" ]]; then
        if [[ -n "${remote_sha:-}" && "$remote_sha" != "0000000000000000000000000000000000000000" ]]; then
          set +e
          gate_output="$(./bin/governance-merge-gate --range "${remote_sha}..${local_sha}" 2>&1)"
          gate_rc=$?
          set -e
          if [[ "$gate_rc" -ne 0 ]]; then
            cat >&2 <<MSG
[HOOK] Push blocked: develop-bound governance materialization gate failed.

$gate_output

Fix the candidate -> milestone -> IBM issue chain before pushing develop.
Policy source: docs/LAWS.md §2C
MSG
            exit "$gate_rc"
          fi
        fi
      fi
      continue
      ;;
    feature/*|hotfix/*)
      # Validate naming convention: must contain raw-xxx or I-xxx key
      if ! echo "$local_branch" | grep -qoE 'raw-[0-9]{8}[-T][0-9]{4,6}Z?' && \
         ! echo "$local_branch" | grep -qoE 'I-[0-9]{8}[-T][0-9]{4,6}Z?(-[A-Z0-9]+)?'; then
        cat >&2 <<MSG
[HOOK] Push blocked: branch '$local_branch' must contain an issue key.
Format: feature/raw-{YYYYMMDD}-{HHMM}-{slug} or feature/raw-{YYYYMMDDTHHMMZ}-{slug}
Each worktree/branch must correspond to an issue (docs/LAWS.md §2).
Use 'git branch -m' to rename.
MSG
        exit 1
      fi
      if [[ "$remote_branch" == "$local_branch" ]]; then
        continue
      fi
      cat >&2 <<MSG
[HOOK] Push blocked: branch '$local_branch' can only push to the same branch on remote.
Attempted remote ref: ${remote_ref:-<none>}
Policy source: $policy_ref
MSG
      exit 1
      ;;
    release/*)
      if [[ "$remote_branch" == "$local_branch" ]]; then
        continue
      fi
      cat >&2 <<MSG
[HOOK] Push blocked: branch '$local_branch' can only push to the same branch on remote.
Attempted remote ref: ${remote_ref:-<none>}
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
