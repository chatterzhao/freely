#!/bin/bash
set -u
Q="$(pwd)"
WTC="$Q/bin/wt-close"
FAIL=0
_chk() { local label="$1" out; out="$2"; if printf '%s' "$out" | grep -q "$3"; then echo "  $label ✓"; else echo "  $label ✗"; FAIL=1; fi; }
echo "═══ Gate Matrix ═══"
O1=$(FREELY_AGENT_RAW_KEY=20990101T000000Z "$WTC" --raw-key 20990101T000000Z 2>&1 | head -10)
_chk "self-unfinished → allow(no activity)" "$O1" "allowing close"
O2=$(FREELY_AGENT_RAW_KEY=20260717T999999Z "$WTC" --raw-key 20260717T004620Z 2>&1 | head -10)
_chk "foreign-finished → allow(sweep)" "$O2" "allowing sweep"
O3=$(FREELY_AGENT_RAW_KEY=20260717T999999Z "$WTC" --raw-key 20990101T000000Z 2>&1 | head -10)
_chk "foreign-unfinished → DENY" "$O3" "DENIED"
O4=$("$WTC" --raw-key 20990101T000000Z --platform-only --reason "违规绕过门禁中，理由充分，是：自治 gate 测试" 2>&1 | head -10)
_chk "platform-only 不受 gate 影响" "$O4" "raw key"
echo "AT-001 $( [ $FAIL -eq 0 ] && echo PASS || echo FAIL )"
