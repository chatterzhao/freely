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

## Candidate

- candidate_id: C-20260704T004227Z-A
- status: promoted
- milestone: M-20260704T004227Z-A
