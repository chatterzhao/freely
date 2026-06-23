#!/usr/bin/env bash
# sse-watchdog.sh — SSE Watchdog: persistent Worker SSE connections
#
# Launched by freely daemon alongside manager_watchdog and interruption_dispatcher.
# Maintains SSE connections to active workers. On state_update events:
#   1. Writes to JSONL queue (.freely/run/sse-events.jsonl)
#   2. Injects into Manager session via ACP session/prompt
#
# Usage:
#   sse-watchdog.sh --project <abs_path> [--watch] [--interval <seconds>]
set -euo pipefail

SELF_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd -P)"
source "$SELF_ROOT/docs/system/workspace/scripts/runtime/freely"

PROJECT=""
WATCH_MODE="0"
INTERVAL="${SSE_WATCHDOG_INTERVAL:-10}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --watch) WATCH_MODE="1"; shift ;;
    --interval) INTERVAL="${2:-10}"; shift 2 ;;
    *) shift ;;
  esac
done

[[ -n "$PROJECT" ]] || { echo "Usage: sse-watchdog.sh --project <path> [--watch]" >&2; exit 1; }

load_config "$PROJECT"

A2A_TASK_PY="$SELF_ROOT/docs/system/workspace/scripts/runtime/a2a_task.py"
QUEUE_FILE="$(run_dir_for_project "$PROJECT")/sse-events.jsonl"
PID_FILE="$(run_dir_for_project "$PROJECT")/sse-watchdog.pid"
ACP_BRIDGE_SOCK="$(_acp_bridge_socket "$PROJECT")"
MANAGER_SESSION_FILE="$(run_dir_for_project "$PROJECT")/manager-session-id"

mkdir -p "$(run_dir_for_project "$PROJECT")"
echo $$ > "$PID_FILE"

# ── ACP session/prompt injection ────────────────────────────────────────

_sse_inject_to_manager() {
  local task_id="$1" state="$2" summary="${3:-}"
  local session_id
  if [[ ! -f "$MANAGER_SESSION_FILE" ]]; then
    return 0  # Manager not yet started, skip injection
  fi
  session_id="$(head -1 "$MANAGER_SESSION_FILE" 2>/dev/null || true)"
  [[ -n "$session_id" ]] || return 0

  local msg="[SSE Watchdog] Worker ${task_id} state=${state}"
  [[ -n "$summary" ]] && msg="${msg} — ${summary}"

  # Inject via ACP bridge session/prompt
  python3 -c "
import json, socket, sys, os
sock_path = '$ACP_BRIDGE_SOCK'
if not os.path.exists(sock_path):
    sys.exit(0)
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.settimeout(5)
try:
    sock.connect(sock_path)
    req = json.dumps({
        'jsonrpc': '2.0', 'id': 1, 'method': 'session/prompt',
        'params': {
            'sessionId': '$session_id',
            'prompt': [{'type': 'text', 'text': '$msg'}]
        }
    }, default=str) + '\n'
    sock.sendall(req.encode())
    sock.shutdown(socket.SHUT_WR)
except Exception:
    pass
finally:
    sock.close()
" 2>/dev/null || true
}

# ── Main SSE watch loop ────────────────────────────────────────────────

_sse_watchdog_cycle() {
  local project="$1"
  # Only run if Manager role and A2A server is up
  [[ "$(effective_runtime_role_for_project "$project")" == "manager" ]] || return 0

  # Get active worker tasks
  local workers
  workers=$(python3 "$A2A_TASK_PY" list --role worker --status working 2>/dev/null | \
    python3 -c "import json,sys; data=json.load(sys.stdin); rows=data.get('rows',[]); [print(r.get('task_id','')) for r in rows[:10]]" 2>/dev/null || true)
  [[ -n "$workers" ]] || return 0

  for task_id in $workers; do
    [[ -n "$task_id" ]] || continue

    # Quick SSE poll: read buffered events with short timeout
    local events
    events=$(python3 -c "
import subprocess, sys, json
result = subprocess.run(
    [sys.executable, '$A2A_TASK_PY', 'stream', '--task-id', '$task_id',
     '--timeout', '3', '--no-print'],
    capture_output=True, text=True, timeout=8)
if result and result.returncode == 0:
    try:
        data = json.loads(result.stdout)
        events = data if isinstance(data, list) else data.get('events', [])
        for ev in events:
            state = ev.get('state', '')
            ts = ev.get('timestamp', '')
            summary = ev.get('completion_summary', '') or ev.get('summary', '')
            print(f'{state}|{ts}|{summary}')
    except:
        pass
" 2>/dev/null || true)

    if [[ -n "$events" ]]; then
      while IFS='|' read -r state ts summary; do
        [[ -n "$state" ]] || continue
        # Enrich with worker context from A2A task record
        local session_id raw_key worktree
        session_id=$(python3 -c "
import subprocess, sys, json
r = subprocess.run([sys.executable, '$A2A_TASK_PY', 'get', '--task-id', '$task_id'],
                   capture_output=True, text=True, timeout=3)
if r.returncode == 0:
    try: d = json.loads(r.stdout); print(d.get('session_id',''))
    except: pass
" 2>/dev/null || true)
        raw_key=$(python3 -c "
import subprocess, sys, json
r = subprocess.run([sys.executable, '$A2A_TASK_PY', 'get', '--task-id', '$task_id'],
                   capture_output=True, text=True, timeout=3)
if r.returncode == 0:
    try: d = json.loads(r.stdout); print(d.get('raw_key',''))
    except: pass
" 2>/dev/null || true)
        worktree=$(python3 -c "
import subprocess, sys, json
r = subprocess.run([sys.executable, '$A2A_TASK_PY', 'get', '--task-id', '$task_id'],
                   capture_output=True, text=True, timeout=3)
if r.returncode == 0:
    try: d = json.loads(r.stdout); print(d.get('worktree',''))
    except: pass
" 2>/dev/null || true)

        # Write enriched event to JSONL queue
        python3 -c "
import json
ev = {
    'task_id': '$task_id',
    'state': '$state',
    'timestamp': '$ts',
    'session_id': '${session_id:-}',
    'raw_key': '${raw_key:-}',
    'worktree': '${worktree:-}',
    'event_type': 'state_update',
    'consumed': False
}
with open('$QUEUE_FILE', 'a') as f:
    f.write(json.dumps(ev, ensure_ascii=False) + '\n')
" 2>/dev/null || true

        # Inject to Manager via ACP with context
        _sse_inject_to_manager "$task_id" "$state" "$summary"
        append_runtime_event "$project" "sse_watchdog_event" \
          "task_id=$task_id" \
          "state=$state" \
          "session_id=${session_id:-}" \
          "raw_key=${raw_key:-}" \
          "worktree=${worktree:-}"
      done <<< "$events"
    fi
  done
}

# ── Main ────────────────────────────────────────────────────────────────

if [[ "$WATCH_MODE" == "1" ]]; then
  while true; do
    _sse_watchdog_cycle "$PROJECT" || true
    sleep "$INTERVAL"
  done
else
  _sse_watchdog_cycle "$PROJECT"
fi
