# Code Review — ACP Session Store (absorbed into chat-inbox-sqlite)

- review_id: `20260430-acp-session-store-verification`
- date: `2026-04-30`
- reviewer: `claude-opus-4.7`
- issue_path: `docs/epics/workspace-routing-foundation/chat-inbox-sqlite/issues/I-20260429-2040-A.md`

## decision

Replace cycle-log text parsing + tool directory scanning with session-store.py SQLite as the authoritative ACP session identity source. Absorb into I-20260429-2040-A since it reuses the same freely.db + CLI pattern.

## why_this

The current session ID extraction chain is broken: run-acp-prompt.py outputs annotated IDs like "uuid (resumed)", monitor-ai-acp.sh extracts without stripping annotations, and select_launch_kind falls back to scanning ~/.claude/projects/ with alphabetical sort. This causes a crash loop where a stale session is repeatedly resumed and fails. The SQLite approach provides a single authoritative source that always stores clean UUIDs and properly tracks session lifecycle (active/failed/completed).

## alternatives_considered

1. **Fix only the text parsing** (strip annotations from cycle log) — would fix the immediate bug but leaves the unreliable scanning fallback intact
2. **Bridge generation number** — adds complexity (new file, generation tracking) without benefit since run-acp-prompt.py already handles session/resume → session/new fallback
3. **JSON file per session** — simpler than SQLite but loses query capability needed for worker/supervisor scenarios
4. **SQLite in freely.db (chosen)** — reuses existing DB pattern from chat-inbox, provides structured queries for future multi-agent coordination

## boundary_non_goals

- Not modifying ACP bridge transport layer
- Not changing non-ACP tool adapters (codex, iflow, kiro-cli)
- Not adding bridge generation tracking (P1)
- Not implementing SSE/HTTP event streaming (not applicable to CLI-first)

## residual_risk

- `chat-inbox.db` → `freely.db` rename orphans existing unconsumed chat data; acceptable since pre-release
- `_stop_patterns` in stop_project_runtime has pre-existing ACP-specific patterns in universal path; follow-on work needed
- session-store.py discovery depends on `$(dirname "$0")` relative to monitor-ai-acp.sh; path must be preserved in install

## scope

session-store.py + run-acp-prompt.py + monitor-ai-acp.sh + freely select_launch_kind + ensure_freely_db auto-init

## follow-on: 2026-04-30 auto-init

Added `ensure_freely_db()` called from `start_project_runtime` so existing projects
auto-initialize freely.db on first start after upgrade. No manual re-init needed.

## verdict

PASS — all 7 success criteria verified, critical regression found and fixed, auto-init added

## follow-on: 2026-04-30 (2) self-healing cleanup

Added `_cleanup_stale_runtime_state()` — validates PID files on startup,
removes stale lock/socket/pid/marker artifacts whose owning process is dead.
Also auto-cleans polluted LAST_TOOL_SESSION_ID in session-state.env.

Industry pattern: nginx (PID file validation), PostgreSQL (crash recovery),
systemd (PIDFile= with automatic cleanup).

## follow-on: 2026-04-30 (3) extended self-heal for acp_bridge

Extended existing startup_self_heal mechanism (not a new function):
- `acp_bridge` role added to `runtime_pid_file_for_role`, `runtime_pid_valid_for_role`, and `startup_self_heal_clear_stale_pid_files_if_needed`
- `acp-bridge.sock` cleaned alongside stale bridge PID
- Cycle-specific failure markers removed on every startup
- Polluted `LAST_TOOL_SESSION_ID` auto-healed via `is_valid_uuid` check

## follow-on: 2026-04-30 (4) stale lock cleanup

Added stale `project-start.lock` cleanup in `startup_self_heal_machine_state_if_needed`.
Lock holder PID is validated; if dead, lock is removed regardless of runtime state.

## follow-on: 2026-04-30 (5) ACP bridge lazy restart

Fixed bridge process keepalive: lazy initialize, auto-restart on death,
restart race guard. Fresh 5s, resume 2s (cache hit).

## follow-on: 2026-04-30 (6) ACP resume evidence from session-store

## follow-on: 2026-04-30 (7) ACP no in-memory fallback

## follow-on: 2026-04-30 (8) ACP permission mode fix
Root cause: --permission-mode bypassPermissions requires --allow-dangerously-skip-permissions
to take effect on child claude process. Without it, Claude CLI silently falls back to default mode.
Fix: call session/set_mode bypassPermissions after session/new in bridge + run-acp-prompt.py direct mode.

## follow-on: 2026-04-30 (9) alias env inheritance fix
Moved _load_tool_launchers + _apply_tool_alias_settings before _bridge_ensure_running
so ACP bridge inherits correct per-alias model/env vars instead of shell environment.

## follow-on: 2026-04-30 (10) auth regex false positive fix
Root cause: issue ID dates (e.g. 20260429, 20260430) contain substrings
matching HTTP status codes (429). Old regex (401|402|403|429) matched
these, causing false auth_or_rate_limit detection.
Fix:  word boundaries so only standalone status codes match.
Verified: "I-20260429-2000-A" → no_match, "HTTP 429" → MATCH.

## follow-on: 2026-04-30 (11) bridge PID fix after fork

Root cause: start_server() wrote os.getpid() before fork, placing parent PID in file.
After parent exits, PID file has dead PID. stop sends SIGTERM to dead PID → no effect.
Fix: move PID write to after fork so file contains daemon child PID.

## follow-on: 2026-04-30 (12) auto-force clean start on restart storm

## follow-on: 2026-04-30 (13) stop cleanup + no attach to storm

stop: added last-resort pkill of all project processes after PID-file termination.
start: active_runtime_attach_reusable_for_project now checks restart storm count
and refuses to attach to a crashing supervisor, forcing a clean start.

## follow-on: 2026-04-30 (14) diagnostic logging improvements
- log_info/log_warn/log_error now include UTC timestamps
- _detect_acp_failure logs exact matched text (no more mystery triggers)
- ACP session_id extracted from cycle log line 1 (no more "unavailable")

## follow-on: 2026-04-30 (15) settle cleanup now removes worktrees
settle_retire_ready_merged_worker_runtime_state now executes git worktree
remove + git branch -d for merged worktrees instead of just clearing state
files. Enables self-governing closeout without dedicated worker processes.

## follow-on: 2026-04-30 (16) settle logging

## follow-on: 2026-04-30 (17) cleanup workers launchable for merged worktrees

## follow-on: 2026-04-30 (18) worker launch on delegate_workers not just rc=0

## follow-on: 2026-05-01 (19) stream-json prototype (dropped)
Prototype shelved: no cross-process cache hits with claude -p mode.
ACP confirmed 60% speed improvement via session/resume cache.

## follow-on: 2026-05-01 (20) worker launch from exit_contract CSV
Worker launch now reads WORKER_PROMPTS_CSV directly from exit_contract
(env format, 100% machine-readable) instead of parsing continuity markdown.

## follow-on: 2026-05-01 (21) worker launch inline docs
