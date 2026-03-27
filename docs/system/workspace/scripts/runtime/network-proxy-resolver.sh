#!/usr/bin/env bash

freely_network_proxy_config_file() {
  local project="$1"
  printf '%s\n' "$project/.freely/config.env"
}

freely_network_proxy_load_project_config() {
  local project="$1" cfg
  FREELY_NETWORK_PROXY_MODE=""
  FREELY_NETWORK_PROXY_URL=""
  FREELY_ALL_PROXY=""
  FREELY_HTTP_PROXY=""
  FREELY_HTTPS_PROXY=""
  FREELY_NO_PROXY=""

  cfg="$(freely_network_proxy_config_file "$project")"
  [[ -f "$cfg" ]] || return 0
  # shellcheck disable=SC1090
  source "$cfg"
}

freely_network_proxy_mode() {
  local mode="${FREELY_NETWORK_PROXY_MODE:-inherit}"
  case "$mode" in
    inherit|explicit|disabled) printf '%s\n' "$mode" ;;
    *) printf '%s\n' "inherit" ;;
  esac
}

freely_network_proxy_resolved_value() {
  local preferred="${1:-}" fallback="${2:-}"
  if [[ -n "$preferred" ]]; then
    printf '%s\n' "$preferred"
  else
    printf '%s\n' "$fallback"
  fi
}

freely_apply_project_network_proxy_env() {
  local project="$1" mode base_proxy all_proxy http_proxy https_proxy no_proxy

  freely_network_proxy_load_project_config "$project"
  mode="$(freely_network_proxy_mode)"

  case "$mode" in
    inherit)
      return 0
      ;;
    disabled)
      unset ALL_PROXY HTTP_PROXY HTTPS_PROXY NO_PROXY
      unset all_proxy http_proxy https_proxy no_proxy
      return 0
      ;;
    explicit)
      base_proxy="${FREELY_NETWORK_PROXY_URL:-}"
      all_proxy="$(freely_network_proxy_resolved_value "${FREELY_ALL_PROXY:-}" "${base_proxy:-${FREELY_HTTP_PROXY:-${FREELY_HTTPS_PROXY:-}}}")"
      http_proxy="$(freely_network_proxy_resolved_value "${FREELY_HTTP_PROXY:-}" "${base_proxy:-$all_proxy}")"
      https_proxy="$(freely_network_proxy_resolved_value "${FREELY_HTTPS_PROXY:-}" "${base_proxy:-$all_proxy}")"
      no_proxy="${FREELY_NO_PROXY:-}"

      [[ -n "$all_proxy" || -n "$http_proxy" || -n "$https_proxy" || -n "$no_proxy" ]] || {
        echo "[ERROR] FREELY_NETWORK_PROXY_MODE=explicit but no proxy values are set in $(freely_network_proxy_config_file "$project")" >&2
        return 1
      }

      export ALL_PROXY="$all_proxy"
      export HTTP_PROXY="$http_proxy"
      export HTTPS_PROXY="$https_proxy"
      export all_proxy="$all_proxy"
      export http_proxy="$http_proxy"
      export https_proxy="$https_proxy"

      if [[ -n "$no_proxy" ]]; then
        export NO_PROXY="$no_proxy"
        export no_proxy="$no_proxy"
      else
        unset NO_PROXY no_proxy
      fi
      ;;
    *)
      echo "[ERROR] unsupported FREELY_NETWORK_PROXY_MODE: $mode" >&2
      return 1
      ;;
  esac
}
