#!/usr/bin/env bash
# AT-001: runtime 实际打出的 auto-loop checkpoint 必须全部在 trace-contract 注册
set -u
F="$(pwd)/docs/system/workspace/scripts/runtime/freely"
DOC="$(pwd)/docs/system/workspace/three-loop-trace-contract.md"
EMITTED=$(grep -oE 'append_lifecycle_trace [^ ]+ "L[0-9]+"' "$F" | grep -oE '"L[0-9]+"' | tr -d '"' | sort -un -k1.2 | uniq)
MISSING=""
for cp in $EMITTED; do
  grep -q "A-$cp\b\|\`$cp\`\|| \`A-$cp\`" "$DOC" || MISSING="$MISSING $cp"
done
if [ -z "$MISSING" ]; then
  echo "AT-001 PASS: 全部 $(echo "$EMITTED" | wc -w | tr -d ' ') 个 checkpoint 已注册"
else
  echo "AT-001 FAIL: 未注册 checkpoint:$MISSING"
fi
