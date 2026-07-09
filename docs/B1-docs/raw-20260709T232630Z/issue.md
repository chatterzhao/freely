---
local_id: raw-20260709T232630Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260709T232630Z-A
platform_ids:
  github:
    issue_id: '3848'
    url: https://github.com/chatterzhao/freely/issues/3848
    synced_at: ''
  gitee:
    issue_id: IK010Y
    url: https://gitee.com/zhaoquan/freely/issues/IK010Y
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-09T23:26:52Z'
updated_at: '2026-07-09T23:26:52Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题
三个 bridge（claude/opencode/cline）共用同一个 `acp-bridge.log`：
- 每个 bridge 启动时 `_truncate_log()` 截断日志，互相覆盖
- 日志行无法区分来自哪个 bridge
- 空闲检测、错误诊断无法定位到具体 bridge

## 修复
`acp-bridge.log` → `acp-bridge-{base_tool}.log`

| 文件 | 改动 |
|------|------|
| `acp-bridge.py` | `_log_file()` 加入 base_tool 后缀 |
| `monitor-ai-acp.sh` | `_bridge_log_file()` 加入 base_tool 参数 |
| `freely` | 所有硬编码 `acp-bridge.log` 改为 per-tool 路径 |

## 验收
- 每个 bridge 写入独立的日志文件
- truncate 仅影响自己的日志
- 错误检测/健康检查能正确找到对应 bridge 的日志
