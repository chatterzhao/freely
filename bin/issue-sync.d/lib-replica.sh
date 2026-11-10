#!/usr/bin/env bash
# lib-replica.sh — sourced by bin/issue-sync, never executed directly.
# Platform-side replica guard (#4225): ask the platform before creating.

# ── Platform-side replica guard (#4225) ────────────────────────────────────
# `platform_ids` is a cache and can be partial after a degraded pull (R6).
# Before creating on a platform that appears missing locally, ask the platform
# itself (by [RAW-key]) whether a canonical replica already exists. The pure
# decision logic lives in sync/replica_guard.py; here we only do the I/O.
_GUARD_SCRIPT="$ROOT_DIR/docs/system/workspace/scripts/sync/replica_guard.py"
_ADAPTER_SCRIPT="$ROOT_DIR/docs/system/workspace/scripts/sync/platform-adapter.py"

# Print the discover-raw receipt (one JSON doc) for a raw key, or nothing on
# any transport failure. Never fabricate a verdict from a failed read.
_replica_receipt() {
  local raw_key="$1"
  [[ -f "$_ADAPTER_SCRIPT" && -f "$_GUARD_SCRIPT" ]] || return 0
  FREELY_PROJECT_ROOT="$ROOT_DIR" python3 "$_ADAPTER_SCRIPT" \
    discover-raw "$raw_key" 2>/dev/null || true
}

# Decide what to do for one platform that is missing from the local cache.
# Args: <guard_on> <receipt> <platform>  → echoes "<state>\t<id>\t<url>".
#   guard_on=0  → 'absent' (original create path, zero behavior change).
#   guard_on=1, no receipt → 'indeterminate' (transport blip, fail closed).
#   guard_on=1, receipt    → delegate to the pure classifier.
_replica_decide() {
  local guard_on="$1" receipt="$2" platform="$3"
  if [[ "$guard_on" != "1" ]]; then
    printf 'absent\t\t\n'; return 0
  fi
  if [[ -z "$receipt" ]]; then
    printf 'indeterminate\t\t\n'; return 0
  fi
  printf '%s\n' "$receipt" | python3 "$_GUARD_SCRIPT" "$platform" 2>/dev/null || \
    printf 'indeterminate\t\t\n'
}

# #4225: before a strict close, heal a partial `platform_ids` cache from
# platform-side discovery so close-platforms closes ALL real replicas, not just
# the ones the local cache happens to list (the other half of the degraded-pull
# defect). Healthy path (no platform missing) is a no-op. Only `present`
# replicas are backfilled; indeterminate/absent never fabricate an id.
_backfill_close_replicas() {
  local file="$1" local_id="$2" platform st rid rurl missing=0 receipt
  [[ "$local_id" == raw-* && -f "$_ADAPTER_SCRIPT" && -f "$_GUARD_SCRIPT" ]] || return 0
  # R12 invariant: a non-terminal raw must abort with ZERO writes. Only heal on
  # a terminal phase, so a rejected close never mutates the local doc.
  local _phase; _phase="$(_fm_get "$file" "phase_state")"
  [[ "$_phase" == "absorbed" || "$_phase" == "dropped" ]] || return 0
  if [[ -n "${GH_REPO:-}" ]] && ! _already_on_platform "$file" github; then missing=1; fi
  if [[ -n "${GITEE_REPO:-}" ]] && ! _already_on_platform "$file" gitee; then missing=1; fi
  [[ "$missing" == "1" ]] || return 0
  receipt="$(_replica_receipt "${local_id#raw-}")"
  [[ -n "$receipt" ]] || return 0
  for platform in github gitee; do
    _already_on_platform "$file" "$platform" && continue
    IFS=$'\t' read -r st rid rurl <<<"$(printf '%s\n' "$receipt" | python3 "$_GUARD_SCRIPT" "$platform" 2>/dev/null || printf 'indeterminate\t\t\n')"
    if [[ "$st" == "present" && -n "$rid" ]]; then
      echo "[issue-sync] close: discovered $platform replica $rid; backfilling platform_ids so it gets closed"
      _update_platform_ids "$file" "$platform" "$rid" "$rurl"
    fi
  done
}
