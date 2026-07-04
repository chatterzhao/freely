#!/usr/bin/env bash
# session-cache.sh — unified session/cache management across AI tools.
#
# Each AI tool has different session storage, fork mechanism, and resume args.
# This module abstracts those differences behind a uniform interface.
#
# Usage: source this file, then call the functions.
#   session_dir_for_tool <tool> <project>          → session directory path
#   session_fork_args <tool> <parent_id> <child_id> → CLI args for fork
#   session_resume_args <tool> <target_id>          → CLI args for resume
#   session_fresh_args <tool> <new_id>              → CLI args for fresh
#   session_find_recent <tool> <project>            → most recent session ID
#   session_has_evidence <tool> <project> <id>      → 0 if JSONL exists
#
# Tool support matrix:
#   claude:  --session-id, --resume, --fork-session
#   codex:   exec, exec resume <id>
#   opencode: --session, --fork, --continue
#   fallback: --session-id, no native fork (prepend JSONL content to prompt)

# ── Tool→directory mapping ────────────────────────────────

session_dir_for_tool() {
  local resolved_tool="$1" project="$2"
  case "$resolved_tool" in
    claude|cc|cc-use-codex-cli)
      local slug; slug=$(printf '%s' "$project" | sed 's|/|-|g')
      printf '%s\n' "${HOME}/.claude/projects/${slug}"
      ;;
    codex)
      printf '%s\n' "${CODEX_HOME:-$HOME/.codex}/sessions"
      ;;
    opencode)
      printf '%s\n' "${HOME}/.opencode/sessions"
      ;;
    *) return 1 ;;
  esac
}

# ── Launch args per tool per strategy ──────────────────────

session_fork_args() {
  local resolved_tool="$1" parent_id="$2" child_id="$3"
  case "$resolved_tool" in
    claude|cc|cc-use-codex-cli)
      printf '%s\n' "--resume" "$parent_id" "--fork-session" "--session-id" "$child_id"
      ;;
    codex)
      # Codex: resume parent, then fork as new (no single-command fork)
      printf '%s\n' "exec" "resume" "$parent_id"
      # After this launch, the new session ID is returned in JSON; caller must capture.
      ;;
    opencode)
      printf '%s\n' "--session" "$parent_id" "--fork"
      ;;
    *)
      # Fallback: no native fork. Caller should prepend parent JSONL to prompt.
      printf '%s\n' "--session-id" "$child_id"
      return 2  # signals "no native fork, use fallback"
      ;;
  esac
}

session_resume_args() {
  local resolved_tool="$1" target_id="$2"
  case "$resolved_tool" in
    claude|cc|cc-use-codex-cli)
      printf '%s\n' "--resume" "$target_id"
      ;;
    codex)
      printf '%s\n' "exec" "resume" "$target_id"
      ;;
    opencode)
      printf '%s\n' "--session" "$target_id" "--continue"
      ;;
    *)
      printf '%s\n' "--resume" "$target_id"
      ;;
  esac
}

session_fresh_args() {
  local resolved_tool="$1" new_id="$2"
  case "$resolved_tool" in
    claude|cc|cc-use-codex-cli)
      printf '%s\n' "--session-id" "$new_id"
      ;;
    codex)
      printf '%s\n' "exec"
      ;;
    opencode)
      printf '%s\n' "--session" "$new_id"
      ;;
    *)
      printf '%s\n' "--session-id" "$new_id"
      ;;
  esac
}

# ── Session discovery ──────────────────────────────────────

session_find_recent() {
  local resolved_tool="$1" project="$2"
  local session_dir; session_dir=$(session_dir_for_tool "$resolved_tool" "$project" 2>/dev/null || true)
  [[ -n "$session_dir" && -d "$session_dir" ]] || return 1

  local latest; latest=$(find "$session_dir" -name "*.jsonl" -type f 2>/dev/null | sort | tail -1)
  [[ -n "$latest" && -f "$latest" ]] || return 1

  local sid; sid=$(basename "$latest" .jsonl)
  [[ -n "$sid" ]] || return 1
  printf '%s\n' "$sid"
}

session_has_evidence() {
  local resolved_tool="$1" project="$2" session_id="$3"
  local session_dir; session_dir=$(session_dir_for_tool "$resolved_tool" "$project" 2>/dev/null || true)
  [[ -n "$session_dir" && -d "$session_dir" ]] || return 1
  [[ -f "$session_dir/${session_id}.jsonl" ]]
}

