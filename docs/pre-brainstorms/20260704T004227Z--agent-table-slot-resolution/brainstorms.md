---
b1_id: B1-20260704T004227Z
phase_state: completed
source_raw: raw-20260704T004227Z
source_url: https://github.com/chatterzhao/freely/issues/3722
produced_candidate: C-20260704T004227Z-A
created_at: 2026-07-04
---

# B1_IBM: agent-table slot 解析与模型匹配修复

## Input

- **来源**: raw-20260704T004227Z (GitHub #3722, Gitee IJYPWD)
- **类型**: fix — 配置与实际行为不一致
- **严重程度**: 高 — 消耗错误模型的 token（pro 而非 flash），成本显著增加

## Problem

agent-table.toml 和 config.toml 均配置使用 `opencode-apikey-ds-flash-auto`（deepseek-v4-flash-free），但实际推理全部走 Claude Code + deepseek-v4-pro 模型。

### 证据链

1. **Session 存储位置错误**: 所有 freely session JSONL 文件落 `~/.claude/projects/`，不在 `~/.opencode/sessions/`
2. **Session 格式错误**: JSONL 中 `model=deepseek-v4-pro`, `entrypoint=sdk-cli`, `version=2.1.121` —— 这是 Claude Code 格式
3. **Slot 目录实际使用错误**: `deepseek-v4-pro` 只在 `claude-apikey-ds-pro-auto/settings.json` 中配置
4. **Daemon 日志显示正确工具已选**: `launching opencode via acp`，但实际 session 跑到 claude 目录

### 旁路 Bug

`_startup` 中 agent-id 解析（line 4278）：`grep -F "$(pwd)"` 用固定字符串匹配，当 `pwd=/Users/.../freely`（develop worktree）时，会匹配 agent-id.env 中所有 `.../freely-worktrees/...` 路径（子串匹配）。首个匹配行是 `worker_01`，导致 develop 上 resolve 出 `worker_01` 而非 `manager_01`。

## Brainstorm

### 问题分解

本 issue 涉及两个独立子问题，应分开处理：

**子问题 A: agent-id 子串匹配 bug**
- 范围: `freely` runtime line 4278，`grep -F "$(pwd)"` 改为精确行尾/分隔符匹配
- 影响: develop 上 agent 身份错判（当前配置下不影响 slot，但逻辑已坏）

**子问题 B: 实际使用的模型与 slot 配置不符**
- 需要确定是哪个环节导致 `deepseek-v4-pro` 被使用
- 三个怀疑方向

### 方向 B1: OPENCODE_CONFIG 未被 opencode ACP server 正确读取

`ai_cli_tool_with_auth_assemble` (line 130) 正确发出了 `OPENCODE_CONFIG=<path>`。但 opencode v1.17.13 在 ACP 模式下可能不读这个 env var，或用法与预期不同。

验证方法: 在 bridge 进程 env 中加入 debug trace，或 strace/dtrace 看 opencode 实际读了哪个配置文件。

### 方向 B2: acp-bridge.py SDK 硬编码 Claude 行为

`acp-bridge.py` 底层用 `@anthropic-ai/claude-agent-acp` SDK。该 SDK 可能:
- 总是把 session 写到 `~/.claude/projects/{slug}`
- 在 session/set_mode 时覆盖模型配置
- 不理会上游传的 `OPENCODE_CONFIG`

验证方法: 检查 `acp-bridge.py` 的 SDK session 创建流程，看是否有模型覆盖逻辑。

### 方向 B3: 环境变量污染

`acp-bridge.py` 的 `start_server()` (line 183) 执行 `env = os.environ.copy()`，继承父进程全部环境变量。如果 daemon 进程环境中有残留的 `ANTHROPIC_MODEL=deepseek-v4-pro` 或 `CLAUDE_CODE_*` 变量，它们会被 ACP server 优先读取。

验证方法: 在 bridge launch 前 `log_info` 打印关键 ANTHROPIC_* / OPENCODE_* / CLAUDE_CODE_* 环境变量。

## Decision: 分两个 candidate 处理

**子问题 A** (agent-id 子串匹配) 是独立、明确、可立即修复的 bug，scope 小，直接改 grep 逻辑即可。

**子问题 B** (模型不匹配) 需要先验证三个方向，确定根因后再设计修复方案。

在同一个 raw issue 下拆为两个 candidate:
- C-20260704T004227Z-A: 修复 agent-id 子串匹配 bug
- C-20260704T004227Z-B: 修复 slot 模型不匹配（需先诊断根因）

## Candidate

- candidate_id: C-20260704T004227Z-A
- status: promoted
- milestone: M-20260704T004227Z-A
