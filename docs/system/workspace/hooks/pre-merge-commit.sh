#!/usr/bin/env bash
set -euo pipefail

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
[[ "$branch" == "develop" ]] || exit 0

if ! git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1; then
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
exit 0
