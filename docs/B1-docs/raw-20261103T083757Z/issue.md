---
schema_version: '1'
local_id: raw-20261103T083757Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4137'
    url: https://github.com/chatterzhao/freely/issues/4137
    synced_at: ''
  gitee:
    issue_id: IKSN3S
    url: https://gitee.com/zhaoquan/freely/issues/IKSN3S
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-03T08:37:58Z'
updated_at: '2026-11-03T08:38:02Z'
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

## 现象
清理远程分支时调用 `python3 docs/system/workspace/scripts/runtime/gitee-issue.py delete-branch <branch>`，四个分支全部返回：

    DELETE /repos/zhaoquan/freely/git/refs/heads/<branch> failed: HTTP 404: {"status":"404","error":"Not Found"}

而分支在 Gitee 上实际存在。改用 `git push origin --delete` 可正常删除。

## 根因
`repo_path_branch()` 构造的是 GitHub 风格路径 `/repos/{owner}/{repo}/git/refs/heads/{branch}`；Gitee API v5 删除分支的 canonical 端点是 `DELETE /repos/{owner}/{repo}/branches/{branch}`。

## 影响
- `wt-close` Phase 4 对 gitee remote 会先走该 API，失败后才 fallback 到 `FREELY_ALLOW_REMOTE_BRANCH_DELETE=1 git push --delete`；功能可恢复但每次多一次失败请求与告警，且让人误以为删除没执行。
- 该 fallback 正是本次 4 个 Gitee 遗留分支删除的实际路径。

## 修复方向
1. `repo_path_branch` 改为 `/repos/{owner}/{repo}/branches/{branch}`（DELETE）。
2. 补一个 wrapper 单测/沙箱验证：分支存在时 DELETE 返回 204/200，分支不存在时 404 语义化。
3. wt-close 的 fallback 保留，但 API 成功路径应成为主路径。

## 发现场景
2026-11-03 清理 2026-06/07 遗留 Gitee 远程分支时复现（4/4 分支均 404，fallback 成功）。
