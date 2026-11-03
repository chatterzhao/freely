---
schema_version: '1'
local_id: raw-20261103T091157Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T091157Z-A
platform_ids:
  github:
    issue_id: '4138'
    url: https://github.com/chatterzhao/freely/issues/4138
    synced_at: ''
  gitee:
    issue_id: IKSNPK
    url: https://gitee.com/zhaoquan/freely/issues/IKSNPK
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-03T09:11:57Z'
updated_at: '2026-11-03T09:29:16Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-03T01:40:00Z'
closeout_note: ''
---
# chore: 双平台 open issue 对齐与本地 raw 元数据回填


workflow_kind: fix

## 现象
走规范的 feedback/wt-create/pr-*/wt-close 后，双平台 issue 仍不对齐：

- GitHub 2623 issues（open 13），Gitee 488 issues（open 17）。
- 4 个 open issue 仅存在于 Gitee：raw-20260715T131531Z、raw-20260718T035754Z、raw-20260719T054212Z、raw-20260720T032133Z。
- 本地 780 个 raw 文档中，574 个缺 Gitee 编号、30 个缺 GitHub 编号；13 个 open issue 尚无本地 raw 文档。

## 根因
历史阶段曾以单平台为主（2026-05 GitHub 1572 条 / Gitee 2 条；2026-07 Gitee 234 条 / GitHub 229 条），早期 issue 只建在单一平台且未回填镜像；本地 raw 文档的 platform_ids 也没有系统性回填。open 集合差异则是 4 个 Gitee-only issue 没有 GitHub 镜像。

## 任务
1. 为全部 17 个 open raw key 物化本地 docs/B1-docs/raw-{key}/issue.md（Usage:
  freely raw-issue-pull --raw-key <key> [--target <dir>]

Pull a raw issue from platform by matching raw-{key} in OPEN issue titles.
Materializes to docs/B1-docs/raw-{key}/issue.md with proper platform_ids.

Options:
  --raw-key <key>   Raw issue key (YYYYMMDDTHHMMSSZ format)
  --target  <dir>   Target directory (default: docs/B1-docs/raw-{key}/)

Example:
  freely raw-issue-pull --raw-key 20260506T100035Z）。
2. 为 4 个 Gitee-only open issue 创建 GitHub 镜像（），使两平台 open 集合按 raw key 完全一致。
3. 回填本地 raw 文档 platform_ids：凡平台已存在副本但未记录编号的，按 raw key 匹配回填（不创建历史 issue）。
4. 产出可复跑的校验脚本 docs/system/workspace/scripts/tests/test-platform-open-parity.py：断言两平台 open raw key 集合相等、每个 open issue 本地有文档且双平台编号齐全。
5. 历史 closed 总量差异作为已知遗留债记录（不批量补建历史 issue）。

## 验收
- 两平台 open raw key 集合相等（当前 13=13）。
- 17 个 open issue 均有本地 raw 文档且 platform_ids.github / platform_ids.gitee 均非空且与平台编号一致。
- 校验脚本可重复运行且通过。
