#!/usr/bin/env bash
# tool-launchers.sh: AI tool abstraction layer — per-tool launch syntax and adapter routing.
#
# Responsibilities:
#   - Per-tool direct CLI launch syntax (claude, codex, kiro-cli, iflow, opencode)
#   - Per-tool ACP launch syntax (claude-agent-acp, codex-acp via run-acp-prompt.py)
#   - Adapter dispatch: direct vs acp (DEPRECATED(direct): to be removed when ACP stable)
#   - Session state mapping: fresh → new, resume → resume, fork → new+context
#   - Tool capability/feature detection (codex-cli, slot switching, MCP)
#   - Network proxy resolution for each tool
#
# Direct mode (DEPRECATED):  monitor-ai-cli.sh calls tool_run_from_prompt_file → exec tool CLI
# ACP mode (primary):        monitor-ai-acp.sh calls tool_run_from_prompt_file → exec run-acp-prompt.py
#
# Entry points used by monitors:
#   tool_run_from_prompt_file <project> <tool> <adapter> <model> ... <launch_kind>
#   tool_run_direct_from_prompt_file  (direct mode, DEPRECATED)
#   tool_run_acp_from_prompt_file     (ACP native)
#   tool_supported_adapters <tool>
#   tool_supported_launch_kinds_for_adapter <tool> <adapter>

_tool_launchers_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

freely_tool_launchers_repo_root() {
  local script_dir="$1" root
  root="$(git -C "$script_dir" rev-parse --show-toplevel 2>/dev/null || true)"
  if [[ -n "$root" ]]; then
    printf '%s\n' "$root"
    return 0
  fi
  case "$script_dir" in
    */docs/system/workspace/scripts/runtime)
      printf '%s\n' "${script_dir%/docs/system/workspace/scripts/runtime}"
      ;;
    *)
      printf '%s\n' "$script_dir"
      ;;
  esac
}

SELF_ROOT="$(freely_tool_launchers_repo_root "$_tool_launchers_dir")"

NETWORK_PROXY_RESOLVER_LIB="$SELF_ROOT/docs/system/workspace/scripts/runtime/network-proxy-resolver.sh"
[[ -f "$NETWORK_PROXY_RESOLVER_LIB" ]] || {
  echo "[ERROR] missing network proxy resolver module: $NETWORK_PROXY_RESOLVER_LIB" >&2
  return 1
}
# shellcheck disable=SC1090
source "$NETWORK_PROXY_RESOLVER_LIB"

SESSION_CACHE_LIB="$SELF_ROOT/docs/system/workspace/scripts/runtime/session-cache.sh"
[[ -f "$SESSION_CACHE_LIB" ]] && source "$SESSION_CACHE_LIB"

RUNTIME_ACP_PROMPT_CLIENT="$SELF_ROOT/docs/system/workspace/scripts/runtime/run-acp-prompt.py"

codex_slot_switch_lock_dir_for_launch() {
  printf '%s\n' "${AI_CLI_SWITCH_LOCK_DIR:-$HOME/.codex/slot-switch.lock}"
}

codex_slot_switch_lock_state_file_for_launch() {
  printf '%s\n' "$(codex_slot_switch_lock_dir_for_launch)/state.env"
}

codex_slot_switch_lock_owner_pid_for_launch() {
  local state_file
  state_file="$(codex_slot_switch_lock_state_file_for_launch)"
  [[ -f "$state_file" ]] || return 0
  sed -n 's/^owner_pid=//p' "$state_file" | tail -n 1
}

codex_slot_switch_lock_cleanup_if_stale_for_launch() {
  local lock_dir owner_pid
  lock_dir="$(codex_slot_switch_lock_dir_for_launch)"
  [[ -d "$lock_dir" ]] || return 0
  owner_pid="$(codex_slot_switch_lock_owner_pid_for_launch)"
  if [[ -z "$owner_pid" ]] || ! kill -0 "$owner_pid" 2>/dev/null; then
    rm -rf "$lock_dir"
  fi
}

codex_slot_switch_in_progress_for_launch() {
  local lock_dir owner_pid inherited_owner_pid
  codex_slot_switch_lock_cleanup_if_stale_for_launch
  lock_dir="$(codex_slot_switch_lock_dir_for_launch)"
  [[ -d "$lock_dir" ]] || return 1
  owner_pid="$(codex_slot_switch_lock_owner_pid_for_launch)"
  inherited_owner_pid="${AI_CLI_SWITCH_LOCK_OWNER_PID:-}"
  [[ -n "$owner_pid" ]] || return 1
  [[ "$owner_pid" != "$$" ]] || return 1
  [[ -z "$inherited_owner_pid" || "$owner_pid" != "$inherited_owner_pid" ]] || return 1
  kill -0 "$owner_pid" 2>/dev/null
}

