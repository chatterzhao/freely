# Pre-tests — 20260430-0000--acp-session-store-and-lifecycle

Hotfix absorbed into chat-inbox-sqlite (I-20260429-2040-A). Tests executed:

## Test 1: session-store.py CLI round-trip
- `python3 session-store.py init --db /tmp/test-freely.db`
- `python3 session-store.py upsert --db ... --session-id $(uuidgen) --project /tmp/test --tool cc --launch-kind fresh --tool-adapter acp --role manager`
- `python3 session-store.py get-active --db ... --project /tmp/test --role manager` → returns clean UUID
- `python3 session-store.py complete --db ... --session-id <uuid> --status failed --error-reason auth_or_rate_limit`
- `python3 session-store.py get-active ...` → returns empty (failed sessions excluded)
- PASS

## Test 2: run-acp-prompt.py stdout format
- Verified all 5 code paths print `print(session_id)` as line 1 before annotated line 2
- PASS

## Test 3: monitor-ai-acp.sh session persistence
- `_persist_session_to_store` reads clean UUID from line 1, calls session-store.py upsert
- `_mark_session_failed` marks failed with error reason
- `_mark_session_completed` marks completed
- `_detect_acp_failure` now has 3 categories (auth, network, bridge_lost)
- PASS

## Test 4: select_launch_kind ACP mode
- No more cycle log text parsing
- No more `_find_recent_session_from_tool_dir` in ACP path
- Uses `session-store.py get-active` as authoritative source
- Falls back to in-memory CLAUDE_SESSION_ID_CURRENT if session-store unavailable
- PASS (code review)

## Test 5: Non-ACP regression guard
- `--bridge-lost-marker-file` only passed when adapter is `acp` (guarded by `_adapter_extra_args` array)
- `ensure_runtime_tool_session_anchor` keeps original `_find_recent_session_from_tool_dir` for non-ACP
- `extract_tool_session_id_from_log` ACP branch removed, codex branch kept
- PASS (code review)

## Test 6: freely.db rename
- All `chat-inbox.db` references renamed to `freely.db`
- `chat-inbox.py` and `session-store.py` both use the same DB
- `freely init` calls both `init` commands (idempotent via IF NOT EXISTS)
- PASS (code review)

## 2026-04-30 (2): ACP bridge + session evidence tests

### Test A: ACP bridge lazy restart
```bash
# Start bridge, wait for idle, send request
python3 acp-bridge.py start --project $PWD
sleep 30  # let claude-agent-acp idle
python3 run-acp-prompt.py --bridge-socket .freely/run/acp-bridge.sock \
  --cwd $PWD --prompt-file /tmp/prompt.txt --launch-kind fresh --mode auto
# Expected: completes in <10s, bridge auto-restarts if process died
```

### Test B: Fresh vs resume speed comparison
```bash
# Fresh: ~5s
python3 run-acp-prompt.py --bridge-socket ... --launch-kind fresh --mode auto | head -1
# Resume: ~2s (cache hit)
python3 run-acp-prompt.py --bridge-socket ... --launch-kind resume --resume $SID --mode auto
```

### Test C: Bridge auto-restart after claude-agent-acp death
```bash
# Verify bridge log shows "server process restarted" after stdout close
grep "restart\|stdout closed" .freely/run/acp-bridge.log
```

### Test D: Session-store evidence in ACP mode
```bash
# Verify session-store.py get-active returns clean UUID
# Verify AI_RESUME_ON_START=true works with session-store evidence (not JSONL)
python3 session-store.py get-active --db .freely/freely.db --project $PWD
```

### Test E: Non-ACP regression (codex path untouched)
```bash
# Verify --bridge-lost-marker-file only passed for acp adapter
# Verify extract_tool_session_id_from_log ACP branch removed
# Verify ensure_runtime_tool_session_anchor non-ACP uses _find_recent_session_from_tool_dir
```

## 2026-04-30 (3): DeepSeek API speed diagnosis

### Test F: Baseline speed tests
```bash
# Simple English prompt (baseline)
echo "say hello world" | claude -p --settings ~/.claude/settings_deepseek_flash.json --dangerously-skip-permissions
# Expected: < 10s

# Simple Chinese prompt
echo "你好" | claude -p --settings ~/.claude/settings_deepseek_flash.json --dangerously-skip-permissions
# Expected: < 10s

# 1KB freely prompt
head -c 1000 .freely/run/prompt-*.txt | claude -p --settings ~/.claude/settings_deepseek_flash.json --dangerously-skip-permissions
# Expected: ~40s (Claude CLI overhead 3-4x vs direct API)
```

### Test G: Proxy elimination test
```bash
# Check for proxy
env | grep -i proxy

# Test without proxy
env -u all_proxy -u http_proxy -u https_proxy \
  claude -p --settings ~/.claude/settings_deepseek_flash.json --dangerously-skip-permissions < prompt.txt
```

### Test H: Direct API speed (bypass Claude CLI)
```bash
# Direct DeepSeek API call — establishes baseline
curl -s -w "TIME=%{time_total}s HTTP=%{http_code}" --max-time 60 \
  https://api.deepseek.com/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DEEPSEEK_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"model":"deepseek-v4-flash","max_tokens":1000,"messages":[{"role":"user","content":"<prompt>"}]}'
# Expected: ~13s for 34KB prompt (no Claude CLI overhead)
```

### Test I: Claude CLI overhead measurement
```bash
# Same prompt, compare direct API vs Claude CLI
# Direct API: ~13s
# Claude CLI:  ~50s (3-4x overhead)
# Claude CLI is reading config, loading model list, etc.
```

### Key finding
- DeepSeek API is NOT slow (~13s for 34KB)
- Claude CLI adds 3-4x overhead (~50s)
- Supervisors must not kill AI during active output — timeout should reset on each output event
