# Pre-tests — 20260430-0000--acp-session-store-and-lifecycle

Hotfix absorbed into chat-inbox-sqlite (I-20260429-2040-A).

## 关键检查方法

### 检查 1: 模型配置是否正确传递到子 claude 进程

**检查目标**: 确认 alias 的 settings_deepseek_flash.json 被 bridge 消费，
而不是被 shell 环境的 ANTHROPIC_MODEL 污染。

**步骤**:
```bash
# 1. 模拟 monitor-ai-acp.sh 的流程
source docs/system/workspace/scripts/runtime/tool-launchers.sh
_apply_tool_alias_settings "cc-ds-flash-auto"
echo "ANTHROPIC_MODEL=$ANTHROPIC_MODEL"  # 应该是 deepseek-v4-flash[1m]

# 2. 启动 bridge
python3 acp-bridge.py start --project $PWD

# 3. 查询 session/new 返回的模型列表
python3 -c "
import socket, json
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect('.freely/run/acp-bridge.sock')
sock.settimeout(15)
f = sock.makefile('r')
# initialize
sock.sendall(json.dumps({'jsonrpc':'2.0','id':1,'method':'initialize',
  'params':{'protocolVersion':1,'clientInfo':{'name':'t','title':'t','version':'1.0'},
  'clientCapabilities':{}}}).encode()+b'\n')
f.readline()
# session/new
sock.sendall(json.dumps({'jsonrpc':'2.0','id':2,'method':'session/new',
  'params':{'cwd':'.','mcpServers':[]}}).encode()+b'\n')
for i in range(10):
    m = json.loads(f.readline())
    if m.get('id')==2 and 'result' in m:
        mods = m['result']['models']
        print(f'currentModelId: {mods[\"currentModelId\"]}')
        for mod in mods['availableModels']:
            print(f'  {mod[\"modelId\"]} → {mod[\"name\"]}')
        break
sock.close()
"
```

**判定标准**:
- ✅ `ANTHROPIC_MODEL=deepseek-v4-flash[1m]` (apply 后)
- ✅ session/new 的 availableModels 中 sonnet/opus/haiku 都指向 `deepseek-v4-flash[1m]`
- ❌ 如果 sonnet/opus 指向 `deepseek-v4-pro[1m]` → 环境变量污染

### 检查 2: 权限模式是否正确设置

**检查目标**: 确认 bridge 在 session/new 后调用了 session/set_mode bypassPermissions。

**步骤**:
```bash
grep "set_mode\|bypassPermissions" .freely/run/acp-bridge.log
```

**判定标准**:
- ✅ 日志中有 `"session <sid>... mode set to bypassPermissions"`
- ✅ 子 claude 进程命令行包含 `--allow-dangerously-skip-permissions`
- ❌ 如果有 `request_permission` → 权限未 bypass

### 检查 3: 子 claude 进程完整命令行验证

**步骤**:
```bash
ps aux | grep "claude.*session-id" | grep -v grep
```

**判定标准**:
- 检查 `--output-format stream-json --input-format stream-json` (ACP 协议)
- 检查 `--allow-dangerously-skip-permissions` (权限跳过)
- 不应有 `--model` 显式指定 (模型由 settings/env 决定)

---

## Test 1: session-store.py CLI round-trip

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

## 2026-04-30 (4): Stop/Start lifecycle + multi-worker stability

### Test J: Stop kills ALL project processes
```bash
# 1. Start daemon
freely daemon start --project $PWD
# 2. Stop
freely daemon stop --project $PWD
sleep 3
# 3. Verify no residue
ps aux | grep -E "freely|acp-bridge|claude-agent|watchdog|daemon-run" | grep -v grep | grep -v memark
# Expected: 0 processes (除了 memark 外部工具)
```

### Test K: Daemon start rejects crash-loop supervisor
```bash
# 1. Create restart storm state
echo 'LAST_RESTART_STORM_COUNT="5"' >> .freely/run/session-state.env
# 2. Start daemon
freely daemon start --project $PWD
# 3. Verify: should either force clean start or reject with clear error
# 4. Check daemon log for "refusing to attach" or "forcing clean daemon start"
```

### Test L: Multi-worker recovery doesn't crash supervisor
```bash
# 1. Create 2 valid test worker prompts in .freely/run/worker-prompts/
# 2. Start daemon
# 3. Monitor supervisor PID for 2 minutes
prev=$(cat .freely/run/supervisor.pid)
for i in $(seq 1 8); do
  sleep 15
  cur=$(cat .freely/run/supervisor.pid || echo dead)
  [[ "$cur" != "$prev" ]] && echo "RESTART" && break
done
echo "stable: $([[ "$cur" == "$prev" ]] && echo YES || echo NO)"
# Expected: supervisor stays alive, workers processed or skipped
```

### Test M: Supervisor completes full cycle after fixes
```bash
# 1. Start daemon (clean state)
# 2. Wait 2 minutes
# 3. Verify: ai_cycle_finished event with rc=0, no auth_or_rate_limit
grep "ai_cycle_finished" .freely/logs/runtime-events.log | tail -1
# Expected: rc=0, exit_reason=ai_exit_rc_ (not auth_or_rate_limit)
```
