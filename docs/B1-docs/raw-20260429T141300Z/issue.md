---
local_id: raw-20260429T141300Z00Z
kind: raw
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
platform_ids:
  github:
    issue_id: '286'
    url: https://github.com/chatterzhao/freely/issues/286
    synced_at: '2026-05-10T09:30:35Z'
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: 2026-04-29 14:13:37+00:00
updated_at: 2026-05-17T04:47:25Z
intake_id: 20260429-071337-docs-system-workspace-scripts-ut
author: zhaoquan
channel: supervisor
session_refs: []
platform_state: closed
---

写一个脚本 docs/system/workspace/scripts/util/count-lines.sh：
1. 统计 docs/system/workspace/scripts/runtime/ 下所有 .sh 和 .py 文件的行数
2. 按行数降序排列
3. 输出格式：`行数 文件路径`
完成后提交。
