#!/usr/bin/env bash
# AT-003: set -u 且 base_tool 未定义时，函数不因 unbound variable 失败
set -u
F="$(pwd)/docs/system/workspace/scripts/runtime/freely"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
{
  echo 'file_mtime_epoch() { echo 0; }'
  echo '_acp_bridge_has_fatal_error() { return 1; }'
  echo '_acp_bridge_socket() { echo "/tmp/nonexistent-$$.sock"; }'
  echo 'SELF_ROOT="/nonexistent"'
  echo 'AGENT_AI_TOOL="claude-apikey-test"'
  awk '/^_ai_shows_liveness_acp\(\)/,/^}/' "$F"
} > "$TMP/h.sh"
ERR=$(bash -c "set -u; source '$TMP/h.sh'; _ai_shows_liveness_acp '/tmp/fake-proj' '99999999' '$TMP/cycle.log' 90" 2>&1 >/dev/null | grep -c "unbound variable" || true)
if [ "$ERR" -eq 0 ]; then
  echo "AT-003 PASS: 无 unbound variable"
else
  echo "AT-003 FAIL: base_tool unbound variable ($ERR 处)"
fi
