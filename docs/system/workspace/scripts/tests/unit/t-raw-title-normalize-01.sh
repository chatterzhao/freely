#!/usr/bin/env bash
# Function-level unit test: title normalisation identity rules.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
MOD="$ROOT/docs/system/workspace/scripts/runtime/raw_title_normalize.py"

python3 - "$MOD" <<'PY' && ut_ok "raw key is derived from title+body, never created_at" \
  || ut_bad "raw key derivation wrong"
import importlib.util, sys
spec = importlib.util.spec_from_file_location("rtn", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
assert m.extract_raw_key("fix: bad title\nlocal_id: raw-20260101T000000Z") == "20260101T000000Z"
assert m.extract_raw_key("no identity here") == ""
PY

python3 - "$MOD" <<'PY' && ut_ok "linked I-* issue is not a raw identity candidate" \
  || ut_bad "linked issue was accepted as a raw"
import importlib.util, sys
spec = importlib.util.spec_from_file_location("rtn", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
key = "20260101T000000Z"
linked = "---\nissue_id: I-20260101T000000Z-C\nkind: linked\npromoted_from: raw-20260101T000000Z\n---\n"
assert m._is_raw_identity("[I-20260101T000000Z-C] 讨论入口", linked, key) is False
raw_body = "| local_id | `raw-20260101T000000Z` |\n| kind | `raw` |\n"
assert m._is_raw_identity("fix: 缺前缀", raw_body, key) is True
assert m._is_raw_identity("[RAW-20260101T000000Z] fix: ok", "", key) is True
PY

python3 - "$MOD" <<'PY' && ut_ok "expected title comes from the single title contract" \
  || ut_bad "expected title diverged from raw_title_contract"
import importlib.util, sys
spec = importlib.util.spec_from_file_location("rtn", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
assert m._expected_title("20260101T000000Z", "fix: bad") == "[RAW-20260101T000000Z] fix: bad"
assert m._expected_title("20260101T000000Z", "[RAW-99999999T000000Z] fix: stale") == "[RAW-20260101T000000Z] fix: stale"
PY

ut_report
