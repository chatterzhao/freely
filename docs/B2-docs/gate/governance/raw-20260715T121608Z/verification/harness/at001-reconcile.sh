#!/bin/bash
# AT-001: 状态收敛断言 — 3 个 merge 实证且无欠账的 I-* 为终态
set -u
ROOT="$(pwd)"; FAIL=0
for f in \
 "docs/B2-docs/a2a/handoff/raw-20260612T000223Z/issues/issues/I-20260612T000223Z-A.md" \
 "docs/B2-docs/ibm/_legacy/raw-MIGRATED-gate-scope-alignment/issues/I-20260616T030213Z-A.md" \
 "docs/B2-docs/a2a/handoff/raw-20260615T001626Z/issues/I-20260615T001626Z-A.md"; do
  st=$(grep -m1 -oE "^-? ?phase_state: [a-z_0-9]+" "$ROOT/$f" 2>/dev/null | awk '{print $NF}')
  case "$st" in completed|absorbed) ;; *) echo "I-drift: $(basename $f)=${st:-MISSING}"; FAIL=$((FAIL+1));; esac
done
[ "$FAIL" -eq 0 ] && echo "AT-001 PASS: 3/3 状态已收敛" || echo "AT-001 FAIL: $FAIL 处未收敛"
