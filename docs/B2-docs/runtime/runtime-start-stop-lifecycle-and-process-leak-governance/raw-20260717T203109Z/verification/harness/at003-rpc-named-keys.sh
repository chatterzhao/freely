#!/usr/bin/env bash
# AT-003: agent_working.get / get_all RPC 返回命名键（worker_id 等），非数字键 '0'..'10'
# 临时 project 起独立 daemon（socket 按临时路径 hash，不碰主仓 daemon）
# usage: at003-rpc-named-keys.sh <runtime_scripts_dir>
set -uo pipefail
RT="$1"
T=$(mktemp -d); mkdir -p "$T/.freely"
cleanup() { python3 "$RT/freely_db_manager.py" stop --project "$T" >/dev/null 2>&1; rm -rf "$T"; }
trap cleanup EXIT
python3 "$RT/freely_db_manager.py" start --project "$T" >/dev/null 2>&1
SOCK=$(python3 -c "import hashlib,os;print('/tmp/freely-db-'+hashlib.sha256(os.path.abspath('$T').encode()).hexdigest()[:16]+'.sock')")
for i in $(seq 1 30); do [[ -S "$SOCK" ]] && break; sleep 0.2; done
[[ -S "$SOCK" ]] || { echo "  daemon socket never appeared"; echo "AT003_RESULT: FAIL"; exit 1; }
python3 - "$RT" "$T" <<'PY'
import sys
rt, proj = sys.argv[1], sys.argv[2]
sys.path.insert(0, rt)
from agent_working import agent_assign, agent_list_by_raw_key, _db_rpc
agent_assign(proj, "raw-at003", "worker", "w01", session_id="s1")
row = agent_list_by_raw_key(proj, "raw-at003")
print("  get keys:", sorted(row.keys()))
rows = _db_rpc(proj, "agent_working.get_all", {}).get("rows", [])
all_ok = rows and "worker_id" in rows[0]
ok = "worker_id" in row and str(row.get("worker_id", "")).startswith("w01") and all_ok
print("AT003_RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
PY
