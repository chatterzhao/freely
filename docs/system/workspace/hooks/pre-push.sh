#!/usr/bin/env bash
set -euo pipefail

policy_ref='docs/CONSTITUTION.md §2'

while read -r local_ref local_sha remote_ref remote_sha; do
  [[ -z "${local_ref:-}" ]] && continue

  # Allow remote branch deletion (git push --delete). git sends
  # all-zero local_sha for delete operations; local_ref may be "(delete)".
  if [[ "$local_sha" == "0000000000000000000000000000000000000000" ]]; then
    continue
  fi

  # Allow tag pushes (git push <remote> <tagname>)
  if [[ "$local_ref" == refs/tags/* ]]; then
    continue
  fi

  local_branch="${local_ref#refs/heads/}"
  remote_branch="${remote_ref#refs/heads/}"

  # Audit log for FREELY_SKIP usage
  if [[ -n "${FREELY_SKIP_CREATE_GATE:-}" || -n "${FREELY_SKIP_IBM_GATE:-}" ]]; then
    mkdir -p .freely/logs
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) SKIP_GATE branch=$local_branch reason=${FREELY_SKIP_CREATE_GATE:-IBM_GATE}" >> .freely/logs/skip-gate.log
  fi

  if [[ "$local_branch" == test-pre-merge-* ]]; then
    cat >&2 <<MSG
[HOOK] Push blocked: test pre-merge batch '$local_branch' is local-only.
Create the batch from current develop, use it for temporary verification, then delete it.
Do not publish test-pre-merge branches to remote.
MSG
    exit 1
  fi

  case "$local_branch" in
    main|develop)
      if [[ "$local_branch" == "develop" && -x "./bin/governance-merge-gate" ]]; then
        if [[ "${FREELY_SKIP_IBM_GATE:-0}" == "1" ]]; then
          echo "[HOOK] FREELY_SKIP_IBM_GATE=1 — validating governance-only paths via governance-merge-gate --skip-ibm-gate"
          set +e
          gate_output="$(./bin/governance-merge-gate --range "develop..HEAD" --skip-ibm-gate 2>&1)"
          gate_rc=$?
          set -e
          if [[ "$gate_rc" -ne 0 ]]; then
            cat >&2 <<MSG
[HOOK] Push blocked: FREELY_SKIP_IBM_GATE=1 but governance-merge-gate detected implementation changes.

$gate_output

FREELY_SKIP_IBM_GATE=1 is only allowed for governance-only changes.
MSG
            exit "$gate_rc"
          fi
          echo "$gate_output"
        elif [[ -n "${remote_sha:-}" && "$remote_sha" != "0000000000000000000000000000000000000000" ]]; then
          set +e
          gate_output="$(./bin/governance-merge-gate --range "${remote_sha}..${local_sha}" 2>&1)"
          gate_rc=$?
          set -e
          if [[ "$gate_rc" -ne 0 ]]; then
            cat >&2 <<MSG
[HOOK] Push blocked: develop-bound governance materialization gate failed.

$gate_output

Fix the candidate -> milestone -> IBM issue chain before pushing develop.
MSG
            exit "$gate_rc"
          fi
        fi
      fi
      continue
      ;;
    feature/*|hotfix/*|fix/*)
      # Validate naming convention: must contain raw-xxx or I-xxx key
      if ! echo "$local_branch" | grep -qoE 'raw-[0-9]{8}[-T][0-9]{4,6}Z?' && \
         ! echo "$local_branch" | grep -qoE 'I-[0-9]{8}[-T][0-9]{4,6}Z?(-[A-Z0-9]+)?'; then
        cat >&2 <<MSG
[HOOK] Push blocked: branch '$local_branch' must contain an issue key.
Format: feature/raw-{YYYYMMDD}-{HHMM[SS]}-{slug} or feature/raw-{YYYYMMDDTHHMM[SS]Z}-{slug}
Each worktree/branch must correspond to an issue (docs/LAWS.md §2).
Use 'git branch -m' to rename.
MSG
        exit 1
      fi
      # Check if pr-create-gate has passed on this branch
      if [[ -z "${FREELY_SKIP_CREATE_GATE:-}" ]]; then
        if [[ ! -f ".freely/run/pr-create-gate-passed" ]]; then
          cat >&2 <<MSG
[HOOK] Push blocked: pr-create-gate has not been run on branch '$local_branch'.

  All fix/feature/hotfix branches must pass pr-create-guarded before pushing.
  Run pr-create-guarded in your worktree:
    ./bin/pr-create-guarded

  The ONLY valid way to push is:
    ./bin/pr-create-guarded
MSG
          exit 1
        fi
      else
        # FREELY_SKIP_CREATE_GATE=1: only allowed for docs-only changes.
        # Code files MUST go through pr-create-guarded.
        local _base; _base="$(git merge-base origin/develop HEAD 2>/dev/null || echo "origin/develop")"
        if git diff --name-only "$_base..HEAD" 2>/dev/null | grep -qE '\.(sh|py|rs|ts|js|tsx|jsx|go|java|c|cpp|h|toml)$'; then
          cat >&2 <<MSG
[HOOK] FREELY_SKIP_CREATE_GATE=1 rejected: code files must use pr-create-guarded.
  Run: ./bin/pr-create-guarded
MSG
          exit 1
        fi
      fi
      if [[ "$remote_branch" == "$local_branch" ]]; then
        continue
      fi
      cat >&2 <<MSG
[HOOK] Push blocked: branch '$local_branch' can only push to the same branch on remote.
Attempted remote ref: ${remote_ref:-<none>}
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
MSG
      exit 1
      ;;
    *)
      cat >&2 <<MSG
[HOOK] Push blocked: unsupported branch type '$local_branch'.
Use feature/*, release/*, hotfix/* or protected integration branches.
MSG
      exit 1
      ;;
  esac
done

exit 0
