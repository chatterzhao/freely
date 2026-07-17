#!/usr/bin/env bash
# AT-004: E2E 沙箱主仓 — 活跃 worker 行存在 → gate DENY（含 worker id）；释放后 → allow。
# 验证链：_main_root 解析 → 按主仓 hash 连 daemon → 命名键读 worker_id → 判定矩阵。
# usage: at004-active-worker-deny.sh <wtclose_script> <runtime_scripts_dir>
set -uo pipefail
WTC="$1"; RT="$2"
SB=$(mktemp -d)
SB=$(cd "$SB" && pwd -P)   # 物理路径：daemon socket 按 abspath hash，git 返回物理路径，两者必须同形态
cleanup() { python3 "$SB/docs/system/workspace/scripts/runtime/freely_db_manager.py" stop --project "$SB" >/dev/null 2>&1; rm -rf "$SB"; }
trap cleanup EXIT
git -C "$SB" init -q -b develop
mkdir -p "$SB/docs/system/workspace/scripts/runtime" "$SB/.freely"
cp "$RT/freely_db_manager.py" "$RT/agent_working.py" "$SB/docs/system/workspace/scripts/runtime/"
git -C "$SB" add -A
git -C "$SB" -c user.email=t@t -c user.name=t commit -qm init
python3 "$SB/docs/system/workspace/scripts/runtime/freely_db_manager.py" start --project "$SB" >/dev/null 2>&1
SOCK=$(python3 -c "import hashlib,os;print('/tmp/freely-db-'+hashlib.sha256(os.path.abspath('$SB').encode()).hexdigest()[:16]+'.sock')")
for i in $(seq 1 30); do [[ -S "$SOCK" ]] && break; sleep 0.2; done
[[ -S "$SOCK" ]] || { echo "  sandbox daemon never came up"; echo "AT004_RESULT: FAIL"; exit 1; }
K=20260717T888888Z
python3 - "$SB" "$K" <<'PY'
import sys
sb, k = sys.argv[1], sys.argv[2]
sys.path.insert(0, sb + "/docs/system/workspace/scripts/runtime")
from agent_working import agent_assign
agent_assign(sb, f"raw-{k}", "worker", "w07", session_id="s7")
PY
cd "$SB"
PROJECT_ROOT="$SB" FREELY_AGENT_RAW_KEY="$K" bash "$WTC" --raw-key "$K" --dry-run 2>"$SB/deny.log" >/dev/null
r1=1; grep -q "DENIED self-owned raw-$K" "$SB/deny.log" && grep -q "w=w07" "$SB/deny.log" && r1=0
echo "  deny phase: $(grep -m1 closeout-gate "$SB/deny.log" || echo '(empty)')"
python3 - "$SB" "$K" <<'PY'
import sys
sb, k = sys.argv[1], sys.argv[2]
sys.path.insert(0, sb + "/docs/system/workspace/scripts/runtime")
from agent_working import agent_release_all
agent_release_all(sb, f"raw-{k}")
PY
PROJECT_ROOT="$SB" FREELY_AGENT_RAW_KEY="$K" bash "$WTC" --raw-key "$K" --dry-run 2>"$SB/allow.log" >/dev/null
r2=1; grep -q "allowing close" "$SB/allow.log" && r2=0
echo "  allow phase: $(grep -m1 closeout-gate "$SB/allow.log" || echo '(empty)')"
if [[ $r1 -eq 0 && $r2 -eq 0 ]]; then echo "AT004_RESULT: PASS"; exit 0; else echo "AT004_RESULT: FAIL"; exit 1; fi
