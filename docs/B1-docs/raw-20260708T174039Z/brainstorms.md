---
b1_id: B1-20260708T174039Z
phase_state: completed
source_raw: raw-20260708T174039Z
created_at: 2026-07-08
---

# B1_IBM: tool-launchers.sh socket path missing base_tool

## Input
- raw issue: raw-20260708T174039Z
- 发现过程：daemon AI session 47 分钟零输出，深入排查确认根因

## Problem
commit 191afb82c 在 5 个文件中加入了 per-tool ACP bridge socket（带 base_tool 后缀），但遗漏了 tool-launchers.sh。

tool_run_acp_from_prompt_file() 第 823 行：`_bridge_socket "$project"` 不传 base_tool
→ 计算出的 socket 路径无后缀：`/tmp/freely-acp-<hash>.sock`
→ acp-bridge.py 监听带后缀的路径：`/tmp/freely-acp-<hash>-claude.sock`
→ run-acp-prompt.py 连接失败（FileNotFoundError）
→ cycle log 完全空白
→ Manager AI session 零输出

## Brainstorm
### Option A: 改 tool-launchers.sh 传 base_tool
在 `_bridge_socket "$project"` 后加 `"$tool"`，此时 `$tool` 已通过 `_resolve_tool_family` 解析为 base family name（如 `claude`）。

### Option B: 改 _bridge_socket 函数默认值
让 `_bridge_socket` 在不传 base_tool 时自动检测当前 slot 的 base_tool。但这引入隐式依赖，不推荐。

## Decision: Option A
- 修改最小（一行）
- 语义清晰：明确传入已解析的 tool 名
- 与其他所有 call site 一致（都传 base_tool）

## Candidate
- candidate_id: C-20260708T174039Z-A
- status: promoted
- milestone: M-20260708T174039Z-A
