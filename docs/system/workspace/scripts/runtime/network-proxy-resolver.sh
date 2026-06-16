#!/usr/bin/env bash

freely_network_proxy_project_config_file() {
  local project="$1"
  printf '%s\n' "$project/.freely/config.toml"
}

freely_network_proxy_global_config_file() {
  local freely_home="${FREELY_HOME:-$HOME/.freely}"
  printf '%s\n' "$freely_home/config.toml"
}

freely_network_proxy_read_config_values() {
  local cfg="$1"
  (
    unset FREELY_NETWORK_PROXY_MODE FREELY_NETWORK_PROXY_URL FREELY_ALL_PROXY FREELY_HTTP_PROXY FREELY_HTTPS_PROXY FREELY_NO_PROXY
    [[ -f "$cfg" ]] || exit 0
    if [[ "$cfg" == *.toml ]]; then
      local freely_root
      freely_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd -P)"
      eval "$("$freely_root/bin/toml2env" --file "$cfg" 2>/dev/null)" || exit 0
    else
      # shellcheck disable=SC1090
      source "$cfg"
    fi
    printf '%s\x1f%s\x1f%s\x1f%s\x1f%s\x1f%s\n' \
      "${FREELY_NETWORK_PROXY_MODE:-}" \
      "${FREELY_NETWORK_PROXY_URL:-}" \
      "${FREELY_ALL_PROXY:-}" \
      "${FREELY_HTTP_PROXY:-}" \
      "${FREELY_HTTPS_PROXY:-}" \
      "${FREELY_NO_PROXY:-}"
  )
}

freely_network_proxy_resolve_config() {
  local project="$1"
  local project_cfg global_cfg
  local project_values global_values
  local project_mode="" project_url="" project_all="" project_http="" project_https="" project_no=""
  local global_mode="" global_url="" global_all="" global_http="" global_https="" global_no=""

  project_cfg="$(freely_network_proxy_project_config_file "$project")"
  global_cfg="$(freely_network_proxy_global_config_file)"

  project_values="$(freely_network_proxy_read_config_values "$project_cfg" || true)"
  if [[ -n "$project_values" ]]; then
    IFS=$'\x1f' read -r project_mode project_url project_all project_http project_https project_no <<<"$project_values"
  fi

  global_values="$(freely_network_proxy_read_config_values "$global_cfg" || true)"
  if [[ -n "$global_values" ]]; then
    IFS=$'\x1f' read -r global_mode global_url global_all global_http global_https global_no <<<"$global_values"
  fi

  FREELY_NETWORK_PROXY_MODE="inherit"
  FREELY_NETWORK_PROXY_URL=""
  FREELY_ALL_PROXY=""
  FREELY_HTTP_PROXY=""
  FREELY_HTTPS_PROXY=""
  FREELY_NO_PROXY=""

  case "${project_mode:-inherit}" in
    disabled)
      FREELY_NETWORK_PROXY_MODE="disabled"
      return 0
      ;;
    explicit)
      FREELY_NETWORK_PROXY_MODE="explicit"
      FREELY_NETWORK_PROXY_URL="${project_url:-$global_url}"
      FREELY_ALL_PROXY="${project_all:-$global_all}"
      FREELY_HTTP_PROXY="${project_http:-$global_http}"
      FREELY_HTTPS_PROXY="${project_https:-$global_https}"
      FREELY_NO_PROXY="${project_no:-$global_no}"
      return 0
      ;;
  esac

  case "${global_mode:-inherit}" in
    explicit|disabled)
      FREELY_NETWORK_PROXY_MODE="$global_mode"
      FREELY_NETWORK_PROXY_URL="$global_url"
      FREELY_ALL_PROXY="$global_all"
      FREELY_HTTP_PROXY="$global_http"
      FREELY_HTTPS_PROXY="$global_https"
      FREELY_NO_PROXY="$global_no"
      return 0
      ;;
  esac

  return 0
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

freely_network_proxy_has_effective_explicit_config() {
  local project="$1"
  freely_network_proxy_resolve_config "$project"
  [[ "$(freely_network_proxy_mode)" == "explicit" ]]
}

freely_apply_project_network_proxy_env() {
  local project="$1" mode base_proxy all_proxy http_proxy https_proxy no_proxy

  freely_network_proxy_resolve_config "$project"
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
        echo "[ERROR] FREELY_NETWORK_PROXY_MODE=explicit but no proxy values are set in $(freely_network_proxy_project_config_file "$project")" >&2
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
