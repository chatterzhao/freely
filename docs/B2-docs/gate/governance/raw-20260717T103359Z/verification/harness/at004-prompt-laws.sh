#!/bin/bash
# AT-004: fallback prompt 铁律幂等 prepend
set -u
Q="$(pwd)"
F="$Q/docs/system/workspace/scripts/runtime/freely"
grep -q "_prepend_worktree_boundary_laws" "$F" || { echo "AT-004 FAIL: prepend 函数不存在"; exit 0; }
TMP=$(mktemp); echo "原始任务内容" > "$TMP"
{
  echo 'append_runtime_event() { :; }'
  awk '/^_prepend_worktree_boundary_laws\(\)/,/^}/' "$F"
} > /tmp/pl.sh
bash -c "source /tmp/pl.sh; _prepend_worktree_boundary_laws '$TMP' 'testkey'; _prepend_worktree_boundary_laws '$TMP' 'testkey'"
N=$(grep -c "worktree-boundary-laws v1" "$TMP")
HAS=$(grep -c "只允许写入" "$TMP" || true)
ORIG=$(grep -c "原始任务内容" "$TMP")
rm -f "$TMP" /tmp/pl.sh
echo "observed: marker_count=$N laws=$HAS original_kept=$ORIG"
if [ "$N" -eq 1 ] && [ "$HAS" -ge 1 ] && [ "$ORIG" -eq 1 ]; then echo "AT-004 PASS"; else echo "AT-004 FAIL"; fi