wait_for_codex_slot_switch_idle_before_launch() {
  local timeout_secs="${FREELY_ACCOUNT_SWITCH_WAIT_SECS:-60}"
  local interval_secs="${FREELY_ACCOUNT_SWITCH_WAIT_INTERVAL_SECS:-1}"
  local start_ts now owner_pid waiting_logged=0
  [[ "$timeout_secs" =~ ^[0-9]+$ ]] || timeout_secs=60
  [[ "$interval_secs" =~ ^[0-9]+$ ]] || interval_secs=1
  start_ts="$(date +%s)"

  while codex_slot_switch_in_progress_for_launch; do
    if [[ "$waiting_logged" == "0" ]]; then
      owner_pid="$(codex_slot_switch_lock_owner_pid_for_launch)"
      echo "[WARN] codex slot switch is already in progress (owner_pid=${owner_pid:-unknown}); waiting before codex launch" >&2
      waiting_logged=1
    fi
    now="$(date +%s)"
    if (( now - start_ts >= timeout_secs )); then
      echo "[ERROR] timed out waiting for codex slot switch to finish before codex launch" >&2
      return 1
    fi
    sleep "$interval_secs"
  done
}

codex_acp_version_for_launch() {
  printf '%s\n' "${FREELY_CODEX_ACP_VERSION:-0.15.0}"
}

codex_acp_platform_triplet_for_launch() {
  local uname_s uname_m
  uname_s="$(uname -s)"
  uname_m="$(uname -m)"
  case "$uname_s:$uname_m" in
    Darwin:arm64) printf 'aarch64-apple-darwin\n' ;;
    Darwin:x86_64) printf 'x86_64-apple-darwin\n' ;;
    Linux:aarch64|Linux:arm64) printf 'aarch64-unknown-linux-gnu\n' ;;
    Linux:x86_64) printf 'x86_64-unknown-linux-gnu\n' ;;
    *)
      echo "[ERROR] unsupported platform for codex-acp binary: ${uname_s}:${uname_m}" >&2
      return 1
      ;;
  esac
}

codex_acp_cache_dir_for_launch() {
  printf '%s\n' "${FREELY_ACP_CACHE_DIR:-$HOME/.cache/freely/acp}"
}

codex_acp_download_url_for_launch() {
  local version="$1" triplet="$2"
  printf 'https://github.com/zed-industries/codex-acp/releases/download/v%s/codex-acp-%s-%s.tar.gz\n' "$version" "$version" "$triplet"
}

ensure_codex_acp_binary_for_launch() {
  local override="${FREELY_CODEX_ACP_BIN:-}"
  local version triplet cache_root install_dir binary_path archive_url tmp_archive

  if [[ -n "$override" ]]; then
    [[ -x "$override" ]] || {
      echo "[ERROR] FREELY_CODEX_ACP_BIN is not executable: $override" >&2
      return 1
    }
    printf '%s\n' "$override"
    return 0
  fi

  version="$(codex_acp_version_for_launch)"
  triplet="$(codex_acp_platform_triplet_for_launch)" || return 1
  cache_root="$(codex_acp_cache_dir_for_launch)"
  install_dir="$cache_root/codex-acp/$version/$triplet"
  binary_path="$install_dir/codex-acp"

  if [[ -x "$binary_path" ]]; then
    printf '%s\n' "$binary_path"
    return 0
  fi

  mkdir -p "$install_dir"
  tmp_archive="$(mktemp "$install_dir/codex-acp.XXXXXX")"
  archive_url="$(codex_acp_download_url_for_launch "$version" "$triplet")"
  echo "[INFO] downloading codex-acp ${version} for ${triplet}" >&2
  curl -fsSL "$archive_url" -o "$tmp_archive" || {
    rm -f "$tmp_archive"
    echo "[ERROR] failed to download codex-acp from $archive_url" >&2
    return 1
  }
  tar -xzf "$tmp_archive" -C "$install_dir" || {
    rm -f "$tmp_archive"
    echo "[ERROR] failed to unpack codex-acp archive: $tmp_archive" >&2
    return 1
  }
  rm -f "$tmp_archive"
  [[ -x "$binary_path" ]] || chmod +x "$binary_path" 2>/dev/null || true
  [[ -x "$binary_path" ]] || {
    echo "[ERROR] codex-acp binary missing after install: $binary_path" >&2
    return 1
  }
  printf '%s\n' "$binary_path"
}

tool_default_capabilities() {
  local tool="$1"
  case "$tool" in
    cc-use-codex-cli) printf 'codex-cli\n' ;;
    *) printf '\n' ;;
  esac
}

tool_default_policy() {
  local tool="$1"
  case "$tool" in
    cc-use-codex-cli) printf 'prefer-codex-for-repo-work\n' ;;
    *) printf '\n' ;;
  esac
}

tool_default_adapter() {
  local tool="$1"
  [[ -n "$tool" ]] || {
    printf '\n'
    return 0
  }
  printf 'direct\n'
}

tool_supported_adapters() {
  local tool="$1"
  tool="$(_resolve_tool_family "$tool")"
  case "$tool" in
    codex)
      printf 'direct\nacp\n'
      ;;
    kiro-cli|iflow|cc|cc-use-codex-cli|claude|opencode|test-sleep|test-compact|test-once|test-session|test-route-only|test-scripted)
      printf 'direct\nacp\n'
      ;;
    *)
      printf 'direct\n'
      ;;
  esac
}

tool_adapter_is_supported() {
  local tool="$1" adapter="$2"
  [[ -n "$tool" && -n "$adapter" ]] || return 1
  printf '%s\n' "$(tool_supported_adapters "$tool")" | tr ',' '\n' | sed 's/^ *//; s/ *$//' | grep -Fxq "$adapter"
}

