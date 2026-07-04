---
b1_id: B1-20260704T004227Z
phase_state: completed
source_raw: raw-20260704T004227Z
source_url: https://github.com/chatterzhao/freely/issues/3722
produced_candidate: C-20260704T004227Z-A
created_at: 2026-07-04
---

# B1_IBM: agent-table slot 解析 — ACP binary 启动错误 + 环境变量污染

## Input

- **来源**: raw-20260704T004227Z (GitHub #3722, Gitee IJYPWD)
- **类型**: fix — agent-table.toml 配置的 slot 与实际执行不一致
- **严重程度**: 高 — 使用了错误的 ACP binary (claude-agent-acp) + 错误的模型 (deepseek-v4-pro)

## Problem

agent-table.toml 配置使用 `opencode-apikey-ds-flash-auto`，但实际推理全部走 `claude-agent-acp` + `deepseek-v4-pro` 模型。

### 根因：两个独立 Bug 叠加

#### Bug 1: monitor-ai-acp.sh 启动 bridge 时未传 `--acp-bin`

**两个独立的 Bridge 启动路径存在，且不一致：**

| 启动者 | 位置 | 传 `--acp-bin`? | 默认 binary |
|--------|------|:---:|------|
| `_ensure_acp_bridge_running()` in freely | line 14175 | ✅ 传 | 从 tool-registry 正确解析 |
| `_bridge_ensure_running()` in monitor-ai-acp.sh | line 152 | ❌ **不传** | `claude-agent-acp` (硬编码) |

**monitor-ai-acp.sh line 152:**
```bash
python3 "$bridge_script" start --project "$project" >/dev/null 2>&1 || {
```
**缺少 `--acp-bin "$acp_bin"`**，bridge 默认使用 `claude-agent-acp`。

**monitor-ai-acp.sh 的设计注释 (line 8) 暴露了硬编码假设：**
```
#   freely → monitor-ai-acp.sh → tool-launchers.sh → run-acp-prompt.py → acp-bridge → claude-agent-acp
```

**"→ claude-agent-acp"** — 架构文档里直接写死了 claude！

#### Bug 1 为何不被 `_ensure_acp_bridge_running` 检测到

monitor-ai-acp.sh 的 `_bridge_ensure_running` 会：
1. 写入 `.tool` 文件 = `opencode-apikey-ds-flash-auto` ✅ (line 168)
2. **不写入 `.bin` 文件** ❌ (没有这个逻辑)

freely 的 `_ensure_acp_bridge_running` 后来检查 (line 14070-14094)：
1. `running_bin=$(cat ".bin")` → **空**（monitor-ai-acp.sh 没写）→ 跳过 binary 比较
2. `running_tool=$(cat ".tool")` → `opencode-apikey-ds-flash-auto` → **匹配** → 跳过 tool 比较
3. `_acp_bridge_health_check` → **通过**（claude-agent-acp 也响应健康检查）
4. → **不重启 bridge**，claude-agent-acp 继续运行

**Bridge 实际运行 claude-agent-acp，但所有检查都认为它是 opencode！**

#### Bug 2: 环境变量污染 (Claude Code 对话 → freely daemon)

```
Claude Code 当前对话
  → ANTHROPIC_MODEL=deepseek-v4-pro[1m]
  → ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
  → ANTHROPIC_AUTH_TOKEN=sk-...
  → AI_AGENT=claude-code_2-1-199_agent
  → CLAUDE_CODE_ENTRYPOINT=cli
  → CLAUDE_CODE_* (多个)

  └─→ ./bin/freely daemon start
        → daemon 继承全部 ANTHROPIC_* 变量
        → _ensure_acp_bridge_running / _bridge_ensure_running
            → env "${_bridge_env[@]}" python3 acp-bridge.py ...
            → acp-bridge.py: env = os.environ.copy()
              → ACP binary 继承污染的环境变量
```

Even if Bug 1 is fixed (correct binary launched), Bug 2 means:
- opencode slot 的 settings.json 没有 `env` 字段 → `ANTHROPIC_MODEL` 不被覆盖
- claude slot 的 settings.json 有 `env` 字段 → 偶然覆盖污染变量

#### Bug 3 (旁路): agent-id 子串匹配

`grep -F "$(pwd)"` 在 develop 上匹配所有 worktree 路径前缀。

## Brainstorm

### 问题分解

三个修复点，scope 独立但都在 bridge 启动/检查链路：

**修复 1: monitor-ai-acp.sh 传 `--acp-bin`**
- 从 `$tool` 提取 base tool → tool-registry `acp.binary` → config.toml 解析路径
- 传入 `python3 "$bridge_script" start ... --acp-bin "$acp_bin"`
- 同时写入 `.bin` 文件，确保后续检查可检测到 binary 变化

**修复 2: bridge 启动前清理 ANTHROPIC_* 等环境变量**
- `_ensure_acp_bridge_running` 中 unset `ANTHROPIC_*`, `CLAUDE_CODE_*`, `AI_AGENT` 等
- monitor-ai-acp.sh 的 `_bridge_ensure_running` 中也做同样清理
- 只有 `ai_cli_tool_with_auth_assemble` 提取的 slot-specific env vars 保留

**修复 3: agent-id grep 精确匹配**
- `grep -F "$(pwd)"` → 增加行尾 `=` 或目录分隔符锚定

### 为什么不可能是其他原因

- ❌ **切号逻辑**: agent-table.toml slot 没变过，不存在切换触发
- ❌ **OPENCODE_CONFIG 不生效**: bridge env 已正确设置，问题在更上游
- ❌ **acp-bridge.py SDK 硬编码**: line 183 `os.environ.copy()` 是纯透传，不是主动设置
- ✅ **monitor-ai-acp.sh 不传 --acp-bin**: 代码确认 + 架构注释写死 "→ claude-agent-acp"

## Decision

三个修复合并为一个 candidate `C-20260704T004227Z-A`，因为都涉及 bridge 启动链路。

修复顺序：
1. 先修 monitor-ai-acp.sh 的 `_bridge_ensure_running` (传 --acp-bin + 写 .bin 文件)
2. 再修 `_ensure_acp_bridge_running` 的环境变量清理
3. 最后修 agent-id grep 子串匹配

### config.toml ACP binary 写入链路（当前正确）

`freely init` → `_init_acp_tool_setup()` (line 20477):

```
对 tool-registry.toml 中每个 tool:
  _tool = "claude" / "codex" / "opencode" / "cline"
  _config_key = "FREELY_ACP_{TOOL}_BIN"  (e.g. FREELY_ACP_OPENCODE_BIN)

  1. 检查 config.toml 是否已有缓存路径 → 有且可执行 → 跳过
  2. 搜索系统 PATH → command -v <binary>
  3. 搜索 cache → ~/.cache/freely/acp/{tool}/*/*/{binary}
  4. 下载 → ensure-acp-binary --tool {tool}

  → upsert_config_key "$project" "$_config_key" "$_found_path"
```

config.toml 当前值:
```
FREELY_ACP_CLAUDE_BIN = "/Users/zhaoyu/.nvm/.../bin/claude-agent-acp"
FREELY_ACP_CODEX_BIN = "/Users/zhaoyu/.cache/freely/acp/codex/.../codex-acp"
FREELY_ACP_OPENCODE_BIN = "/Users/zhaoyu/.opencode/bin/opencode"
FREELY_ACP_CLINE_BIN = "/Users/zhaoyu/.nvm/.../bin/cline"
```

**这个写入逻辑是正确的。** 问题在消费侧。

### ACP binary 消费链路对比

| 步骤 | `_ensure_acp_bridge_running` (freely) | `_bridge_ensure_running` (monitor-ai-acp.sh) |
|------|------|------|
| 获取 tool name | `AGENT_AI_TOOL` → 已有 | 参数 `$2` → `opencode-apikey-ds-flash-auto` |
| 提取 base_tool | `base_tool="${AGENT_AI_TOOL%%-*}"` ✅ | ❌ **没提取** |
| 查询 registry acp.binary | `_reg_bin="$(_tool_registry_get "$base_tool" "acp.binary")"` ✅ | ❌ **没查** |
| 查询 config.toml 路径 | `FREELY_ACP_$(echo "$base_tool" \| tr ...)_BIN` → `${!_config_key}` ✅ | ❌ **没查** |
| 传 `--acp-bin` 给 bridge | ✅ 传了 | ❌ **没传** → 默认 `claude-agent-acp` |
| 写 `.bin` 文件 | ✅ `printf ... > "$acp_bin_file"` | ❌ 没写 |
| 写 `.tool` 文件 | ✅ 写 | ✅ 写 |

`_bridge_ensure_running` 修复伪码:
```bash
local base_tool="${tool%%-*}"
local acp_bin acp_args=()
acp_bin="$(_tool_registry_get "$base_tool" "acp.binary" 2>/dev/null || echo "claude-agent-acp")"
# 从 config.toml 读取安装路径（优先）
local config_key; config_key="FREELY_ACP_$(echo "$base_tool" | tr '[:lower:]' '[:upper:]')_BIN"
local config_path; config_path="$(_read_config_value "$config_key" 2>/dev/null || true)"
[[ -n "$config_path" && -x "$config_path" ]] && acp_bin="$config_path"
# 解析 acp args
local raw_args; raw_args="$(_tool_registry_get "$base_tool" "acp.args" 2>/dev/null || true)"
[[ -n "$raw_args" ]] && read -ra acp_args <<<"$raw_args"

python3 "$bridge_script" start --project "$project" --acp-bin "$acp_bin" ${acp_args:+--acp-args "${acp_args[*]}"} >/dev/null 2>&1
printf '%s\n' "$acp_bin" > "$acp_bin_file"
```

## 诊断日志增强

当前日志只说 "launching opencode via acp"，完全不够。以下是必须增加的诊断日志点：

### 日志点 1: agent-table 解析时（load_config line ~4288）

当前输出:
```
[INFO] agent-table: worker_01 AGENT_AI_TOOL=opencode-apikey-ds-flash-auto
```

需要增加:
```
[INFO] agent-table: agent_id=manager_01 role=manager slot=opencode-apikey-ds-flash-auto base_tool=opencode acp_binary=opencode acp_args=acp
```
记录内容: `agent_id`, `role`, `slot`, `base_tool`, `acp_binary` (from registry), `provider`, `model` (from settings.json if available)

### 日志点 2: bridge 启动时（_ensure_acp_bridge_running 和 _bridge_ensure_running）

当前输出:
```
[INFO] ACP bridge started (bridge_pid=...)
```

需要增加:
```
[INFO] acp bridge launch: binary=/Users/.../opencode/bin/opencode args="acp" base_tool=opencode slot=opencode-apikey-ds-flash-auto config=~/.ai-auth/opencode-apikey-ds-flash-auto/settings.json model=deepseek-v4-flash-free provider=deepseek
```
记录内容: `binary` (完整路径), `acp_args`, `base_tool`, `slot`, `slot_config_path`, `model` (从 settings.json 提取), `provider` (API endpoint)

### 日志点 3: bridge 环境变量清理记录

```
[INFO] acp bridge env: sanitized=12 inherited ANTHROPIC_*=3 CLAUDE_CODE_*=8 AI_AGENT=1 kept_slot_vars="OPENCODE_CONFIG=/path/to/settings.json CLAUDE_CODE_PERMISSION_MODE=allow"
```
记录内容: `sanitized_count` (清理掉的变量数), `kept_vars` (保留的 slot-specific 变量), 清理的变量类型

### 日志点 4: ACP session 创建时（run-acp-prompt.py 或 monitor-ai-acp.sh writeback）

```
[INFO] acp session: session_id=xxx agent_role=manager actual_binary=opencode actual_model=deepseek-v4-flash-free actual_provider=https://api.deepseek.com/anthropic launch_kind=fresh
```
记录内容: `session_id`, `agent_role`, `actual_binary` (运行时确认), `actual_model` (从 session response 获取), `actual_provider`

### 日志点 5: 每个 cycle 完成时

在 session-state.env 或 cycle log 中追加:
```
last_cycle_acp_binary=<binary_basename>
last_cycle_model=<model_used>
last_cycle_provider=<api_endpoint>
last_cycle_agent_id=<manager_01|worker_01|reviewer_01>
```

## 测试用例

### 测试 1: ACP binary 与 slot base_tool 一致性

```
测试名称: test-acp-binary-matches-agent-table-slot
测试目标: 验证 agent-table.toml 每个 agent role 的 slot → base_tool → acp.binary 链路正确

测试步骤:
1. 读取 agent-table.toml 中每个 [[agents]] 的 {role}_slot
2. 从 slot 名提取 base_tool（%%-* 之前的部分）
3. 从 tool-registry.toml 查询 {base_tool}.acp.binary
4. 验证 binary 不为空且合法
5. 验证 config.toml 中 FREELY_ACP_{TOOL_UPPER}_BIN 指向的路径存在且可执行
6. 对每个不同的 base_tool，验证只有一个唯一的 acp binary

断言:
- 每个 agent role 的 slot 都能成功解析到 acp.binary
- 不同 base_tool 不被错误映射到同一个默认 binary（claude-agent-acp）
- FREELY_ACP_*_BIN 路径存在且可执行

实现: bin/test-acp-binary-matches-agent-table-slot
```

### 测试 2: 环境变量污染检测

```
测试名称: test-acp-bridge-env-sanitization
测试目标: 验证 bridge 启动后环境中无父进程泄露的 AI 相关环境变量

测试步骤:
1. 在 shell 环境中设置模拟的 ANTHROPIC_MODEL, ANTHROPIC_BASE_URL, AI_AGENT 等变量
2. 启动 freely daemon start --task-mode listen --force
3. 读取 bridge 进程的 /proc/<pid>/environ（或 ps eww）
4. 检查是否存在: ANTHROPIC_MODEL, ANTHROPIC_AUTH_TOKEN, ANTHROPIC_BASE_URL,
   ANTHROPIC_DEFAULT_OPUS_MODEL, ANTHROPIC_DEFAULT_SONNET_MODEL, ANTHROPIC_DEFAULT_HAIKU_MODEL,
   CLAUDE_CODE_*, AI_AGENT
5. 检查 bridge env 中只有 slot-specific 变量（如 OPENCODE_CONFIG）

断言:
- bridge 进程环境中无 ANTHROPIC_* 变量（除非 slot settings.json 的 env 字段显式设置）
- bridge 进程环境中无 CLAUDE_CODE_* 变量
- bridge 进程环境中无 AI_AGENT 变量
- bridge env 中包含 slot settings.json env 字段中显式声明的变量

实现: bin/test-acp-bridge-env-sanitization
```

### 测试 3: Bridge 启动完整性

```
测试名称: test-acp-bridge-start-records
测试目标: 验证 bridge 启动后 .bin 和 .tool 文件都正确写入

测试步骤:
1. 启动 freely daemon start --task-mode listen --force
2. 检查 /tmp/freely-acp-<hash>.pid.bin 文件存在且内容非空
3. 检查 /tmp/freely-acp-<hash>.pid.tool 文件存在且内容非空
4. 验证 .bin 文件内容等于 tool-registry 中的 acp.binary
5. 验证 .tool 文件内容等于 AGENT_AI_TOOL
6. 停止 daemon，修改 .bin 为错误值
7. 重新启动，验证 bridge 检测到 binary 变化并重启

断言:
- .bin 文件在 bridge 启动后立即写入
- .tool 文件在 bridge 启动后立即写入
- binary 变化能被检测到并触发重启

实现: bin/test-acp-bridge-start-records
```

### 测试 4: 端到端模型验证（smoke test）

```
测试名称: test-acp-session-model-matches-config
测试目标: 启动 daemon → 创建 session → 验证 session JSONL 中 model 与 agent-table slot 配置一致

测试步骤:
1. 确认 agent-table.toml 中 manager_slot = opencode-apikey-ds-flash-auto
2. 启动 freely daemon start --task-mode auto --force
3. 等待第一个 manager cycle 完成
4. 读取最新 session JSONL（~/.claude/projects/{slug}/{session_id}.jsonl 或 ~/.opencode/sessions/）
5. 提取 model 字段
6. 对比 model 与 slot settings.json 中配置的 model

断言:
- session JSONL 中 model 与 agent-table slot 对应的 settings.json 中的 model 一致
- 如果 slot 是 opencode-* → model 是 opencode 格式的 deepseek-v4-flash-free
- 如果 slot 是 claude-* → model 与 claude settings.json env.ANTHROPIC_MODEL 一致

实现: bin/test-acp-session-model-matches-config
```

## Candidate

- candidate_id: C-20260704T004227Z-A
- status: promoted
- milestone: M-20260704T004227Z-A
