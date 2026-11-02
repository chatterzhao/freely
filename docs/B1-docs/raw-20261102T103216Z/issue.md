---
schema_version: '1'
local_id: raw-20261102T103216Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261102T103216Z-A
platform_ids:
  github:
    issue_id: '4119'
    url: https://github.com/chatterzhao/freely/issues/4119
    synced_at: ''
  gitee:
    issue_id: IKSE3I
    url: https://gitee.com/zhaoquan/freely/issues/IKSE3I
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-02T10:32:17Z'
updated_at: '2026-11-02T10:48:05Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-02T10:47:58Z'
closeout_note: ''
---

# [RAW-20261102T103216Z] fix: pre-push 在 ps 不可用时误拦 wt-close 的远程分支删除

workflow_kind: fix

## 现象
raw-20261101T140415Z 收口时，wt-close 删除 GitHub/Gitee 远程分支均失败，hook 输出 [HOOK] 远程分支删除被拦截。

## 根因
.githooks/pre-push.sh 用 ps -o args= 遍历父进程识别 wt-close；本机沙箱禁止 ps（/bin/ps: Operation not permitted），识别失败即 fail-closed，连 wt-close 自己也被拦。

## 影响
每次 wt-close 都遗留远程分支；PR 关闭但分支残留，fleet 状态与平台不一致。

## 修复方案
wt-close 在调用 git push --delete 前设置显式标记（如 FREELY_ALLOW_REMOTE_BRANCH_DELETE=1），hook 仅在该标记存在时放行；直接 push --delete 仍拦截。

## 验收
1. wt-close 能删除双平台远程分支。
2. 裸 git push --delete 仍被 hook 拦截。