tool_supported_launch_kinds_for_adapter() {
  local tool="$1" adapter="$2"
  tool="$(_resolve_tool_family "$tool")"
  case "$tool:$adapter" in
    codex:acp)
      # codex-acp supports full ACP session lifecycle (Zed codex-acp)
      printf 'fresh\nresume\nfork\nfresh_with_handoff\nprompt\n'
      ;;
    *:acp)
      # ACP native: session states + prompt (multi-turn delta)
      printf 'fresh\nresume\nfork\nfresh_with_handoff\nprompt\n'
      ;;
    *)
      # direct mode (DEPRECATED: will be removed when ACP is stable)
      printf 'fresh\nresume\nfresh_with_handoff\n'
      ;;
  esac
}

tool_adapter_supports_launch_kind() {
  local tool="$1" adapter="$2" launch_kind="$3"
  [[ -n "$tool" && -n "$adapter" && -n "$launch_kind" ]] || return 1
  printf '%s\n' "$(tool_supported_launch_kinds_for_adapter "$tool" "$adapter")" | tr ',' '\n' | sed 's/^ *//; s/ *$//' | grep -Fxq "$launch_kind"
}

# _resolve_type_expansion: resolve a name via `type`, return the expansion.
# Handles zsh ("is an alias for") and bash ("is aliased to") formats.
# Returns nothing if the name is not an alias.
_resolve_type_expansion() {
  local name="$1" type_output
  type_output=$(${SHELL:-bash} -ic "type '$name' 2>&1" 2>/dev/null) || true
  if echo "$type_output" | grep -q 'is an alias for'; then
    echo "$type_output" | sed 's/.*is an alias for //'
  elif echo "$type_output" | grep -q 'is aliased to'; then
    echo "$type_output" | sed 's/.*is aliased to .//; s/.$//'
  fi
}

# _strip_env_prefix: strip leading VAR=val assignments from an alias expansion.
# Handles VAR=val, VAR="quoted val", VAR='quoted val' patterns.
# Uses case-based prefix matching instead of bash regex for portability.
_strip_env_prefix() {
  local val="$1"
  while true; do
    # Trim leading whitespace
    val="${val#"${val%%[![:space:]]*}"}"
    # Check if the next token looks like an env var assignment (VAR=)
    case "$val" in
      [a-zA-Z_]*=*) ;;
      *) break ;;
    esac
    val="${val#*=}"
    if [[ "$val" == \"* ]]; then
      val="${val#\"}"           # strip opening quote
      val="${val#*\"}"          # skip to after closing quote
      val="${val# }"            # strip trailing space
    elif [[ "$val" == \'* ]]; then
      val="${val#\'}"
      val="${val#*\'}"
      val="${val# }"
    else
      val="${val#*[[:space:]]}" # unquoted: skip to next space
    fi
  done
  printf '%s\n' "$val"
}

# _resolve_tool_family: resolve any alias/function/binary to known tool family.
# Uses `type` for unified cross-shell resolution. No hardcoded prefix lists needed.
# Supports recursive aliases (alias → another alias → binary).
_resolve_tool_family() {
  local tool="$1"
  # Strip slot suffix: codex-apikey-xxx → codex, claude-account-xxx → claude
  case "$tool" in
    *-apikey-*) tool="${tool%%-apikey-*}" ;;
    *-account-*) tool="${tool%%-account-*}" ;;
  esac
  case "$tool" in
    codex|claude|cc|cc-use-codex-cli|kiro-cli|iflow|opencode) printf '%s\n' "$tool"; return 0 ;;
  esac
  local expansion binary
  expansion=$(_resolve_type_expansion "$tool")
  if [[ -z "${expansion:-}" ]]; then
    # Not an alias — try as a binary path
    local bin_output
    bin_output=$(${SHELL:-bash} -ic "type '$tool' 2>&1" 2>/dev/null) || true
    if echo "$bin_output" | grep -q ' is /'; then
      expansion=$(echo "$bin_output" | sed 's/.* is //')
    fi
  fi
  if [[ -n "${expansion:-}" ]]; then
    binary="$(_strip_env_prefix "$expansion")"
    binary="${binary%% *}"
    binary=$(basename "$binary" 2>/dev/null || echo "$binary")
    case "$binary" in
      claude)  printf 'claude\n'; return 0 ;;
      codex|kiro-cli|iflow|opencode) printf '%s\n' "$binary"; return 0 ;;
      *)
        local rec_expansion rec_binary
        rec_expansion=$(_resolve_type_expansion "$binary")
        if [[ -n "${rec_expansion:-}" ]]; then
          rec_binary="$(_strip_env_prefix "$rec_expansion")"
          rec_binary="${rec_binary%% *}"
          rec_binary=$(basename "$rec_binary" 2>/dev/null || echo "$rec_binary")
          case "$rec_binary" in
            claude)  printf 'claude\n'; return 0 ;;
            codex|kiro-cli|iflow|opencode) printf '%s\n' "$rec_binary"; return 0 ;;
          esac
        fi
        ;;
    esac
  fi
  printf '%s\n' "$tool"
}

