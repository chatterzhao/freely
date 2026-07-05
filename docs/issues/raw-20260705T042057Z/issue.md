---
local_id: raw-20260705T042057Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3740'
    url: https://github.com/chatterzhao/freely/issues/3740
    synced_at: ''
  gitee:
    issue_id: IJYU0G
    url: https://gitee.com/zhaoquan/freely/issues/IJYU0G
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-05T04:21:17Z'
updated_at: '2026-07-05T04:21:17Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

多处从 slot 提取 base_tool 后没有校验是否在 tool-registry 中。不支持的 base_tool 会静默继续，导致运行时错误难以诊断。

## 修复

1. 新增 _validate_base_tool_from_slot 函数：提取 base_tool → 校验 tool-registry → 不通过则阻塞并列出支持的工具（动态读取）
2. 在所有入口调用：worker launch、daemon bridge scan、cycle bridge check
3. 修复 stop_project_runtime 清理全部 bridge socket
