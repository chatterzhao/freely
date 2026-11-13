#!/usr/bin/env bash
# Function-level unit test (Step 2.5): the standalone-tool classification must
# not weaken the three original bin-projection gate rules.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
REG="$ROOT/docs/system/workspace/scripts/bin-projections.yaml"
LINT="$ROOT/bin/check-bin-projection"

python3 - "$REG" <<'PY' && ut_ok "22 standalone / 13 to-migrate classification" || ut_bad "classification counts wrong"
import json, sys
d = json.load(open(sys.argv[1]))
e = [x for x in d["entries"] if x["class"] != "dispatcher"]
assert "standalone-tool" in d["classes"]
assert sum(1 for x in e if x["class"] == "standalone-tool") == 22
assert sum(1 for x in e if x["class"] == "implementation-in-bin") == 13
assert all("case by case" not in str(x["reason"]).lower() for x in e)
PY

grep -qF 'not registered in' "$LINT" && ut_ok "coverage rule present" || ut_bad "coverage rule missing"
grep -qF 'stale entry' "$LINT" && ut_ok "staleness rule present" || ut_bad "staleness rule missing"
grep -qF 'delete its registry entry' "$LINT" && ut_ok "shrink rule present" || ut_bad "shrink rule missing"
grep -qF 'not declared in registry classes' "$LINT" \
  && ut_ok "class whitelist check present" \
  || ut_bad "class whitelist check missing"
grep -qF 'concrete classification decision' "$LINT" \
  && ut_ok "placeholder-reason rejection present" \
  || ut_bad "placeholder-reason rejection missing"

out="$(python3 "$LINT" --project "$ROOT" --json 2>/dev/null)"
python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["ok"] and not d["errors"]' <<<"$out" \
  && ut_ok "lint passes on the real repository" \
  || ut_bad "lint failed on the real repository: $out"

ut_report
