---
local_id: raw-20260630T135725Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260630T135725Z-A
platform_ids:
  github:
    issue_id: '3661'
    url: https://github.com/chatterzhao/freely/issues/3661
    synced_at: ''
  gitee:
    issue_id: IJXXNU
    url: https://gitee.com/zhaoquan/freely/issues/IJXXNU
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T13:57:47Z'
updated_at: '2026-06-30T13:57:47Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因
PR #3658+#3660 合并后 _init_acp_tool_setup() 使用 get_config/set_config，但这两个函数在代码库中不存在。

## 修复
- 读取: grep config.toml
- 写入: upsert_config_key (已有函数 L4331)
- Runtime: ${!_config_key:-} 间接展开
