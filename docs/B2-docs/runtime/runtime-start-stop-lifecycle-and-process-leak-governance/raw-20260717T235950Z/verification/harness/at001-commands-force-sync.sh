#!/usr/bin/env bash
# AT-001: commands.md --force 选项行含自治门禁语义，与 wt-close --help 判据一致
# usage: at001-commands-force-sync.sh <project_or_worktree_root>
set -uo pipefail
R="$1"
line=$(grep -E '^\| `--force` \| 永久丢弃' "$R/docs/system/workspace/commands.md" || true)
if [[ -z "$line" ]]; then echo "  --force row not found"; echo "AT001_RESULT: FAIL"; exit 1; fi
echo "  row: $line"
if echo "$line" | grep -q "自治门禁"; then echo "AT001_RESULT: PASS"; exit 0; fi
echo "  row lacks 自治门禁 wording"; echo "AT001_RESULT: FAIL"; exit 1
