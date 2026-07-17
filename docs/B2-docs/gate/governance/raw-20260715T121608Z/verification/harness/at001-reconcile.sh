#!/bin/bash
# AT-001: 证据包完整性 — A/B/C/D 四节齐备且逐项含证据锚
set -u
F="$(pwd)/docs/B2-docs/gate/governance/raw-20260715T121608Z/verification/reconcile-evidence-package.md"
FAIL=0
for sec in "## A." "## B." "## C." "## D."; do grep -q "$sec" "$F" || { echo "missing $sec"; FAIL=1; }; done
[ "$(grep -c '7e1057dc2\|b4e6d5d99\|4f5183b71' "$F")" -ge 3 ] || { echo "A 节 merge 实证不全"; FAIL=1; }
[ "$(grep -oE 'gh#[0-9]+|#5[0-9][0-9]|PR#2243|#2883|#231' "$F" | wc -l | tr -d ' ')" -ge 13 ] || { echo "B 节平台实证不足 13"; FAIL=1; }
[ "$(grep -oE 'I-20260[0-9TZ]+-[A-Z-]+' "$F"  || { echo "C 节留档不全"; FAIL=1; }
[ "$FAIL" -eq 0 ] && echo "AT-001 PASS: 证据包完整(A3+B13+C6+D1)" || echo "AT-001 FAIL"
