---
b1_id: B1-20260704T004227Z
phase_state: completed
source_raw: raw-20260704T004227Z
source_url: https://github.com/chatterzhao/freely/issues/3722
produced_candidate: C-20260704T004227Z-A
created_at: 2026-07-04
---

# B1_IBM: agent-table slot 解析与环境变量污染

## Input

- **来源**: raw-20260704T004227Z (GitHub #3722, Gitee IJYPWD)
- **类型**: fix — 配置与实际行为不一致
- **严重程度**: 高 — 消耗错误模型的 token（pro 而非 flash），成本显著增加

## Problem

agent-table.toml 配置使用 `opencode-apikey-ds-flash-auto`（deepseek-v4-flash-free），但实际推理全部走 Claude Code + deepseek-v4-pro 模型。

### 根因：环境变量污染

**确认根因：父进程（Claude Code session）设置的 `ANTHROPIC_*` 环境变量被 freely daemon 继承，并通过 `acp-bridge.py` 透传给 ACP server binary，覆盖了 slot 配置。**

#### 污染链路

```
Claude Code session (当前对话)
  → 设置: ANTHROPIC_MODEL=deepseek-v4-pro[1m]
           ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
           ANTHROPIC_AUTH_TOKEN=sk-...
           CLAUDE_CODE_ENTRYPOINT=cli
           AI_AGENT=claude-code_2-1-199_agent
  → Bash 执行: ./bin/freely daemon start
      → freely daemon 继承全部 ANTHROPIC_* 变量
      → _ensure_acp_bridge_running()
          → env "${_bridge_env[@]}" python3 acp-bridge.py ...
              → acp-bridge.py: env = os.environ.copy()
                  → ACP server binary (opencode acp) 收到:
                      - OPENCODE_CONFIG=.../opencode-apikey-ds-flash-auto/settings.json ✓
                      - ANTHROPIC_MODEL=deepseek-v4-pro[1m] ← 未清理！
                      - ANTHROPIC_AUTH_TOKEN=sk-... ← 未清理！
```

#### 为什么 claude slot 不受影响

`ai_cli_tool_with_auth_assemble` (line 198-223) 会从 slot 的 `settings.json` 的 `env` 字段提取环境变量，通过 `env "${_bridge_env[@]}"` 注入。对于 claude slot（如 `claude-apikey-ds-flash-auto`），其 `settings.json` 有 `env: {ANTHROPIC_MODEL: "deepseek-v4-flash[1m]", ...}`，会覆盖继承的污染变量。

但 opencode slot 的 `settings.json` 没有 `env` 字段——模型配置用的是 opencode 专有格式 `"model": "opencode/deepseek-v4-flash-free"`，不是 `ANTHROPIC_MODEL` 环境变量。所以继承的 `ANTHROPIC_MODEL=deepseek-v4-pro[1m]` 不会被覆盖，ACP binary 读取了这个错误的模型。

#### 为什么 session 文件落在 ~/.claude/projects/

- `CLAUDE_CODE_ENTRYPOINT=cli` 从 Claude Code 父进程继承
- `AI_AGENT=claude-code_2-1-199_agent` 从 Claude Code 父进程继承
- 这些变量告诉 ACP SDK 将 session 写入 Claude 目录

#### 证据确认

```bash
# 当前 shell 中确实存在这些变量：
$ env | grep -E "ANTHROPIC_|CLAUDE_CODE|AI_AGENT"
ANTHROPIC_MODEL=deepseek-v4-pro[1m]
ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
ANTHROPIC_AUTH_TOKEN=sk-<redacted>
AI_AGENT=claude-code_2-1-199_agent
CLAUDE_CODE_ENTRYPOINT=cli
...
```

### 旁路 Bug

`_startup` 中 agent-id 解析（line 4278）：`grep -F "$(pwd)"` 用固定字符串匹配，当 `pwd=.../freely`（develop worktree）时，会匹配 agent-id.env 中所有 `.../freely-worktrees/...` 路径（子串匹配），导致 develop 上 resolve 出 `worker_01` 而非 `manager_01`。

## Brainstorm

### 问题分解

**子问题 A: agent-id 子串匹配 bug**
- 范围: `freely` runtime line 4278，`grep -F "$(pwd)"` 改为精确行尾锚定匹配
- 影响: develop 上 agent 身份错判

**子问题 B: 环境变量污染（根因）**
- 位置: `_ensure_acp_bridge_running` (line ~14155) + `acp-bridge.py` `start_server()` (line 183)
- 两个环节需要修复

### 方向 B1: 在启动 bridge 前清理环境变量（首选）

在 `_ensure_acp_bridge_running` 中，`env "${_bridge_env[@]}"` 之前，先 unset 所有 AI-tool 相关的继承环境变量：
- `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL`, `ANTHROPIC_MODEL`
- `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`
- `CLAUDE_CODE_*` (全部)
- `AI_AGENT`
- `OPENCODE_CONFIG`, `CODEX_HOME` (留给 bridge env 重新设置)

然后让 `ai_cli_tool_with_auth_assemble` 提取的 slot-specific env vars 成为唯一真源。

### 方向 B2: 在 acp-bridge.py 中清理环境变量

在 `AcpBridge.start_server()` 的 `env = os.environ.copy()` 之后，清理 AI-tool 相关的环境变量，只保留上游显式传入的。

方向 B1 更优——清理在入口处做，不依赖 acp-bridge.py 了解哪些 env var 属于哪个工具。

### 方向 B3: opencode slot settings.json 增加 env 字段（补丁方案）

在 `~/.ai-auth/opencode-apikey-ds-flash-auto/settings.json` 中增加 `env` 字段设置模型相关变量。但这是治标不治本——下次换其他工具/open code 的其他 slot 同样会出问题。

## Decision

**采纳方向 B1（清理环境变量）+ 修复子问题 A（grep 子串匹配）**

在同一个 raw issue 下拆为两个 candidate:
- C-20260704T004227Z-A: 修复 agent-id 子串匹配 bug + 在 bridge launch 前清理 AI 环境变量
- C-20260704T004227Z-B: 已吸收到 C-A——根因已确定，不需要单独研究

## Candidate

- candidate_id: C-20260704T004227Z-A
- status: promoted
- milestone: M-20260704T004227Z-A