# ── Fallback: prepend parent JSONL context to prompt ────────
# For tools without native fork. Reads parent session JSONL,
# extracts conversation as text, prepends to prompt file.

session_fork_fallback_prepend() {
  local resolved_tool="$1" parent_id="$2" prompt_file="$3"
  local session_dir project_dir
  # We don't have project here; use the global session dir approach
  case "$resolved_tool" in
    claude|cc|cc-use-codex-cli|codex)
      return 1  # these tools have native fork, no fallback needed
      ;;
  esac
  # For tools without native session storage, we can't prepend.
  return 1
}

# ── Session ID extraction from tool output ──────────────────

session_extract_id_from_log() {
  local resolved_tool="$1" log_file="$2"
  case "$resolved_tool" in
    claude|cc|cc-use-codex-cli)
      local debug_log="${log_file%.log}.debug.log"
      local sid
      sid=$(sed -n 's/.*session[._]id[=:]\s*\([a-f0-9]\{8\}-[a-f0-9]\{4\}-[a-f0-9]\{4\}-[a-f0-9]\{4\}-[a-f0-9]\{12\}\).*/\1/p' "$debug_log" 2>/dev/null | head -n 1)
      if [[ -z "$sid" ]]; then
        sid=$(sed -n 's/.*session[._]id[=:]\s*\([a-f0-9]\{8\}-[a-f0-9]\{4\}-[a-f0-9]\{4\}-[a-f0-9]\{4\}-[a-f0-9]\{12\}\).*/\1/p' "$log_file" 2>/dev/null | head -n 1)
      fi
      printf '%s\n' "$sid"
      ;;
    codex)
      sed -n 's/^session id: //p' "$log_file" 2>/dev/null | head -n 1
      ;;
    opencode)
      sed -n 's/.*service=session id=\(ses_[A-Za-z0-9_]*\).*/\1/p' "$log_file" 2>/dev/null | head -n 1
      ;;
    *) ;;
  esac
}

# ── Strategy: decide launch kind based on current state ─────
# Returns: launch_kind=<fresh|resume|fork> resume_target=<id> session_id=<id>
# Caller sets TOOL_SESSION_ID_CURRENT and SESSION_PARENT_ID based on output.

session_strategy_decide() {
  local project="$1" tool="$2"
  local resolved_tool; resolved_tool="$(_resolve_tool_family "$tool")"
  local session_id="${TOOL_SESSION_ID_CURRENT:-}"
  local parent_id="${SESSION_PARENT_ID:-}"

  # 1. Fork: parent ID set, no own session → new worker forking from parent
  if [[ -n "$parent_id" && -z "$session_id" ]]; then
    session_id="$(generate_uuid_for_runtime)"
    printf 'launch_kind=fork\n'
    printf 'session_id=%s\n' "$session_id"
    printf 'resume_target=%s\n' "$parent_id"
    return 0
  fi

  # 2. Resume: own session ID exists and has evidence
  if [[ -n "$session_id" ]]; then
    if session_has_evidence "$resolved_tool" "$project" "$session_id"; then
      printf 'launch_kind=resume\n'
      printf 'session_id=%s\n' "$session_id"
      printf 'resume_target=%s\n' "$session_id"
      return 0
    fi
    # Session ID exists but no evidence → enforcement applies
    if [[ "${AI_RESUME_ON_RESTART:-false}" == "true" ]]; then
      echo "[ERROR] session $session_id has no JSONL evidence" >&2
      return 1
    fi
  fi

  # 3. JSONL fallback: no session ID but tool dir has sessions
  local fallback_id; fallback_id=$(session_find_recent "$resolved_tool" "$project" 2>/dev/null || true)
  if [[ -n "$fallback_id" ]]; then
    printf 'launch_kind=resume\n'
    printf 'session_id=%s\n' "$fallback_id"
    printf 'resume_target=%s\n' "$fallback_id"
    return 0
  fi

  # 4. Fresh: nothing to resume, first-ever launch
  local new_id; new_id=$(generate_uuid_for_runtime)
  printf 'launch_kind=fresh\n'
  printf 'session_id=%s\n' "$new_id"
  printf 'resume_target=%s\n' "$new_id"
  return 0
}
