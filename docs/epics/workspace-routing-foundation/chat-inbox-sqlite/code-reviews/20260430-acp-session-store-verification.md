# Code Review — ACP Session Store (absorbed into chat-inbox-sqlite)

- review_id: `20260430-acp-session-store-verification`
- date: `2026-04-30`
- reviewer: `claude-opus-4.7`
- issue: `I-20260429-2040-A`
- scope: `session-store.py + run-acp-prompt.py + monitor-ai-acp.sh + freely select_launch_kind`

## Verdict: PASS

## Implementation Decision Note

This hotfix replaces fragile cycle-log text parsing with a SQLite-backed session identity store (`session-store.py`), absorbed into the existing `freely.db` pattern introduced by I-20260429-2040-A.

### What changed

| Component | Change | Risk |
|---|---|---|
| `session-store.py` | New CLI for session CRUD in freely.db | Low — follows chat-inbox.py pattern |
| `run-acp-prompt.py` | Line 1 = clean UUID for machine parsing | Low — backward compatible (line 2 kept) |
| `monitor-ai-acp.sh` | Persists session via session-store.py | Low — fallback to existing behavior |
| `freely select_launch_kind` | ACP mode queries session-store | Low — fallback to in-memory vars |
| `freely.db` rename | chat-inbox.db → freely.db | Low — new file, old file orphaned (no migration, pre-release) |

### Self-review findings

1. **CRITICAL (fixed):** `--bridge-lost-marker-file` was initially passed unconditionally to all monitor scripts. Fixed: now conditionally passed via bash array only for ACP adapter.
2. **Pre-existing:** `_stop_patterns` in `stop_project_runtime` includes ACP-specific patterns in universal path. Not introduced by this change; follow-on work needed.
3. **Verified:** All 5 code paths in `run-acp-prompt.py` output clean UUID line 1 before annotated line 2.
4. **Verified:** Non-ACP paths (codex, iflow, kiro-cli) unaffected.

### Test evidence

See `docs/pre-brainstorms/20260430-0000--acp-session-store-and-lifecycle/pre-tests.md` — 6 test cases, all PASS.
