---
local_id: raw-20260629T165403Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260629T165403Z-A
platform_ids:
  github:
    issue_id: '3634'
    url: https://github.com/chatterzhao/freely/issues/3634
    synced_at: ''
  gitee:
    issue_id: IJXON1
    url: https://gitee.com/zhaoquan/freely/issues/IJXON1
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-29T16:54:23Z'
updated_at: '2026-06-29T16:54:23Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 背景

PR #3633 合并后实测发现两个 bug。

### Bug 1: args[@] unbound variable

    line 206: set -- "${args[@]}"

当 --raw-key 或 --branch 提供时 args 数组为空，set -euo pipefail 下触发 unbound variable 错误。

修复：加 if [[ ${#args[@]} -gt 0 ]] 守卫。

### Bug 2: Phase 6b test-pre-merge 用 -d 而非 -D

test-pre-merge 分支有未合并的 merge commit（从 fix 过来的 sync merge），git branch -d 拒绝删除。

修复：Phase 6b 中 test-pre-merge 删除改用 git branch -D。

## 验收
- --raw-key 正常收口不报 unbound variable
- test-pre-merge 分支自动删除成功
