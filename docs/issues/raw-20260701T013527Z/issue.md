---
local_id: raw-20260701T013527Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3674'
    url: https://github.com/chatterzhao/freely/issues/3674
    synced_at: ''
  gitee:
    issue_id: IJXYY1
    url: https://gitee.com/zhaoquan/freely/issues/IJXYY1
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-01T01:35:48Z'
updated_at: '2026-07-01T01:35:48Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n
## 问题描述

启动 freely daemon 时，daemon-launch.log 中出现：

```
line 14052: get_config: command not found
```

## 根因

freely runtime 脚本第 14052 行调用了未定义的 `get_config` 函数。该行意图读取 config.toml 中的 ACP binary 路径（如 FREELY_ACP_CLAUDE_BIN），但函数不存在。

## 修复方案

将 `get_config "$key" ""` 替换为 `${!_config_key:-}` — bash间接变量展开。load_config 已通过 toml2env 将所有 config.toml 值导出为环境变量。
