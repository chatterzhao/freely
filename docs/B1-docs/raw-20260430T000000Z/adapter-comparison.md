# Adapter Comparison: Direct vs ACP vs Stream-JSON

## 测试条件

- Model: `deepseek-v4-flash`
- API: DeepSeek Anthropic-compatible endpoint (`/anthropic/v1/messages`)
- Machine: macOS, Claude CLI v2.1.123

## 缓存验证方法

### Anthropic 兼容端点
```bash
# 发两次相同请求，检查 usage.cache_read_input_tokens
curl ... /anthropic/v1/messages -d '{"model":"deepseek-v4-flash","messages":[...]}'
# → usage.cache_read_input_tokens > 0 → 缓存命中 ✅
```
确认命中：2048/2145 tokens (95%)

### DeepSeek 原生端点
```bash
curl ... /v1/chat/completions -d '{"model":"deepseek-chat","messages":[...]}'
# → usage.prompt_cache_hit_tokens > 0 → 缓存命中 ✅
```
确认命中：2048/2145 tokens (95%)

## 三种适配器对比

| | Direct (`claude -p`) | ACP (bridge) | Stream-JSON (新) |
|---|---|---|---|
| **启动命令** | `claude -p < prompt.txt` | `claude-agent-acp → bridge → claude` | `claude -p --output-format stream-json --input-format stream-json` |
| **Fresh 首次响应** | ~5s (小) / >60s (大) | ~5s (session/new) | ~3-5s (小) / TBD (大) |
| **Resume 恢复** | `--resume <uuid>` | `session/resume <session_id>` | `--resume <uuid>` |
| **Resume 速度** | ~5s (无效缓存) | **~2s (60% faster)** ✅ | TBD |
| **跨进程缓存** | ❌ 每次新 system prompt | ✅ session 上下文一致 | ❌ 每次新进程 |
| **Session 持久** | 磁盘 (~/.claude/sessions/) | bridge 内存 (+ session-store) | 磁盘 + session-store |
| **依赖** | 无 | claude-agent-acp (npm) | 无 |
| **Hook leak** | 无 | ⚠️ v0.31.4 已知问题 | 无 |
| **工具执行** | Claude 内部 | claude-agent-acp → Claude | Claude 内部 |
| **大 prompt** | ⚠️ >30KB 可能失败 (0B输出) | ✅ 正常工作 | TBD |
| **复杂度** | 最低 | 高 (bridge + agent) | 中等 |

## 缓存命中深度分析

### 为什么 ACP 的 Resume 快？

```
Direct -p (每次新进程):
  Claude 生成 system prompt A → API request A → 无缓存
  Claude 生成 system prompt B → API request B → 无缓存 (A≠B)
  
ACP session/resume:
  session/new → system prompt X → API request X → 创建缓存
  session/resume → system prompt X → API request X → 缓存命中! (X=X)
```

关键：ACP 的 `session/resume` 保持了相同的会话上下文，API 请求的 system prompt 前缀相同 → 缓存命中。每次新 `-p` 进程生成不同的 system prompt → 无法命中。

### 缓存命中条件

1. **相同 model** (`deepseek-v4-flash`) ✅
2. **相同 system prompt 前缀** — ACP 满足，direct 不满足 ❌
3. **相同 user prompt 前缀** ✅ (freely prompt 固定)
4. **TTL 内** (几小时到几天) ✅

## 关键发现

### `--exclude-dynamic-system-prompt-sections` 标志

Claude CLI v2.1.123 提供了此标志，将动态内容（cwd, env info, memory paths, git status）从 system prompt 移到首条 user message。**这使 system prompt 静态化，理论上可以跨进程缓存命中。**

实测结果：
- 用 `--exclude-dynamic`：claude -p 正常输出（6019B）
- 不用 `--exclude-dynamic`：claude -p 失败（0B）
- 但跨进程缓存**未观察到显著加速**（24s → 24s）

原因分析：即使移除了动态部分，system prompt 中仍包含 tool definitions、model info 等内容，这些在不同 `-p` 调用间可能有细微差异，导致 API 缓存未命中。

### 为什么 ACP 缓存成功而 direct/stream-json 不行

```
ACP session/resume:
  claude-agent-acp 保持进程存活 → system prompt 生成一次
  → 所有 session/prompt 请求共享同一 system prompt
  → DeepSeek API 缓存命中 ✅

Direct -p / Stream-JSON:
  每次新进程 → Claude 重新生成 system prompt
  → 即使内容相同，可能有细微差异（时间戳等）
  → DeepSeek API 缓存未命中 ❌
```

## 推荐

| 场景 | 推荐适配器 | 原因 |
|---|---|---|
| 生产环境 | ACP | 缓存命中 60% 速度提升，session 持久 |
| 开发/测试 | Stream-JSON | 无 npm 依赖，简单可靠 |
| 单次任务 | Direct | 最简单，无状态 |
| 未来方向 | Stream-JSON | 去掉 claude-agent-acp，配 session-store 实现 session 持久后可达到 ACP 级缓存 |

## 测试用例

### TC1: 验证 API 缓存 (Anthropic 端点)
```bash
PROMPT=$(python3 -c "import json; print(json.dumps(open('prompt.txt').read()))")
# Cold
curl ... /anthropic/v1/messages -d '{"model":"deepseek-v4-flash","messages":[...]}' | jq .usage.cache_read_input_tokens
# → 0 或不存在
# Warm (10s 后)
curl ... /anthropic/v1/messages -d '{"model":"deepseek-v4-flash","messages":[...]}' | jq .usage.cache_read_input_tokens
# → >0 → 缓存命中 ✅
```

### TC2: ACP Resume 缓存
```bash
# Fresh
SID=$(run-acp-prompt.py --agent claude-agent-acp --launch-kind fresh ... | head -1)
# Resume
run-acp-prompt.py --agent claude-agent-acp --launch-kind resume --resume "$SID" ...
# 预期: resume 比 fresh 快 50%+
```

### TC3: Direct --resume UUID 
```bash
SID=$(uuidgen)
# Fresh
claude -p --session-id "$SID" < prompt.txt
# Resume  
claude -p --resume "$SID" < prompt.txt
# 预期: 时间相近 (无跨进程缓存)
```
