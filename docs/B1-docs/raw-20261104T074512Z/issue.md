---
schema_version: '1'
local_id: raw-20261104T074512Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T074512Z-A
platform_ids:
  github:
    issue_id: '4158'
    url: https://github.com/chatterzhao/freely/issues/4158
    synced_at: ''
  gitee:
    issue_id: IKSW2M
    url: https://gitee.com/zhaoquan/freely/issues/IKSW2M
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-04T07:45:13Z'
updated_at: '2026-11-04T07:45:18Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
---

workflow_kind: fix

## 根因
`bin/freely-package` 对 `--output` 不做任何路径校验，直接 `rm -rf "$OUTPUT"`；`--output /`、`--output ~`、`--output ..` 会把删除目标指向仓库外。

## 证据
- `bin/freely-package:46-52`：`--output` 直接赋值，无校验。
- `bin/freely-package:57-59`：仅空值兜底为 `$HOME/.freely/versions/$VERSION`（因此 `--output ""` 不构成风险，原 #4157 的该条描述有误）。
- `bin/freely-package:68`：`rm -rf "$OUTPUT"` 先于 `mkdir -p`，无 realpath 前缀校验、无 dry-run、无 `--one-file-system`。

## 影响
- `freely freely-package --version <valid> --output /` 在 Linux 上会递归删除根目录（macOS 受 SIP 限制，但部分路径仍可删）。
- `--output ~` 会删除整个用户主目录；`--output /Users` 同理。
- 该命令通常由发布流程以较高权限执行，误触概率不低。

## 修复方案
1. 解析后立即规范化：`OUTPUT="$(cd "$(dirname "$OUTPUT")" 2>/dev/null && pwd -P)/$(basename "$OUTPUT")"`，解析失败即退出。
2. 拒绝以下目标：`/`、`$HOME` 本身、`..`、仓库根，以及 `$HOME/.freely/versions` 的祖先目录；用「必须位于 `$HOME/.freely/versions/` 或显式 `--allow-outside`」做白名单。
3. 删除前加 `[[ "$OUTPUT" == "$HOME/.freely/versions/"* ]] || fail`；先建临时目录再原子替换，避免先删后建。
4. 增加 `--dry-run`，打印将删除的绝对路径，并要求 `--yes` 才执行。

## 验收标准
- RED：`freely-package --version 2026.11.03-stable --output /` 退出非零并打印拒绝原因；当前执行 `rm -rf /`。
- RED：`--output ~`、`--output ..`、`--output "$HOME"` 同样被拒。
- GREEN：`--output "$HOME/.freely/versions/2026.11.03-stable"` 正常通过。
- GREEN：`--dry-run` 只打印目标路径，不执行删除。
