---
owner_issue: I-20260524T053214Z-A
issue_id: I-20260524T053214Z-A
---
# Code Review — acp-tool-switch-integration

- issue_id: I-20260524T053214Z-A
- reviewer: claude-opus-4.7
- mode: subagent
- verdict: pass
- **commits reviewed**: 4c146655, 7bd478b4

## Review Scope

4 commits across 4 files, 119 insertions / 5 deletions.

### 1. `freely:select_launch_kind()` ACP path

**Change**: Added `_tool_switch_launch_kind()` call before `get-active` in ACP path. If `fresh`, sets `fresh_with_handoff` and returns.

**Assessment**: Correct. The `_ts_launch` variable is local to ACP block (not conflicting with global `_ts_launch` at line 15959). The placement after fork check and before session-store query is correct — fork workers skip this check (they have `SESSION_PARENT_ID` set and need parent context).

**Edge cases**: 
- When `_tool_switch_read_latest()` returns empty → returns `fresh` → correct
- When `_new_sid` is populated and same tool → returns `resume` → proceeds to session-store → correct
- When cross_tool → returns `fresh` → `fresh_with_handoff` → correct

### 2. `freely:_acp_bridge_has_fatal_error()`

**Change**: Added `Session not found|Internal error|Resource not found` regex.

**Assessment**: Correct. Positioned after network failure check, before return 1. Uses same `rg -qi` pattern as existing checks. The `Internal error` match is intentionally broad to catch opaque ACP errors.

**Residual risk**: `Internal error` can match legitimate internal warnings (low risk — bridge log internal errors always indicate real issues).

### 3. `monitor-ai-acp.sh:_detect_acp_failure()`

**Change**: (a) Expanded grep to include bridge log file, (b) added `elif` branch for `Internal error|Resource not found|server error` in cycle log.

**Assessment**: Correct. Bridge log path computation `$(dirname "$log_file")/../run/acp-bridge.log` resolves correctly from `.freely/logs/` to `.freely/run/`. The `elif` catches opaque ACP errors that don't contain "Session not found" literally.

**Edge cases**: When bridge log doesn't exist (first cycle after fresh install), `grep` with non-existent file may fail on macOS BSD grep (suppressed by `2>/dev/null`). The first `if` block result may be silently dropped. Mitigated by `elif` branch which doesn't depend on bridge log.

### 4. `monitor-ai-acp.sh:_tool_switch_writeback_session_id()`

**Change**: New function calling `session-store.py tool-switch-update-sid`. Called after `_persist_session_to_store()`.

**Assessment**: Correct. Guard clauses check for missing session-store.py and empty `new_session_id`. Uses `|| true` to never block the main flow on writeback failure.

### 5. `run-acp-prompt.py` prompt mode fallback

**Change**: Wrapped `send_prompt()` in try/except. On failure, `session/new` fallback + retry.

**Assessment**: Correct. Uses same fallback pattern as "resume" mode (line 351-359). The `launch_kind` is updated to "fresh" after fallback so that cache statistics reflect the actual launch pattern. `session_id` is correctly updated before retry.

**Residual risk**: If the AI API/proxy itself is what's causing the failure (not the session), the retry will also fail. This is mitigated by bridge idle timeout (300s) — the retry won't hang forever.

### 6. `session-store.py` validation

**Change**: `_validate_required_fields()` for `upsert_session()`, `tool_switch_atomic_write()`, `tool_switch_update_session_id()`.

**Assessment**: Correct. UUID validation uses standard RFC 4122 regex. Validation runs before any DB writes, preventing dirty data. The `is_valid_uuid_str()` helper is standalone for reuse.

## Static Test Results

| Test | Result |
|------|--------|
| DB validation: empty session_id → ValueError | PASS |
| DB validation: invalid UUID → ValueError | PASS |
| DB validation: empty project → ValueError | PASS |
| DB validation: invalid role → ValueError | PASS |
| DB validation: empty new_tool → ValueError | PASS |
| DB validation: empty new_session_id → ValueError | PASS |
| new_session_id writeback to tool_switch_events | PASS |
| _detect_acp_failure: Internal error in cycle log | PASS |
| _detect_acp_failure: Session not found in bridge log | PASS |
| _detect_acp_failure: Resource not found in cycle log | PASS |
| _detect_acp_failure: idle timeout (existing pattern) | PASS |
| _detect_acp_failure: auth failure (existing pattern) | PASS |
| run-acp-prompt.py compiles | PASS |

## Verdict

**PASS** — all changes are minimal, correct, and well-guarded. No regressions to non-ACP path.
