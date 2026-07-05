---
b1_id: B1-20260627T084551Z
phase_state: completed
source_raw: raw-20260627T084545Z51Z
source_url: https://github.com/chatterzhao/freely/issues/3586
produced_candidate: C-20260627T084551Z-A
created_at: 2026-06-27
---

# B1_IBM: run-acp-prompt.py fork 改用 session/fork

## Input
- 来源: raw-20260627T084545Z51Z (GitHub #3586)
- 调研文档: .acp-session-fork-review.md

## 调用链追踪

### fork 当前实现

```
freely: manager 委派 → LAUNCH_KIND_SELECTED="fork"
  → monitor-ai-acp.sh --launch-kind fork
    → run-acp-prompt.py --launch-kind fork --resume {parent_id}
      → L456-462:
          session_result = client.request("session/new", new_params)
          # "Using session/new is safe" ← 注释过时
```

### session/fork 协议

ACP 官方方法 `session/fork`（`agentclientprotocol/agent-client-protocol` v0.13.7）：
- 参数: `{sessionId: parent_id, cwd: ..., mcpServers: []}`
- 返回: `{sessionId: child_uuid}`
- 效果: 新 UUID + 继承 parent 完整历史 → prompt 缓存命中

### 各工具实测

| 工具 | sessionCapabilities | fork |
|------|--------------------|------|
| Claude (0.31.4) | `{fork, list, resume, close}` | ✅ |
| OpenCode (1.17.11) | `{fork, list, resume, close}` | ✅ |
| Cline (3.0.29) | `{}` | ❌ |
| Codex (0.15.0) | `{list, close}` | ❌ |

### Bug G: ensure-codex-acp

```bash
REGISTRY="$SCRIPT_DIR/tool-registry.json5"  # ← 文件已改为 .toml
```
`_reg_get` 返回空 → `set -e` 退出。缓存命中的二进制仍可用，但首次安装/升级失败。

## Decision

两个改动都是唯一方案，无替代。

```python
# run-acp-prompt.py L456-462: fork 路径
if launch_kind == "fork":
    try:
        session_result = client.request("session/fork",
            {"sessionId": parent_id, "cwd": cwd, "mcpServers": []}, timeout=30)
    except Exception:
        session_result = client.request("session/new",
            {"sessionId": args.session_id, "cwd": cwd, "mcpServers": []}, timeout=30)
```

ensure-codex-acp: `tool-registry.json5` → `tool-registry.toml`（1 行）。

## Candidate
- candidate_id: C-20260627T084551Z-A
- status: promoted
- milestone: M-20260627T084551Z-A
