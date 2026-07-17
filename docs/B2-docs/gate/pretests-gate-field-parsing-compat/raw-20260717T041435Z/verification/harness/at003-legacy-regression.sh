#!/bin/bash
# AT-003: develop 已合并的引号版与双行版 I-* 经两解析器均得合法路径
set -u
ROOT="$(pwd)"
GATE="$ROOT/docs/system/workspace/scripts/quality/pretests-gate"
F_QUOTED="$ROOT/docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/issues/I-20260717T004620Z-A.md"
F_DUAL="$ROOT/docs/B2-docs/runtime/sse-watchdog/raw-20260717T004721Z/issues/I-20260717T004721Z-A.md"
VRE='^docs/B2-docs/.+/raw-[^/]+/code-reviews$'
FAIL=0
for f in "$F_QUOTED" "$F_DUAL"; do
  [ -f "$f" ] || { echo "missing $f"; FAIL=1; continue; }
  G=$(python3 - "$GATE" "$f" <<'PY'
import re,sys
src=open(sys.argv[1]).read(); text=open(sys.argv[2]).read()
rm=re.search(r're\.search\(rf"(.+?)", text',src)
pat=rm.group(1).replace('{re.escape(field)}','verification_artifact_dir')
m=re.search(pat,text,re.MULTILINE)
print(m.group(1).strip() if m else '')
PY
)
  printf '%s' "$G" | grep -qE "$VRE" || { echo "gate 解析失配: $(basename $f) got=$G"; FAIL=1; }
  R=$(grep "verification_artifact_dir:" "$f" | head -1 | sed -e 's/^[^:]*:[[:space:]]*//' -e $'s/^[\'"`]//' -e $'s/[\'"`][[:space:]]*$//')
  printf '%s' "$R" | grep -qE "$VRE" || { echo "review 解析失配: $(basename $f) got=$R"; FAIL=1; }
done
[ "$FAIL" -eq 0 ] && echo "AT-003 PASS: 存量双格式全通过" || echo "AT-003 FAIL"
