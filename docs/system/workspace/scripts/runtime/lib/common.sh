#!/usr/bin/env bash
# runtime/lib/common.sh — helpers shared by the runtime monolith and the
# extracted `bin/<cmd>` projections (#4160).
#
# Why this file exists: before the split, `scripts/runtime/freely` defined
# `log_*`, `state_dir` and `run_dir_for_project` inline, so any extracted
# command either had to re-implement them (drift) or source the 27k-line
# monolith (circular). One small owner removes both options.
#
# Sourced by: scripts/runtime/freely, bin/test-gate, bin/evidence.
# Contract: no `exit` here — a sourced caller decides how to fail.

# One timestamp format for logs, one for machine-readable records. They differ
# on purpose: logs are wrapped in brackets, state files must stay bare.
_log_ts() { date -u +"[%Y-%m-%dT%H:%M:%SZ]" | tr -d '\n'; }
log_info() { echo "$(_log_ts) [INFO] $*" >&2; }
log_warn() { echo "$(_log_ts) [WARN] $*" >&2; }
log_error() { echo "$(_log_ts) [ERROR] $*" >&2; }

current_timestamp_utc_for_machine() {
  date -u '+%Y-%m-%dT%H:%M:%SZ'
}

# STATE_DIR_NAME keeps its single owner in the monolith for compatibility with
# callers that set it before sourcing; the fallback is the same literal.
state_dir() {
  local project="$1"
  echo "$project/${STATE_DIR_NAME:-.freely}"
}

run_dir_for_project() {
  local project="$1"
  echo "$(state_dir "$project")/run"
}
