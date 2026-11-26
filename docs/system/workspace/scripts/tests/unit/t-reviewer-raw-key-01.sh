#!/usr/bin/env bash
# Function-level test for a2a_task._a2a_exit_update_fields (#4109).
# A needs-review state_update SSE event MUST carry raw_key, otherwise the
# watchdog reviewer route fails closed and phase reviews are bypassed.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="${UT_PROJECT_ROOT:-$(git rev-parse --show-toplevel)}"
A2A="$ROOT/docs/system/workspace/scripts/runtime/a2a_task.py"

assert_file "$A2A" "a2a_task.py exists"

probe() {
  python3 - "$A2A" "$1" 2>/dev/null <<'PY'
import importlib.util
import sys
from types import SimpleNamespace

path, case = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("a2a_unit_probe", path)
m = importlib.util.module_from_spec(spec)
sys.modules["a2a_unit_probe"] = m
spec.loader.exec_module(m)

class Stored:
    def get(self, task_id):
        return {"task_id": task_id, "raw_key": "raw-20260807T121205Z"}

class Empty:
    def get(self, task_id):
        return {}

args = SimpleNamespace(summary="s", next="", evidence="", raw_key="")
if case == "record":
    fields = m._a2a_exit_update_fields("input-required", "needs-review:b1", args, Stored(), "t")
    print("ok" if fields.get("raw_key") == "raw-20260807T121205Z" else "bad")
elif case == "explicit":
    args.raw_key = "raw-explicit"
    fields = m._a2a_exit_update_fields("input-required", "needs-review:b1", args, Stored(), "t")
    print("ok" if fields.get("raw_key") == "raw-explicit" else "bad")
elif case == "reject":
    try:
        m._a2a_exit_update_fields("input-required", "needs-review:b2", args, Empty(), "t")
        print("bad")
    except ValueError:
        print("ok")
elif case == "plain":
    fields = m._a2a_exit_update_fields("completed", "", args, Stored(), "t")
    print("ok" if "raw_key" not in fields else "bad")
PY
}

assert_eq "ok" "$(probe record)" "needs-review field carries raw_key from task record"
assert_eq "ok" "$(probe explicit)" "explicit --raw-key wins over task record"
assert_eq "ok" "$(probe reject)" "missing raw_key raises ValueError (fail-closed)"
assert_eq "ok" "$(probe plain)" "non-review transition unchanged"

ut_report
