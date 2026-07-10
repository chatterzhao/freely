---
local_id: raw-20260704T004227Z27Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260704T004227Z-A
platform_ids:
  github:
    issue_id: '3722'
    url: https://github.com/chatterzhao/freely/issues/3722
    synced_at: ''
  gitee:
    issue_id: IJYPWD
    url: https://gitee.com/zhaoquan/freely/issues/IJYPWD
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-04T00:42:51Z'
updated_at: '2026-07-04T00:42:51Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

\n\n
## 现象

config.toml 和 agent-table.toml 均配置使用 opencode-apikey-ds-flash-auto（deepseek-v4-flash-free 模型），但实际推理全部走 Claude Code + deepseek-v4-pro 模型。

## 证据

1. 所有 freely session（manager + worker）的 JSONL 文件落在 ~/.claude/projects/ 目录，不在 ~/.opencode/sessions/
2. Session JSONL 中 model=deepseek-v4-pro，entrypoint=sdk-cli，version=2.1.121（Claude Code 格式）
3. OpenCode sessions 目录几乎为空
4. deepseek-v4-pro 只在 claude-apikey-ds-pro-auto/settings.json 中配置，opencode-apikey-ds-flash-auto 配置的是 deepseek-v4-flash-free

## 旁路 Bug

_startup agent-id 解析存在子串匹配 bug：grep -F "$(pwd)" 在 develop worktree（路径 .../freely）会匹配所有 .../freely-worktrees/... 路径，导致 develop 上 resolve 出 worker_01 而非 manager_01。

## 分析方向

- _ensure_acp_bridge_running 如何将 slot 配置传递给 ACP binary
- OPENCODE_CONFIG env var 是否正确设置
- acp-bridge.py 的 SDK session 存储路径是否硬编码
- 是否存在 slot fallback/switch 机制导致 claude-pro 被选中
