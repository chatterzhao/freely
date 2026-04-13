#!/usr/bin/env bash
set -euo pipefail

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
[[ "$branch" == "develop" ]] || exit 0
project_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd -P)"
guarded_state_path="$(git rev-parse --git-dir 2>/dev/null || true)"
if [[ -n "$guarded_state_path" ]]; then
  guarded_state_path="$guarded_state_path/freely-guarded-merge-state"
fi

break_glass_reason="${FREELY_BREAK_GLASS_REASON:-}"
break_glass_blocked_gate="${FREELY_BLOCKED_GATE:-}"
break_glass_follow_on_issue="${FREELY_FOLLOW_ON_ISSUE:-}"
break_glass_operation_scope="${FREELY_OPERATION_SCOPE:-}"
break_glass_evidence_refs="${FREELY_EVIDENCE_REFS:-}"

load_guarded_state() {
  [[ -n "$guarded_state_path" && -f "$guarded_state_path" ]] || return 1
  guarded_state_target=""
  guarded_state_source=""
  guarded_state_bypass=""
  while IFS='=' read -r key value; do
    case "$key" in
      target_branch) guarded_state_target="$value" ;;
      source_branch) guarded_state_source="$value" ;;
      bypass_mode) guarded_state_bypass="$value" ;;
    esac
  done <"$guarded_state_path"
  [[ -n "$guarded_state_target" && -n "$guarded_state_source" && -n "$guarded_state_bypass" ]] || return 1
}

require_valid_guarded_merge_state() {
  load_guarded_state || {
    cat <<MSG
[HOOK] Merge blocked: canonical guarded merge state is missing or malformed.
Raw develop merges are not an allowed entrypoint. Re-run the merge through ./bin/merge-guarded so hooks can verify the canonical handshake.
Policy source: docs/LAWS.md §2, §2D
MSG
    exit 1
  }

  if [[ "${FREELY_GUARDED_MERGE_COMPLETION:-0}" != "1" ]]; then
    cat <<MSG
[HOOK] Merge blocked: canonical guarded merge handshake marker is missing.
Raw develop merges are not an allowed entrypoint. Re-run the merge through ./bin/merge-guarded.
Policy source: docs/LAWS.md §2, §2D
MSG
    exit 1
  fi

  if ! git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1; then
    cat <<MSG
[HOOK] Merge blocked: guarded completion requires an active MERGE_HEAD.
Policy source: docs/LAWS.md §2D
MSG
    exit 1
  fi

  if [[ "$guarded_state_target" != "$branch" ]]; then
    cat <<MSG
[HOOK] Merge blocked: guarded merge completion target '$guarded_state_target' does not match current branch '$branch'.
Policy source: docs/LAWS.md §2D
MSG
    exit 1
  fi

  merge_head="$(git rev-parse -q --verify MERGE_HEAD 2>/dev/null || true)"
  source_sha="$(git rev-parse "$guarded_state_source" 2>/dev/null || true)"
  if [[ -z "$merge_head" || -z "$source_sha" || "$merge_head" != "$source_sha" ]]; then
    cat <<MSG
[HOOK] Merge blocked: guarded merge completion source '$guarded_state_source' does not match MERGE_HEAD.
Policy source: docs/LAWS.md §2D
MSG
    exit 1
  fi
}

require_valid_guarded_merge_state

if [[ -n "$break_glass_reason$break_glass_blocked_gate$break_glass_follow_on_issue$break_glass_operation_scope$break_glass_evidence_refs" ]]; then
  case "$break_glass_reason" in
    tooling_unavailable|verified_false_negative) ;;
    *)
      cat <<MSG
[HOOK] Merge blocked: unsupported break-glass reason '$break_glass_reason'.

Policy source: docs/LAWS.md §2D
MSG
      exit 1
      ;;
  esac

  case "$break_glass_blocked_gate" in
    pre-commit|pre-merge-commit|governance-merge-gate|governance-promotion-gate|pretests-gate|checkpoint-guard) ;;
    *)
      cat <<MSG
[HOOK] Merge blocked: unsupported break-glass blocked gate '$break_glass_blocked_gate'.

Policy source: docs/LAWS.md §2D
MSG
      exit 1
      ;;
  esac

  if [[ "$break_glass_operation_scope" != "merge_completion_only" ]]; then
    cat <<MSG
[HOOK] Merge blocked: break-glass scope must be 'merge_completion_only'.

Policy source: docs/LAWS.md §2D
MSG
    exit 1
  fi

  if [[ -z "$break_glass_follow_on_issue" || -z "$break_glass_evidence_refs" ]]; then
    cat <<MSG
[HOOK] Merge blocked: break-glass requires follow-on issue and at least one evidence reference.

Policy source: docs/LAWS.md §2D
MSG
    exit 1
  fi

  if [[ "$guarded_state_bypass" != "break_glass" ]]; then
    cat <<MSG
[HOOK] Merge blocked: guarded merge completion state does not authorize break-glass completion.
Policy source: docs/LAWS.md §2D
MSG
    exit 1
  fi

  cat <<MSG
[HOOK] Break-glass acknowledged for develop merge completion.

- reason: $break_glass_reason
- blocked_gate: $break_glass_blocked_gate
- operation_scope: $break_glass_operation_scope
- follow_on_issue: $break_glass_follow_on_issue
- evidence_refs: $break_glass_evidence_refs

Policy source: docs/LAWS.md §2D
MSG
  exit 0
fi

if git diff --cached --quiet --diff-filter=ACMR --; then
  exit 0
fi

if [[ ! -x "./bin/governance-merge-gate" ]]; then
  exit 0
fi

set +e
gate_output="$(./bin/governance-merge-gate --staged --target-branch "$branch" --source-branch "$guarded_state_source" 2>&1)"
gate_rc=$?
set -e

if [[ "$gate_rc" -ne 0 ]]; then
  cat <<MSG
[HOOK] Merge blocked: develop-bound governance materialization gate failed.

$gate_output

Fix the candidate -> milestone -> IBM issue chain in the source writable worktree, and make sure the owner pre-tests reflect real test work or lawful non-test waivers with traceable evidence before rerunning the guarded merge from the canonical lane. Do not clear this gate by only filling metadata.
Only use break-glass if this failure matches docs/LAWS.md §2D and the merge can stay within merge_completion_only scope.
Policy source: docs/LAWS.md §2C, §2D
MSG
  exit "$gate_rc"
fi

echo "$gate_output"

if [[ ! -x "./bin/governance-promotion-gate" ]]; then
  exit 0
fi

set +e
promotion_output="$(./bin/governance-promotion-gate --project "$project_root" --target-branch "$branch" 2>&1)"
promotion_rc=$?
set -e

if [[ "$promotion_rc" -ne 0 ]]; then
  cat <<MSG
[HOOK] Merge blocked: develop-bound promotion ownership gate failed.

$promotion_output

Let the current promotion owner finish or reclaim ownership through manager arbitration before merging to develop.
Only use break-glass if this failure matches docs/LAWS.md §2D and the merge can stay within merge_completion_only scope.
MSG
  exit "$promotion_rc"
fi

[[ -n "$promotion_output" ]] && echo "$promotion_output"
exit 0
