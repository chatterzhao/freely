#!/bin/bash
# AT-002: pr-review-guarded 取值逻辑四格式兼容
# 方法: (a) 锚定断言——文件含三段式引号可选管道特征; (b) 行为——同款管道四格式矩阵
set -u
RV="$(pwd)/bin/pr-review-guarded"
FAIL=0
grep -q "s/^\[^:\]\*:\[\[:space:\]\]\*//" "$RV" || { echo "anchor FAIL: 去前缀段缺失"; FAIL=1; }
LINE=$(grep "_verification_dir=" "$RV" | head -1)
printf '%s' "$LINE" | grep -q "sed -e" || { echo "anchor FAIL: 非多段 sed"; FAIL=1; }
printf '%s' "$LINE" | grep -Fq "s/.*: *'" && { echo "anchor FAIL: 仍是旧单引号强制 sed"; FAIL=1; }
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
path='docs/B2-docs/gate/x/raw-20260717T000000Z/code-reviews'
printf -- "- verification_artifact_dir: %s\n" "$path" > $TMP/a
printf -- "- verification_artifact_dir: '%s'\n" "$path" > $TMP/b
printf -- '- verification_artifact_dir: "%s"\n' "$path" > $TMP/c
printf -- '- verification_artifact_dir: `%s`\n' "$path" > $TMP/d
ok=0
for f in a b c d; do
  got=$(grep "verification_artifact_dir:" "$TMP/$f" | head -1 | sed -e 's/^[^:]*:[[:space:]]*//' -e $'s/^[\'"`]//' -e $'s/[\'"`][[:space:]]*$//')
  [ "$got" = "$path" ] && ok=$((ok+1)) || echo "$f fail: $got"
done
if [ "$FAIL" -eq 0 ] && [ "$ok" -eq 4 ]; then echo "AT-002 PASS: 4/4 格式解析通过"; else echo "AT-002 FAIL ($ok/4, anchor_fail=$FAIL)"; fi
