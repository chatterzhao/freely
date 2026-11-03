---
local_id: raw-20260714T012901Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '3899'
    url: https://github.com/chatterzhao/freely/issues/3899
    synced_at: ''
  gitee:
    issue_id: IK0TKM
    url: https://gitee.com/zhaoquan/freely/issues/IK0TKM
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-14T01:29:23Z'
updated_at: '2026-07-14T01:29:23Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因
freely init 不初始化 AI_MODE 环境变量，导致 set -u 下 $AI_MODE 裸引用触发 unbound variable crash。daemon-run 输出丢弃到 /dev/null，crash 无声，表现为 supervisor 无限重启循环。

## 影响
3 处 log/echo 中的裸 $AI_MODE (line 22697, 22719, 24994) 在 AI launch 点前崩溃，daemon 永远无法启动 AI cycle。

## 修复方案
$AI_MODE → ${AI_MODE:-none}
