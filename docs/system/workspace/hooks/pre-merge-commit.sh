#!/usr/bin/env bash
set -euo pipefail

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
[[ "$branch" == "develop" ]] || exit 0
project_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd -P)"

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
Policy source: docs/LAWS.md §2C
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
MSG
  exit "$promotion_rc"
fi

[[ -n "$promotion_output" ]] && echo "$promotion_output"
exit 0
