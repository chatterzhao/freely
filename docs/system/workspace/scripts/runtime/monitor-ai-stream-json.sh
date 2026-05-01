#!/usr/bin/env bash
# monitor-ai-stream-json.sh: AI lifecycle monitor for stream-json adapter.
# STATUS: PROTOTYPE — see stream-json-bridge.py for details.
# ON HOLD: 2026-05-01. Reason: no cross-process cache hits.
#
# Simpler than monitor-ai-acp.sh: no persistent bridge needed.
# Each cycle spawns claude directly via stream-json-bridge.py.
# Session persistence via session-store.py.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

main() {
  local project="" tool="" prompt_file=""
  local session_id="" launch_kind="fresh" mode="auto" model=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --project) project="$2"; shift 2 ;;
      --tool) tool="$2"; shift 2 ;;
      --prompt-file) prompt_file="$2"; shift 2 ;;
      --session-id|--claude-session-id) session_id="$2"; shift 2 ;;
      --launch-kind) launch_kind="$2"; shift 2 ;;
      --mode) mode="$2"; shift 2 ;;
      --model) model="$2"; shift 2 ;;
      --pid-file) shift 2 ;;  # accept but ignore (no persistent process)
      --log-file) shift 2 ;;  # accept but ignore
      --debug-log-file) shift 2 ;;
      --tool-adapter) shift 2 ;;
      --reasoning-effort) shift 2 ;;
      --tool-capabilities) shift 2 ;;
      --tool-policy) shift 2 ;;
      --codex-capability-*) shift 2 ;;
      --network-failure-marker-file) shift 2 ;;
      --failure-marker-file) shift 2 ;;
      --bridge-lost-marker-file) shift 2 ;;
      --tool-resume-target) shift 2 ;;
      *) echo "[WARN] unknown arg: $1" >&2; shift ;;
    esac
  done

  [[ -n "$project" && -n "$tool" && -n "$prompt_file" ]] || {
    echo "[ERROR] missing required args" >&2; exit 1
  }

  local bridge_py="$SCRIPT_DIR/stream-json-bridge.py"
  [[ -f "$bridge_py" ]] || {
    echo "[ERROR] stream-json-bridge.py not found: $bridge_py" >&2; exit 1
  }

  # Write own PID as ai.pid
  echo "$$" > "$project/.freely/run/ai.pid" 2>/dev/null || true

  # Run the stream-json bridge (blocks until turn completes)
  python3 "$bridge_py" run \
    --project "$project" \
    --prompt-file "$prompt_file" \
    --session-id "${session_id:-}" \
    --launch-kind "$launch_kind" \
    --mode "$mode" \
    --model "${model:-}" \
    --tool "$tool"

  local rc=$?
  if [[ $rc -eq 0 ]]; then
    echo "[STREAM-JSON] cycle complete" >&2
  else
    echo "[WARN] stream-json cycle finished with rc=$rc" >&2
  fi
  exit $rc
}

main "$@"
