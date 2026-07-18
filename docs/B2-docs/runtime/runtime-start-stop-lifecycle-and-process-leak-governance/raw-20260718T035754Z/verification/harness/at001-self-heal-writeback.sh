#!/usr/bin/env bash
# AT-001: bridge 启动后 config.toml FREELY_ACP_CLAUDE_BIN 从空变为正确路径
# usage: at001-self-heal-writeback.sh <runtime_script> <project_root>
set -uo pipefail
S="$1"; P="$2"
val=$(grep 'FREELY_ACP_CLAUDE_BIN' "$P/.freely/config.toml" | sed "s/.*= *\"//;s/\"//")
if [[ -z "$val" ]]; then echo "  config still empty"; echo "AT001_RESULT: FAIL"; exit 1; fi
if [[ "$val" == "/"* && -x "$val" ]]; then echo "  binary cached: $val"; echo "AT001_RESULT: PASS"; exit 0; fi
echo "  unexpected value: $val"; echo "AT001_RESULT: FAIL"; exit 1
