---
local_id: raw-20260710T043521Z
kind: raw
phase_state: absorbed
platform_ids:
  gitee:
    issue_id: IK04AI
    url: https://gitee.com/zhaoquan/freely/issues/IK04AI
    synced_at: ''
primary_platform: gitee
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-10T12:35:43+08:00'
updated_at: '2026-07-10T12:35:43+08:00'
intake_id: ''
author: platform
channel: gitee
session_refs: []
---

\n\n## 问题
scan 仍输出 641 个 `2a_state_mismatch` items，它们 phase_state=absorbed/dropped, platform_state=closed，但无 platform_ids。
scan 逻辑: `terminal phase + platform_state set + no real platform data → 2a_state_mismatch`
应改为: `platform_state=closed + no platform_ids → 静默跳过`

另有 11 个文件 `platform_state=closed---` (YAML delimiter 污染)。

## 修复
1. scan decision tree: platform_state=closed + 无 platform_ids → skip
2. 修正 11 个 corrupt 文件

## 验收
- scan items 从 690 降到 ~50
