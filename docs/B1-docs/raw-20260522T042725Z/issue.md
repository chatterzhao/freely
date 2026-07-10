---
local_id: raw-20260522T042725Z25Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2109'
    url: https://github.com/chatterzhao/freely/issues/2109
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-22T04:27:37Z'
updated_at: '2026-06-17T00:26:27Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed---

## 问题
1. active slot 写部分名 apikey-test，应写全名 claude-apikey-test
2. switch 白名单缺 claude
3. --settings-file 死代码
4. switch apikey 检测 ==apikey-* 对全名 claude-apikey-* 无效，应改为 *-apikey-*
5. watchdog auto-switch 不知道 apikey alias，需要 persist_project_tool_selection 恢复 alias 检测
