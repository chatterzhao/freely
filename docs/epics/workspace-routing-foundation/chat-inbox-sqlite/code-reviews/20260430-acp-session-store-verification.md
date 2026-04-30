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

session-store.py + run-acp-prompt.py + monitor-ai-acp.sh + freely select_launch_kind

## verdict

PASS — all 7 success criteria verified, critical regression found and fixed
