#!/usr/bin/env bash

sanitize_claude_project_key() {
  local project_root="$1"
  printf '%s\n' "${project_root//\//-}"
}

claude_projects_root() {
  printf '%s\n' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects"
}

project_root_variants() {
  local project_root="$1"
  local physical=""
  printf '%s\n' "$project_root"
  if [[ -d "$project_root" ]]; then
    physical="$(cd "$project_root" && pwd -P)"
    if [[ -n "$physical" && "$physical" != "$project_root" ]]; then
      printf '%s\n' "$physical"
    fi
  fi
}

find_claude_jsonl_path_for_session() {
  local project_root="$1" claude_session_id="$2"
  local projects_root project_key candidate variant fallback_candidate
  [[ -n "$project_root" && -n "$claude_session_id" ]] || return 0
  projects_root="$(claude_projects_root)"
  while IFS= read -r variant; do
    [[ -n "$variant" ]] || continue
    project_key="$(sanitize_claude_project_key "$variant")"
    candidate="$projects_root/$project_key/$claude_session_id.jsonl"
    if [[ -f "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done <<<"$(project_root_variants "$project_root")"

  while IFS= read -r fallback_candidate; do
    [[ -n "$fallback_candidate" ]] || continue
    if claude_jsonl_matches_project_root "$fallback_candidate" "$project_root"; then
      printf '%s\n' "$fallback_candidate"
      return 0
    fi
  done <<<"$(find "$projects_root" -type f -name "${claude_session_id}.jsonl" 2>/dev/null | sort)"
}

claude_jsonl_matches_project_root() {
  local claude_jsonl_path="$1" project_root="$2"
  [[ -f "$claude_jsonl_path" && -n "$project_root" ]] || return 1

  if command -v python3 >/dev/null 2>&1; then
    python3 - "$claude_jsonl_path" "$project_root" <<'PY'
import json
import os
import sys

jsonl_path = sys.argv[1]
project_root = sys.argv[2]
variants = {project_root}
try:
    variants.add(os.path.realpath(project_root))
except Exception:
    pass

matched = False
with open(jsonl_path, "r", encoding="utf-8") as fh:
    for raw in fh:
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        cwd = obj.get("cwd")
        if not cwd:
            continue
        cwd_variants = {cwd}
        try:
            cwd_variants.add(os.path.realpath(cwd))
        except Exception:
            pass
        if variants & cwd_variants:
            matched = True
            break
sys.exit(0 if matched else 1)
PY
    return $?
  fi

  local candidate_cwd
  candidate_cwd="$(rg -o '"cwd":"[^"]+"' "$claude_jsonl_path" | sed 's/.*"cwd":"//; s/"$//' | head -n 1)"
  [[ -n "$candidate_cwd" ]] || return 1
  [[ "$candidate_cwd" == "$project_root" ]] && return 0
  [[ -d "$candidate_cwd" && -d "$project_root" && "$(cd "$candidate_cwd" && pwd -P)" == "$(cd "$project_root" && pwd -P)" ]]
}

extract_latest_codex_thread_id_from_claude_jsonl() {
  local claude_jsonl_path="$1"
  [[ -f "$claude_jsonl_path" ]] || return 0

  if command -v python3 >/dev/null 2>&1; then
    python3 - "$claude_jsonl_path" <<'PY'
import json
import sys

path = sys.argv[1]
last = ""
with open(path, "r", encoding="utf-8") as fh:
    for raw in fh:
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        mcp_meta = obj.get("mcpMeta") or {}
        structured = mcp_meta.get("structuredContent") or {}
        thread_id = structured.get("threadId")
        if thread_id:
            last = thread_id
            continue
        tool_result = obj.get("toolUseResult")
        if isinstance(tool_result, dict):
            thread_id = tool_result.get("threadId")
            if thread_id:
                last = thread_id
                continue
        if isinstance(tool_result, str) and '"threadId"' in tool_result:
            try:
                parsed = json.loads(tool_result)
            except Exception:
                parsed = None
            if isinstance(parsed, dict) and parsed.get("threadId"):
                last = parsed["threadId"]
if last:
    print(last)
PY
    return 0
  fi

  rg -o '"threadId":"[^"]+"' "$claude_jsonl_path" | sed 's/.*"threadId":"//; s/"$//' | tail -n 1
}

find_codex_jsonl_path_for_thread() {
  local thread_id="$1"
  local sessions_root
  [[ -n "$thread_id" ]] || return 0
  sessions_root="${CODEX_HOME:-$HOME/.codex}/sessions"
  [[ -d "$sessions_root" ]] || return 0
  find "$sessions_root" -type f -name "*${thread_id}.jsonl" | sort | tail -n 1
}

resolve_cc_session_evidence() {
  local project_root="$1" claude_session_id="$2"
  local claude_jsonl_path codex_thread_id codex_jsonl_path codex_mcp_used

  claude_jsonl_path="$(find_claude_jsonl_path_for_session "$project_root" "$claude_session_id")"
  codex_thread_id=""
  codex_jsonl_path=""
  codex_mcp_used="0"

  if [[ -n "$claude_jsonl_path" ]]; then
    codex_thread_id="$(extract_latest_codex_thread_id_from_claude_jsonl "$claude_jsonl_path")"
    if [[ -n "$codex_thread_id" ]]; then
      codex_mcp_used="1"
      codex_jsonl_path="$(find_codex_jsonl_path_for_thread "$codex_thread_id")"
    fi
  fi

  cat <<EOF
CLAUDE_JSONL_PATH="${claude_jsonl_path:-}"
CODEX_MCP_USED="$codex_mcp_used"
CODEX_MCP_THREAD_ID="${codex_thread_id:-}"
CODEX_MCP_JSONL_PATH="${codex_jsonl_path:-}"
EOF
}