# _apply_tool_alias_settings: resolve alias, extract --settings path, export env vars.
# For ACP mode, this is how per-alias settings (e.g. cc-ds-flash-auto) are applied.
_apply_tool_alias_settings() {
  local tool="$1"
  local resolved alias_path
  case "$tool" in
    codex|claude|cc|cc-use-codex-cli|kiro-cli|iflow|opencode) return 0 ;;
  esac
  resolved=$(_resolve_type_expansion "$tool")
  [[ -n "$resolved" ]] || return 0
  local first_binary="${resolved%% *}"
  if [[ ! "$first_binary" =~ ^(claude|codex|kiro-cli|iflow|opencode)$ ]]; then
    local rec_resolved
    rec_resolved=$(_resolve_type_expansion "$first_binary")
    [[ -n "$rec_resolved" ]] && resolved="$rec_resolved"
  fi
  # Export env var assignments from alias prefix (e.g. OPENCODE_CONFIG=... opencode)
  local remainder="$resolved"
  while true; do
    local _trimmed="${remainder#"${remainder%%[![:space:]]*}"}"
    case "$_trimmed" in
      [a-zA-Z_]*=*) ;;
      *) break ;;
    esac
    local var_name="${remainder%%=*}"
    var_name="${var_name##* }"  # strip leading spaces
    remainder="${remainder#*=}"
    if [[ "$remainder" == \"* ]]; then
      remainder="${remainder#\"}"
      local var_val="${remainder%%\"*}"
      export "$var_name"="$var_val"
      remainder="${remainder#*\"}"
      remainder="${remainder# }"
    elif [[ "$remainder" == \'* ]]; then
      remainder="${remainder#\'}"
      local var_val="${remainder%%\'*}"
      export "$var_name"="$var_val"
      remainder="${remainder#*\'}"
      remainder="${remainder# }"
    else
      local var_val="${remainder%%[[:space:]]*}"
      export "$var_name"="$var_val"
      remainder="${remainder#*[[:space:]]}"
    fi
  done
  # Extract --settings <path> from the remainder
  alias_path=$(echo "$remainder" | sed -n 's/.*--settings \([^ ]*\).*/\1/p')
  [[ -n "$alias_path" ]] || return 0
  alias_path="${alias_path/#\~/$HOME}"
  [[ -f "$alias_path" ]] || return 0
  while IFS='=' read -r key value; do
    [[ -n "$key" ]] || continue
    export "$key"="$value"
  done <<<"$(python3 -c "
import json, sys
try:
    with open('$alias_path') as f:
        d = json.load(f)
    env = d.get('env', {})
    for k, v in env.items():
        print(f'{k}={v}')
    # Read permission mode: top-level 'permissionMode' or nested 'permissions.defaultMode'
    pm = d.get('permissionMode', '') or d.get('permissions', {}).get('defaultMode', '')
    if pm:
        print(f'CLAUDE_CODE_PERMISSION_MODE={pm}')
    settings_file = '${alias_path}'
    print(f'CLAUDE_CODE_SETTINGS_FILE={settings_file}')
except: pass
" 2>/dev/null)"
}

tool_has_capability() {
  local capabilities="$1" capability="$2"
  [[ -n "$capability" ]] || return 1
  printf '%s\n' "$capabilities" | tr ',' '\n' | sed 's/^ *//; s/ *$//' | grep -Fxq "$capability"
}

tool_accepts_explicit_resume_target() {
  local tool="$1"
  tool="$(_resolve_tool_family "$tool")"
  case "$tool" in
    codex|iflow|opencode) return 0 ;;
    *) return 1 ;;
  esac
}

tool_requires_explicit_resume_target() {
  local tool="$1"
  tool="$(_resolve_tool_family "$tool")"
  case "$tool" in
    codex) return 0 ;;
    *) return 1 ;;
  esac
}

project_worktrees_root_for_launch() {
  local project="$1"
  local project_parent project_name
  project_parent="$(dirname "$project")"
  if [[ "$(basename "$project_parent")" == *-worktrees ]]; then
    printf '%s\n' "$project_parent"
    return 0
  fi
  project_name="$(basename "$project")"
  printf '%s\n' "${project_parent}/${project_name}-worktrees"
}

claude_home_mode_for_launch() {
  printf '%s\n' "${FREELY_CLAUDE_HOME_MODE:-project}"
}

claude_runtime_home_for_launch() {
  local project="$1"
  printf '%s\n' "$project/.freely/tool-homes/claude"
}

ensure_claude_runtime_home_for_launch() {
  local project="$1" claude_home
  claude_home="$(claude_runtime_home_for_launch "$project")"
  mkdir -p \
    "$claude_home/.claude" \
    "$claude_home/.claude/projects" \
    "$claude_home/.claude/plugins" \
    "$claude_home/.claude/statsig" \
    "$claude_home/.claude/session-env" \
    "$claude_home/.claude/sessions"
  printf '%s\n' "$claude_home"
}

tool_supports_add_dir_boundary() {
  local tool="$1"
  case "$tool" in
    codex|iflow|claude|claude|cc|cc-use-codex-cli) return 0 ;;
    *) return 1 ;;
  esac
}

tool_boundary_add_dir() {
  local tool="$1" project="$2" worktrees_root
  tool_supports_add_dir_boundary "$tool" || return 0
  worktrees_root="$(project_worktrees_root_for_launch "$project")"
  [[ -n "$worktrees_root" && "$worktrees_root" != "$project" ]] || return 0
  printf '%s\n' "$worktrees_root"
}

