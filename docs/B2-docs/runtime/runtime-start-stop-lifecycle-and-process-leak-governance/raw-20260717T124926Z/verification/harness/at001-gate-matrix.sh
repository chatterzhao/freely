#!/bin/bash
# AT-001: gate 行为矩阵 — 自属未完成→拒+JSON reason / 他属已完成→允许 / 他属未完成→拒 / 所有既有 closeout 动作不变
set -u
Q="$(pwd)"
FAIL=0
# 1) 自属未完成假key(无merge证据+agent_working 无活跃) → 应拒且输出 actionable
OUT1=$(FREELY_AGENT_RAW_KEY=20990101T000000Z "$Q/bin/wt-close" --raw-key 20990101T000000Z 2>&1 | head -10)
if printf '%s' "$OUT1" | grep -qE "DENIED|BLOCKED|rejected" ; then
  echo "  gate1 自属未完成→拒 ✓"
else
  echo "  gate1 自属未完成→误放行 ✗"; FAIL=1
fi
# 2) 他属已完成key(有merge证据) → 应允许(过gate)
OUT2=$(FREELY_AGENT_RAW_KEY=20260717T999999Z "$Q/bin/wt-close" --raw-key 20260717T004620Z 2>&1 | head -10)
if printf '%s' "$OUT2" | grep -qE "DENIED|BLOCKED|rejected" ; then
  echo "  gate2 他属已完成→误拒 ✗"; FAIL=1
else
  echo "  gate2 他属已完成→通过 ✓"
fi
# 3) 他属未完成假key → 应拒
OUT3=$(FREELY_AGENT_RAW_KEY=20260717T999999Z "$Q/bin/wt-close" --raw-key 20990101T000000Z 2>&1 | head -10)
if printf '%s' "$OUT3" | grep -qE "DENIED|BLOCKED|rejected" ; then
  echo "  gate3 他属未完成→拒 ✓"
else
  echo "  gate3 他属未完成→误放行 ✗"; FAIL=1
fi
# 4) 既有 closeout 功能:--platform-only 不受 gate 影响
OUT4=$("$Q/bin/wt-close" --raw-key 20990101T000000Z --platform-only --reason "违规绕过门禁中，理由充分，是：测试自治 gate" 2>&1 | head -10)
if printf '%s' "$OUT4" | grep -qi "platform"; then
  echo "  gate4 platform-only 不受影响 ✓"
else
  echo "  gate4 platform-only 路径异常 ✗"; FAIL=1
fi
echo "AT-001 $( [ $FAIL -eq 0 ] && echo PASS || echo FAIL )"
