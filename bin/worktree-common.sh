#!/usr/bin/env bash
set -euo pipefail

# Scripts live in the main repo (primary git worktree), not in worktrees.
# Use git worktree list to find the primary worktree path.
# Buffer git output into a variable to avoid SIGPIPE from awk exit
# closing the pipe while git is still writing (triggers set -o pipefail).
_wt_raw="$(git worktree list --porcelain 2>/dev/null || true)"
_primary="$(printf '%s\n' "$_wt_raw" | awk '
  $1=="worktree" { wt=$2 }
  $1=="HEAD" && $2 ~ /^[0-9a-f]{40}$/ { print wt; exit }
')"
if [[ -z "$_primary" ]]; then
  # Fallback: assume we're at the main repo
  _primary="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
fi
ROOT_DIR="$_primary"
# shellcheck disable=SC1091
source "$ROOT_DIR/docs/system/workspace/scripts/worktree/worktree-common.sh" "$@"
