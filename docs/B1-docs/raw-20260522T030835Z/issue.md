---
local_id: raw-20260522T030835Z35Z
kind: raw
phase_state: dropped
platform_ids:
  github:
    issue_id: '2105'
    url: https://github.com/chatterzhao/freely/issues/2105
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-22T03:08:48Z'
updated_at: '2026-06-21T20:13:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 要改的

### cmd_login (ai-cli:1076)
apikey模式不只是建空slot目录，还要：
1. 复制settings文件到slot目录
2. 追加alias到.zshrc
3. 写active slot

### cmd_switch (ai-cli:1273)  
apikey slot切换时，除了写active slot文件，还要更新项目 config.env 的 AI_TOOL 为 alias名

## 不改的
- account模式：完全不变
- codex apikey：现有流程不变
- 其他命令(save/list/status/delete/whoami)
