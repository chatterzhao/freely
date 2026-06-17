#!/usr/bin/env bash
# post-rewrite.sh — Rebase integrity verification hook for Freely
#
# Triggered automatically after `git rebase` and `git commit --amend`.
# Saves a pre-rebase diff snapshot (via pre-rebase) and compares against
# post-rebase diff to detect silently dropped changes.
#
# Output marker: .freely/run/rebase-lost-files (one path per line)
# pr-merge-guarded reads this marker and blocks merge if present.
set -euo pipefail

HOOK_TYPE="${1:-}"

# Only handle rebase; amend is too noisy for this check.
[[ "$HOOK_TYPE" == "rebase" ]] || exit 0

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
SNAPSHOT_DIR="$ROOT_DIR/.freely/run/pre-rebase-diffs"
MARKER_FILE="$ROOT_DIR/.freely/run/rebase-lost-files"

# Find the most recent pre-rebase snapshot for this branch.
branch="$(git rev-parse --abbrev-ref HEAD)"
latest_snapshot="$(ls -t "$SNAPSHOT_DIR"/*-"${branch//\//-}".diff 2>/dev/null | head -1 || true)"

if [[ -z "$latest_snapshot" || ! -f "$latest_snapshot" ]]; then
  # No snapshot — nothing to compare. Clean up any stale marker.
  rm -f "$MARKER_FILE"
  exit 0
fi

# Generate post-rebase diff (file list only, for reliable comparison).
post_files="$(mktemp)"
trap 'rm -f "$post_files"' EXIT
git diff develop...HEAD --name-only 2>/dev/null | sort > "$post_files"

# Compare: files that were in the pre-rebase snapshot but are missing now.
lost_files="$(comm -23 <(sort "$latest_snapshot") "$post_files" || true)"

if [[ -n "$lost_files" ]]; then
  cat >&2 <<EOF
╔══════════════════════════════════════════════════════════╗
║  ⚠️  REBASE INTEGRITY CHECK FAILED                       ║
╠══════════════════════════════════════════════════════════╣
║  The following files were present before rebase          ║
║  but are MISSING from the post-rebase diff:              ║
╠══════════════════════════════════════════════════════════╣
EOF
  while IFS= read -r f; do
    echo "║  $f" >&2
  done <<< "$lost_files"
  cat >&2 <<EOF
╠══════════════════════════════════════════════════════════╣
║  Action: verify if these were intentionally dropped      ║
║  or accidentally lost during conflict resolution.        ║
║  pr-merge-guarded will BLOCK merge while this persists.  ║
║  Clear with: rm -f $MARKER_FILE                          ║
╚══════════════════════════════════════════════════════════╝
EOF
  # Write marker for pr-merge-guarded to read.
  mkdir -p "$(dirname "$MARKER_FILE")"
  echo "$lost_files" > "$MARKER_FILE"
  # Clean up snapshot (one-shot check per rebase).
  rm -f "$latest_snapshot"
  exit 1
fi

# Clean: no files lost.
rm -f "$MARKER_FILE"
rm -f "$latest_snapshot"
