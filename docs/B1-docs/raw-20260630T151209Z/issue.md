---
local_id: raw-20260630T151209Z09Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260630T151209Z-A
platform_ids:
  github:
    issue_id: '3666'
    url: https://github.com/chatterzhao/freely/issues/3666
    synced_at: ''
  gitee:
    issue_id: IJXXXM
    url: https://gitee.com/zhaoquan/freely/issues/IJXXXM
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T15:12:34Z'
updated_at: '2026-06-30T15:12:34Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 改进
1. _read_config_value() 统一函数：有 config 逐字段读，无 config 返回空不报错
2. 已有字段不动，仅新增缺失字段
3. --reset 强制覆盖所有字段
4. L20045 平台检查改用统一函数
