#!/bin/bash
# AT-001: 状态收敛断言 — (a) 3 个 merge 实证且无欠账的 I-* 为终态 (b) 13 个 legacy raw 有终态
set -u
ROOT="$(pwd)"; FAIL=0
for f in \
 "docs/B2-docs/a2a/handoff/raw-20260612T000223Z/issues/issues/I-20260612T000223Z-A.md" \
 "docs/B2-docs/ibm/_legacy/raw-MIGRATED-gate-scope-alignment/issues/I-20260616T030213Z-A.md" \
 "docs/B2-docs/a2a/handoff/raw-20260615T001626Z/issues/I-20260615T001626Z-A.md"; do
  st=$(grep -m1 -oE "^-? ?phase_state: [a-z_0-9]+" "$ROOT/$f" 2>/dev/null | awk '{print $NF}')
  case "$st" in completed|absorbed) ;; *) echo "I-drift: $(basename $f)=${st:-MISSING}"; FAIL=$((FAIL+1));; esac
done
for K in 20260506T100000Z 20260517T113021Z 20260517T113514Z 20260517T113807Z 20260517T114147Z 20260517T114702Z 20260517T115113Z 20260517T115824Z 20260517T120124Z 20260517T120752Z 20260517T121432Z 20260527T004453Z 20260617T035314Z; do
  st=$(grep -m1 "^phase_state:" "$ROOT/docs/B1-docs/raw-$K/issue.md" 2>/dev/null | awk '{print $2}')
  case "$st" in absorbed|dropped) ;; *) echo "raw-drift: $K=${st:-none}"; FAIL=$((FAIL+1));; esac
done
[ "$FAIL" -eq 0 ] && echo "AT-001 PASS: 16/16 状态已收敛" || echo "AT-001 FAIL: $FAIL 处未收敛"
