#!/bin/bash
# AT-001: 未完成 key 默认拦截;已合并 key 通过前置检查
set -u
Q="$(pwd)"
# 未完成假 key(无 merge 证据):期望被 guard 拦(输出含 ownership-guard 拒绝话术)
OUT1=$("$Q/bin/wt-close" --raw-key 20990101T000000Z 2>&1 | head -20)
G1=0; printf '%s' "$OUT1" | grep -q "ownership-guard" && G1=1
# 已合并 key(raw-20260717T004620Z 有 merge 记录):应通过 guard(后续因工位不存在等报错不属 guard)
OUT2=$("$Q/bin/wt-close" --raw-key 20260717T004620Z 2>&1 | head -20)
G2=0; printf '%s' "$OUT2" | grep -q "ownership-guard" && G2=1
echo "observed: unfinished_blocked=$G1 merged_blocked=$G2"
if [ "$G1" -eq 1 ] && [ "$G2" -eq 0 ]; then echo "AT-001 PASS"; else echo "AT-001 FAIL: g1=$G1 g2=$G2"; fi
