#!/usr/bin/env bash
set -euo pipefail

SELF_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd -P)"
source "$SELF_ROOT/docs/system/workspace/scripts/runtime/freely"

usage() {
  cat <<'EOF'
Usage:
  manager-watchdog.sh --project <abs_path> --recover-expected-workers
EOF
}

project=""
recover_expected_workers="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) project="$(abs_path_or_fail "${2:-}")"; shift 2 ;;
    --recover-expected-workers) recover_expected_workers="1"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; exit 1 ;;
  esac
done

[[ -n "$project" && "$recover_expected_workers" == "1" ]] || {
  usage >&2
  exit 1
}

load_config "$project"
printf '%s\n' "$(manager_runtime_recover_workers_if_needed "$project")"
