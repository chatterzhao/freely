#!/usr/bin/env bash
# Coordination contract: the reason enum must be importable as a package,
# agree with the machine-readable contract, and never need an agents/ sys.path hack.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
RUNTIME="$ROOT/docs/system/workspace/scripts/runtime"
CONTRACT="$ROOT/contracts/coordination/contract.yaml"

[[ -f "$CONTRACT" ]] && ut_ok "coordination contract file exists" || ut_bad "coordination contract missing"
python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$CONTRACT" >/dev/null 2>&1 \
  && ut_ok "contract is stdlib-parseable" || ut_bad "contract is not stdlib-parseable"

count="$(PYTHONPATH="$RUNTIME" python3 -c 'from coordination.input_required_reason import InputRequiredReason as R; print(len(list(R)))' 2>/dev/null)"
assert_eq "12" "$count" "InputRequiredReason exposes 12 values after the move"

parity="$(PYTHONPATH="$RUNTIME" python3 -c '
import json, sys
from coordination.input_required_reason import InputRequiredReason as R
m = json.load(open(sys.argv[1]))
print("ok" if set(m["input_required_reasons"]) == {r.value for r in R} else "drift")
' "$CONTRACT" 2>/dev/null)"
assert_eq "ok" "$parity" "contract reasons match the runtime enum"

grep -q 'sys.path.insert.*agents' "$RUNTIME/watchdog_sse.py" \
  && ut_bad "watchdog still injects agents/ into sys.path" \
  || ut_ok "watchdog has no agents/ sys.path hack"

python3 "$ROOT/bin/check-coordination-contract" --root "$ROOT" >/dev/null 2>&1 \
  && ut_ok "coordination lint passes on the real corpus" \
  || ut_bad "coordination lint refuses the real corpus"

ut_report