project_branch_for_launch() {
  local project="$1"
  git -C "$project" branch --show-current 2>/dev/null || true
}

protected_branch_for_launch() {
  local branch="$1"
  [[ "$branch" == "main" || "$branch" == "develop" || "$branch" == test-pre-merge-* ]]
}

cc_codex_policy_prompt() {
  local policy="${1:-}"
  local project_root="${2:-}"
  local codex_model="${3:-gpt-5.4}"
  local codex_sandbox="${4:-workspace-write}"
  local codex_approval_policy="${5:-never}"
  local codex_cwd_mode="${6:-project-root}"
  local worktrees_root="${7:-}"
  local branch="${8:-}"
  local cwd_guidance
  cwd_guidance="- The repository project root (${project_root}) remains the primary integration cwd. When calling the Codex MCP tool for a new session, use cwd=${project_root} unless the task needs owner development on a protected branch."
  if protected_branch_for_launch "$branch"; then
    cwd_guidance="- The current branch is protected (${branch}). Keep ${project_root} for read/merge/integration work, but for any new owner-development or staged repository-writing Codex MCP session, first create or enter a dedicated worktree under ${worktrees_root} and use that worktree path as cwd instead of ${project_root}."
  fi
  cat <<EOF
Freely runtime policy:
- You are running as Claude Code inside Freely.
- If the codex-cli MCP tool is available, prefer using it for repository implementation, bug fixing, code review, and verification work.
- For new repository work, start a Codex MCP session instead of keeping the entire implementation inside Claude.
- For continuation of the same repository task, prefer continuing the existing Codex MCP thread when prior context already points to one.
- When calling the Codex MCP tool for a new session, pass these parameters unless the task explicitly requires something stricter:
  - model=${codex_model}
  - sandbox=${codex_sandbox}
  - approval-policy=${codex_approval_policy}
  - cwd policy: ${codex_cwd_mode}
- Repository integration root: ${project_root}
- Allowed sibling worktrees root: ${worktrees_root:-unavailable}
- ${cwd_guidance#- }
- When continuing an existing Codex MCP thread, preserve the same repository-root cwd and the same non-interactive approval policy unless the task explicitly requires a stricter mode.
- The current runtime is non-interactive; permissions are configured by the tool-native config. Do not ask the user for confirmations.
- Current cc policy: ${policy:-default}
EOF
}

# DEPRECATED(direct): direct mode will be removed once ACP is stable.
# Only maintain for tools without ACP support (kiro-cli, iflow, opencode).
tool_run_direct_from_prompt_file() {
  local project="$1"
  local tool="$2"
  local model="${3:-}"
  local reasoning_effort="${4:-}"
  local mode="$5"
  local prompt_file="$6"
  local launch_kind="$7"
  local tool_capabilities="${8:-}"
  local tool_policy="${9:-}"
  local codex_capability_model="${10:-gpt-5.4}"
  local codex_capability_sandbox="${11:-workspace-write}"
  local codex_capability_approval_policy="${12:-never}"
  local codex_capability_cwd_mode="${13:-project-root}"
  local debug_log_file="${14:-}"
  local claude_session_id="${15:-}"
  local tool_resume_target="${16:-}"

  local -a tool_extra_args=()
  if [[ -n "${AI_TOOL_EXTRA_ARGS:-}" ]]; then
    IFS=' ' read -ra tool_extra_args <<< "${AI_TOOL_EXTRA_ARGS}"
  fi

  # Resolve shell alias if tool is not a known command (e.g. ccds-auto -> claude)
  _resolve_tool_alias() {
    local name="$1"
    local resolved
    # Known tool families: return as-is
    case "$name" in
      codex|kiro-cli|iflow|claude|cc|cc-use-codex-cli|opencode|test-sleep|test-compact|test-once|test-session|test-route-only|test-scripted)
        printf '%s\n' "$name"
        return 0
        ;;
    esac
    # Unknown name: try zsh alias resolution (user's .zshrc aliases)
    resolved=$(${SHELL:-bash} -ic "alias '$name' 2>/dev/null" 2>/dev/null | sed -n "s/^${name}='\(.*\)'$/\1/p")
    if [[ -n "$resolved" ]]; then
      printf '%s\n' "$resolved"
      return 0
    fi
    # Unresolved: return as-is (may fail later)
    printf '%s\n' "$name"
    return 0
  }

  local resolved_tool_full
  resolved_tool_full=$(_resolve_tool_alias "$tool")
  if [[ "$resolved_tool_full" != "$tool" ]]; then
    # Alias was resolved: extract binary and prepend extra args to tool_extra_args
    local resolved_bin="${resolved_tool_full%% *}"
    local alias_extra="${resolved_tool_full#* }"
    if [[ "$alias_extra" != "$resolved_tool_full" ]]; then
      local -a alias_args
      IFS=' ' read -ra alias_args <<< "$alias_extra"
      tool_extra_args=("${alias_args[@]}" "${tool_extra_args[@]:-}")
    fi
    tool="$resolved_bin"
  fi

  # Allow AI_TOOL_FAMILY to override detected tool family (e.g. alias resolves to
  # a wrapper script, but resume/session conventions follow a known family)
  if [[ -n "${AI_TOOL_FAMILY:-}" ]]; then
    tool="${AI_TOOL_FAMILY}"
  fi

  case "$tool" in
    codex)
      wait_for_codex_slot_switch_idle_before_launch || return 1
      freely_apply_project_network_proxy_env "$project"
      local worktrees_root
      worktrees_root="$(tool_boundary_add_dir "$tool" "$project")"
      local -a args=(exec --skip-git-repo-check -C "$project")
      [[ -n "$worktrees_root" ]] && args+=(--add-dir "$worktrees_root")
      if [[ "$launch_kind" == "resume" ]]; then
        [[ -n "$tool_resume_target" ]] || {
          echo "[ERROR] codex resume requires an explicit session target" >&2
          return 1
        }
        args=(exec resume "$tool_resume_target" --skip-git-repo-check)
      fi
      [[ -n "$model" ]] && args+=(-m "$model")
      [[ -n "$reasoning_effort" ]] && args+=(-c "model_reasoning_effort=\"$reasoning_effort\"")
      [[ "$mode" == "auto" ]] && args+=(--dangerously-bypass-approvals-and-sandbox)
      exec codex "${tool_extra_args[@]:-}" "${args[@]}" - <"$prompt_file"
      ;;
    iflow)
      local worktrees_root
      worktrees_root="$(tool_boundary_add_dir "$tool" "$project")"
      local -a args=()
      [[ -n "$worktrees_root" ]] && args+=(--add-dir "$worktrees_root")
      [[ -n "$model" ]] && args+=(-m "$model")
      if [[ "$launch_kind" == "resume" ]]; then
        if [[ -n "$tool_resume_target" ]]; then
          args+=(-r "$tool_resume_target")
        else
          args+=(-c)
        fi
      fi
      if [[ "$mode" == "auto" ]]; then
        exec iflow "${tool_extra_args[@]:-}" "${args[@]}" -p "$(cat "$prompt_file")" -y --max-turns 100
      else
        exec iflow "${tool_extra_args[@]:-}" "${args[@]}" -p "$(cat "$prompt_file")" --default --max-turns 100
      fi
      ;;
    kiro-cli)
      local selected_model="${model:-auto}"
      if [[ "$launch_kind" == "resume" ]]; then
        if [[ "$mode" == "auto" ]]; then
          exec kiro-cli "${tool_extra_args[@]:-}" chat --resume --no-interactive --trust-all-tools --model "$selected_model" "继续上次未完成工作，按项目意图和宪法持续推进。"
        else
          exec kiro-cli "${tool_extra_args[@]:-}" chat --resume --model "$selected_model" "继续上次未完成工作，按项目意图和宪法持续推进。"
        fi
      fi

      if [[ "$mode" == "auto" ]]; then
        exec kiro-cli "${tool_extra_args[@]:-}" chat --no-interactive --trust-all-tools --model "$selected_model" <"$prompt_file"
      else
        exec kiro-cli "${tool_extra_args[@]:-}" chat --model "$selected_model" <"$prompt_file"
      fi
      ;;
    claude|cc|cc-use-codex-cli)
      local system_prompt worktrees_root project_branch claude_home_mode claude_home
      local -a args=(-p)
      worktrees_root="$(tool_boundary_add_dir "$tool" "$project")"
      project_branch="$(project_branch_for_launch "$project")"
      claude_home_mode="$(claude_home_mode_for_launch)"
      claude_home=""
      if [[ "$tool" == "cc" && "$claude_home_mode" == "project" ]]; then
        claude_home="$(ensure_claude_runtime_home_for_launch "$project")"
      fi
      [[ -n "$worktrees_root" ]] && args+=(--add-dir "$worktrees_root")
      [[ -n "$debug_log_file" ]] && args+=(--debug-file "$debug_log_file")
      # Session strategy: use the session-cache module if available.
      if [[ "$launch_kind" == "fork" ]]; then
        if [[ -n "$tool_resume_target" && -n "$claude_session_id" ]] && declare -f session_fork_args >/dev/null 2>&1; then
          while IFS= read -r arg; do [[ -n "$arg" ]] && args+=("$arg"); done <<<"$(session_fork_args "$tool" "$tool_resume_target" "$claude_session_id")"
        elif [[ -n "$tool_resume_target" && -n "$claude_session_id" ]]; then
          args+=(--resume "$tool_resume_target" --fork-session --session-id "$claude_session_id")
        elif [[ -n "$tool_resume_target" ]]; then
          args+=(--resume "$tool_resume_target" --fork-session)
        elif [[ -n "$claude_session_id" ]]; then
          args+=(--session-id "$claude_session_id")
        fi
      elif [[ "$launch_kind" == "resume" ]]; then
        if [[ -n "$tool_resume_target" ]] && declare -f session_resume_args >/dev/null 2>&1; then
          while IFS= read -r arg; do [[ -n "$arg" ]] && args+=("$arg"); done <<<"$(session_resume_args "$tool" "$tool_resume_target")"
        elif [[ -n "$tool_resume_target" ]]; then
          args+=(--resume "$tool_resume_target")
        elif [[ -n "$claude_session_id" ]]; then
          args+=(--session-id "$claude_session_id")
        fi
      elif [[ -n "$claude_session_id" ]]; then
        if declare -f session_fresh_args >/dev/null 2>&1; then
          while IFS= read -r arg; do [[ -n "$arg" ]] && args+=("$arg"); done <<<"$(session_fresh_args "$tool" "$claude_session_id")"
        else
          args+=(--session-id "$claude_session_id")
        fi
      fi
      [[ -n "$model" && "$model" != "default" ]] && args+=(--model "$model")
      [[ -n "$reasoning_effort" ]] && args+=(--effort "$reasoning_effort")
      if tool_has_capability "$tool_capabilities" "codex-cli"; then
        system_prompt="$(cc_codex_policy_prompt "$tool_policy" "$project" "$codex_capability_model" "$codex_capability_sandbox" "$codex_capability_approval_policy" "$codex_capability_cwd_mode" "$worktrees_root" "$project_branch")"
        args+=(--append-system-prompt "$system_prompt")
      fi
      if [[ -n "$claude_home" ]]; then
        exec env HOME="$claude_home" claude "${tool_extra_args[@]:-}" "${args[@]}" <"$prompt_file"
      fi
      exec claude "${tool_extra_args[@]:-}" "${args[@]}" <"$prompt_file"
      ;;

    opencode)
      local -a args=(run --print-logs)
      [[ -n "$project" ]] && args+=("--dir" "$project")
      if [[ "$launch_kind" == "resume" ]] && [[ -n "$tool_resume_target" ]]; then
        args+=("-s" "$tool_resume_target")
      fi
      exec opencode "${tool_extra_args[@]:-}" "${args[@]}" "$(cat "$prompt_file")"
      ;;
    test-sleep)
      exec bash -lc 'echo "[TEST] mock AI CLI started"; sleep 5'
      ;;
    test-compact)
      exec bash -lc 'echo "[TEST] mock AI CLI started"; echo "context compacted"; sleep 1'
      ;;
    test-once)
      exec bash -lc 'echo "[TEST] mock AI CLI started"; sleep 1'
      ;;
    test-session)
      exec bash -lc 'echo "session id: test-session"; echo "[TEST] mock AI CLI started"; sleep 1'
      ;;
    test-route-only)
      exec bash -lc "cat <<'EOF'
