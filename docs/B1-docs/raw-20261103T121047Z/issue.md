---
schema_version: '1'
local_id: raw-20261103T121047Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T121047Z-A
platform_ids:
  github:
    issue_id: '4142'
    url: https://github.com/chatterzhao/freely/issues/4142
    synced_at: ''
  gitee:
    issue_id: IKSPBS
    url: https://gitee.com/zhaoquan/freely/issues/IKSPBS
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-03T12:10:47Z'
updated_at: '2026-11-03T12:25:49Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-03T12:30:00Z'
closeout_note: ''
---
# pr-merge-guarded 批量 issue-sync 误关闭非本 lane open issue


workflow_kind: fix

## 严重度
P0：一次 docs-only 合并把 13 个真实 open issue 在 GitHub（及 6 个在 Gitee）全部关闭，随后必须手工重开。

## 复现
1. open issue 集合：GitHub/Gitee 各 13。
2. 合并只改 docs/B1-docs 的 lane（如 raw-20261103T111400Z：物化 13 个 open raw 文档 + 回填 15 个历史文档编号）。
3. pr-merge-guarded 在 merge 前调用 _sync_issues_changed_in_merge：它用 git diff develop..src -- docs/B1-docs/**/issue.md 取**所有**变化的 issue.md；对每个 raw/proposed 文档执行 _update_issue_phase absorbed + issue-sync close。
4. 结果：13 个不属于本 lane 的 open raw issue 被误判为 absorbed 并在两平台关闭（日志 [MERGE-GUARD] synced 29 issue(s) to platforms）。

## 根因
pr-merge-guarded _sync_issues_changed_in_merge 未按分支 raw key 过滤 diff 中的 raw 文档；把治理数据变更（物化/回填）当成生命周期推进。

## 修复方向
1. 只同步 local_id 含分支 raw key 的 issue（raw-<key>、I-<key>-*）；其余 changed raw docs 一律不动。
2. 分支名无 raw key 时保持旧行为（兼容）。
3. 回归测试：多 raw 文档 diff + 指定 raw key → 只过滤出本 key；无 key → 不过滤。
4. 同时修 gitee-issue.py reopen：复用 close 的 repo_path_post + repo body 模式（当前 reopen 用 repo_path 导致 Gitee 404）。

## 验收
- 单测：scope 过滤函数；reopen 请求构造函数。
- 事故复盘：重开 13+6 个 issue 后 open 集合恢复 13=13（已人工恢复）。
- 不改变正常 lane（只改自己 raw issue）的收口行为。
