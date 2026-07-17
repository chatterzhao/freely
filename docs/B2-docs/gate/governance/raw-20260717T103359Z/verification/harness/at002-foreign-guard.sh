#!/bin/bash
# AT-002: FREELY_AGENT_RAW_KEY 异主拦截;同主/未设不受该项影响
set -u
Q="$(pwd)"
OUT1=$(FREELY_AGENT_RAW_KEY=20260717T999999Z "$Q/bin/wt-close" --raw-key 20260717T004620Z 2>&1 | head -20)
F1=0; printf '%s' "$OUT1" | grep -q "ownership-guard.*异主\|foreign" && F1=1
OUT2=$(FREELY_AGENT_RAW_KEY=20260717T004620Z "$Q/bin/wt-close" --raw-key 20260717T004620Z 2>&1 | head -20)
F2=0; printf '%s' "$OUT2" | grep -q "ownership-guard.*异主\|foreign" && F2=1
echo "observed: foreign_blocked=$F1 self_blocked=$F2"
if [ "$F1" -eq 1 ] && [ "$F2" -eq 0 ]; then echo "AT-002 PASS"; else echo "AT-002 FAIL: f=$F1 s=$F2"; fi