[TEST] mock AI CLI started
selected_tool = test-route-only
target_skill_or_loop = skill:freely-doc-B2_IBM-execution
\`next_prompt\`：
```text
你现在承接第二跳，直接进入 skill:freely-doc-B2_IBM-execution 并修改真实文档产物。
```
EOF
sleep 1"
      ;;
    test-scripted)
      [[ -n "${FREELY_TEST_SCRIPTED_TOOL_BIN:-}" ]] || {
        echo "[ERROR] test-scripted requires FREELY_TEST_SCRIPTED_TOOL_BIN" >&2
        return 1
      }
      [[ -x "${FREELY_TEST_SCRIPTED_TOOL_BIN:-}" ]] || {
        echo "[ERROR] test-scripted script is not executable: ${FREELY_TEST_SCRIPTED_TOOL_BIN:-}" >&2
        return 1
      }
      exec "${FREELY_TEST_SCRIPTED_TOOL_BIN}" \
        --project "$project" \
        --prompt-file "$prompt_file" \
        --launch-kind "$launch_kind" \
        --mode "$mode" \
        --tool-resume-target "$tool_resume_target"
      ;;
    *)
      echo "[ERROR] unsupported tool: $tool" >&2
      return 1
      ;;
  esac
}

tool_run_acp_from_prompt_file() {
  local project="$1"
  local tool="$2"
  local model="${3:-}"
  local reasoning_effort="${4:-}"
  local mode="$5"
  local prompt_file="$6"
  local launch_kind="$7"
  local tool_capabilities="${8:-}"
  local tool_policy="${9:-}"
  local codex_capability_model="${10:-gpt-5.4}"
  local codex_capability_sandbox="${11:-workspace-write}"
  local codex_capability_approval_policy="${12:-never}"
  local codex_capability_cwd_mode="${13:-project-root}"
  local debug_log_file="${14:-}"
  local claude_session_id="${15:-}"
  local tool_resume_target="${16:-}"

  # Apply per-alias settings env vars (e.g. cc-ds-flash-auto → Flash model)
  # Must be called BEFORE alias resolution to extract --settings from the alias.
  _apply_tool_alias_settings "$tool"

  # Resolve alias (cc-ds-flash-auto → claude) before per-tool dispatch
  tool="$(_resolve_tool_family "$tool")"

  local bridge_socket
  bridge_socket="$(_bridge_socket "$project")"

  case "$tool" in
    codex)
      [[ -f "$RUNTIME_ACP_PROMPT_CLIENT" ]] || {
        echo "[ERROR] missing ACP prompt client: $RUNTIME_ACP_PROMPT_CLIENT" >&2
        return 1
      }
      local codex_acp_bin
      codex_acp_bin="$(ensure_codex_acp_binary_for_launch)" || return 1
      # codex-acp bridge socket (separate from claude bridge)
      local _hash; _hash=$(printf "%s" "$project" | shasum -a 256 | cut -c1-16)
      local codex_bridge_socket="/tmp/freely-acp-$_hash.sock"
      freely_apply_project_network_proxy_env "$project"
      exec python3 "$RUNTIME_ACP_PROMPT_CLIENT" \
        --bridge-socket "$codex_bridge_socket" \
        --cwd "$project" \
        --prompt-file "$prompt_file" \
        --mode "$mode" \
        --model "$model" \
        --launch-kind "$launch_kind" \
        --session-id "${claude_session_id:-}" \
        ${tool_resume_target:+--resume "$tool_resume_target"} \
        --reasoning-effort "$reasoning_effort"
      ;;
    claude|cc|cc-use-codex-cli)
      [[ -f "$RUNTIME_ACP_PROMPT_CLIENT" ]] || {
        echo "[ERROR] missing ACP prompt client: $RUNTIME_ACP_PROMPT_CLIENT" >&2
        return 1
      }
      freely_apply_project_network_proxy_env "$project"
      local -a acp_args=(
        --bridge-socket "$bridge_socket"
        --cwd "$project"
        --prompt-file "$prompt_file"
        --mode "$mode"
        --model "$model"
        --launch-kind "$launch_kind"
        --reasoning-effort "$reasoning_effort"
      )
      # Session management based on launch kind
      case "$launch_kind" in
        resume)
          [[ -n "$tool_resume_target" ]] && acp_args+=(--resume "$tool_resume_target")
          ;;
        prompt)
          # Multi-turn delta: session alive, just send prompt.
          # Pass session_id as --resume; run-acp-prompt --launch-kind prompt
          # sets session_id from it and calls send_prompt() directly.
          [[ -n "$claude_session_id" ]] && acp_args+=(--resume "$claude_session_id")
          ;;
        fork)
          [[ -n "$tool_resume_target" ]] && acp_args+=(--resume "$tool_resume_target")
          ;;
        fresh|fresh_with_handoff)
          [[ -n "$claude_session_id" ]] && acp_args+=(--session-id "$claude_session_id")
          ;;
      esac
      exec python3 "$RUNTIME_ACP_PROMPT_CLIENT" "${acp_args[@]}"
      ;;
    opencode)
      [[ -f "$RUNTIME_ACP_PROMPT_CLIENT" ]] || {
        echo "[ERROR] missing ACP prompt client: $RUNTIME_ACP_PROMPT_CLIENT" >&2
        return 1
      }
      exec python3 "$RUNTIME_ACP_PROMPT_CLIENT" \
        --agent 'opencode acp' \
        --cwd "$project" \
        --prompt-file "$prompt_file" \
        --mode "$mode" \
        --model "$model" \
        --launch-kind "$launch_kind" \
        --reasoning-effort "$reasoning_effort"
      ;;
    *)
      echo "[ERROR] unsupported ACP launcher for tool: $tool" >&2
      return 1
      ;;
  esac
}

tool_run_from_prompt_file() {
  local project="$1"
  local tool="$2"
  local adapter="${3:-}"
  local model="${4:-}"
  local reasoning_effort="${5:-}"
  local mode="$6"
  local prompt_file="$7"
  local launch_kind="$8"
  local tool_capabilities="${9:-}"
  local tool_policy="${10:-}"
  local codex_capability_model="${11:-gpt-5.4}"
  local codex_capability_sandbox="${12:-workspace-write}"
  local codex_capability_approval_policy="${13:-never}"
  local codex_capability_cwd_mode="${14:-project-root}"
  local debug_log_file="${15:-}"
  local claude_session_id="${16:-}"
  local tool_resume_target="${17:-}"

  [[ -n "$adapter" ]] || adapter="$(tool_default_adapter "$tool")"
  if ! tool_adapter_is_supported "$tool" "$adapter"; then
    echo "[ERROR] unsupported adapter '$adapter' for tool '$tool' (supported: $(tool_supported_adapters "$tool" | tr '\n' ',' | sed 's/,$//'))" >&2
    return 1
  fi
  if ! tool_adapter_supports_launch_kind "$tool" "$adapter" "$launch_kind"; then
    echo "[ERROR] launch kind '$launch_kind' is not supported for tool '$tool' with adapter '$adapter' (supported: $(tool_supported_launch_kinds_for_adapter "$tool" "$adapter" | tr '\n' ',' | sed 's/,$//'))" >&2
    return 1
  fi

  case "$adapter" in
    direct)
      tool_run_direct_from_prompt_file "$project" "$tool" "$model" "$reasoning_effort" "$mode" "$prompt_file" "$launch_kind" "$tool_capabilities" "$tool_policy" "$codex_capability_model" "$codex_capability_sandbox" "$codex_capability_approval_policy" "$codex_capability_cwd_mode" "$debug_log_file" "$claude_session_id" "$tool_resume_target"
      ;;
    acp)
      tool_run_acp_from_prompt_file "$project" "$tool" "$model" "$reasoning_effort" "$mode" "$prompt_file" "$launch_kind" "$tool_capabilities" "$tool_policy" "$codex_capability_model" "$codex_capability_sandbox" "$codex_capability_approval_policy" "$codex_capability_cwd_mode" "$debug_log_file" "$claude_session_id" "$tool_resume_target"
      ;;
    *)
      echo "[ERROR] adapter '$adapter' is configured for tool '$tool' but has no runtime launcher implementation yet" >&2
      return 1
      ;;
  esac
}
