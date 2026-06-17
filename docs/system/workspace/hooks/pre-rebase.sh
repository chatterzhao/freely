#!/usr/bin/env bash
# pre-rebase.sh — Save diff snapshot before rebase for post-rewrite integrity check.
#
# Triggered automatically before `git rebase`.
# Saves: .freely/run/pre-rebase-diffs/<timestamp>-<branch>.diff
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
SNAPSHOT_DIR="$ROOT_DIR/.freely/run/pre-rebase-diffs"

branch="$(git rev-parse --abbrev-ref HEAD)"
# Skip on protected branches (we never rebase develop/main directly).
case "$branch" in
  develop|main|master) exit 0 ;;
esac

mkdir -p "$SNAPSHOT_DIR"
ts="$(date -u +%Y%m%dT%H%M%SZ)"
snapshot_file="$SNAPSHOT_DIR/${ts}-${branch//\//-}.diff"

# Save the file list for this branch's unique changes vs develop.
git diff develop...HEAD --name-only 2>/dev/null | sort > "$snapshot_file"

# Clean up snapshots older than 7 days.
find "$SNAPSHOT_DIR" -name '*.diff' -mtime +7 -delete 2>/dev/null || true
