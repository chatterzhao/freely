#!/usr/bin/env bash
set -euo pipefail

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
[[ "$branch" == "develop" ]] || exit 0
project_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd -P)"

break_glass_reason="${FREELY_BREAK_GLASS_REASON:-}"
break_glass_blocked_gate="${FREELY_BLOCKED_GATE:-}"
break_glass_follow_on_issue="${FREELY_FOLLOW_ON_ISSUE:-}"
break_glass_operation_scope="${FREELY_OPERATION_SCOPE:-}"
break_glass_evidence_refs="${FREELY_EVIDENCE_REFS:-}"

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
gate_output="$(./bin/governance-merge-gate --staged 2>&1)"
gate_rc=$?
set -e

if [[ "$gate_rc" -ne 0 ]]; then
  cat <<MSG
[HOOK] Merge blocked: develop-bound governance materialization gate failed.

$gate_output

Fix the candidate -> milestone -> IBM issue chain in the source feature worktree, then replay the merge.
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
