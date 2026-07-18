---
local_id: raw-20260717T235950Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260717T235950Z-A
platform_ids:
  github:
    issue_id: '3985'
    url: https://github.com/chatterzhao/freely/issues/3985
    synced_at: ''
  gitee:
    issue_id: IK1VFQ
    url: https://gitee.com/zhaoquan/freely/issues/IK1VFQ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-18T00:00:14Z'
updated_at: '2026-07-18T00:00:14Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因
PR #3980/#3984 引入 autonomous close gate 后，wt-close usage() 的 --force 描述已同步（绕过自治门禁拒绝判定/正常自治关闭不需要此标志），但 docs/system/workspace/commands.md §wt-close 选项表 --force 行（约 L193）仍为旧文案『永久丢弃（不可恢复）。有未合并提交时需同时 --discard-unmerged』，缺自治门禁语义——文档与 --help 真源不一致。

## 影响
agent/人按 commands.md 理解 --force 时缺『正常自治关闭不需要此标志、gate 自动判定放行』的关键语义，可能误用 --force 绕过 gate。

## 修复方案
commands.md --force 行同步为与 usage() 一致的描述（含绕过自治门禁拒绝判定 + 正常自治关闭不需要）。验收：该行含『自治门禁』且与 wt-close --help 语义一致。
