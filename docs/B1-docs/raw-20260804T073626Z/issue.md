---
schema_version: '1'
local_id: raw-20260804T073626Z
kind: raw
phase_state: absorbed
absorbed_into: 'I-20260725T030511Z-A'
platform_ids:
  github:
    issue_id: '4077'
    url: https://github.com/chatterzhao/freely/issues/4077
    synced_at: ''
  gitee:
    issue_id: IK6EKQ
    url: https://gitee.com/zhaoquan/freely/issues/IK6EKQ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-08-04T07:36:26Z'
updated_at: '2026-08-04T08:30:00Z'
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
`freely wt-create` 在 raw-issue-pull 阶段失败：`拒绝创建工位: raw-issue-pull failed`。底层 `platform-adapter.py pull` 抛 `KeyError: issue_number`（line 898 `check_and_claim_assignee(plat, info["issue_number"])`）。

## 根因
1. GitHub handler `search_raw_issue`（platform-adapter.py L233）比较时 `haystack.lower()` 转小写，但 needle `f"raw-{raw_key}"` 未转小写。raw key 固定含大写 `Z`（`20260804T073054Z`），lower 后是 `z`，永不匹配 → GitHub 侧恒返回 `{"matches": []}`。
2. 顶层 `search_raw_issue`（L679）把任意非空 dict 计入 results，`{"matches": []}` 被当作有效平台结果。
3. `pull_raw_issue`（L898）遍历 results 时直接取 `info["issue_number"]`，空 matches 条目无此键 → KeyError。
Gitee handler 无此 bug（needle 先 `.lower()`）。

## 影响
所有 `--source platform` 的 wt-create 都会失败（GitHub 侧空匹配 → KeyError），开发流程入口被阻塞。GitHub 侧 issue 匹配功能完全失效。

## 修复建议
1. GitHub `search_raw_issue`：needle 改 `f"raw-{raw_key}".lower()`。
2. 顶层 `search_raw_issue`：过滤 `{"matches": []}` 的空结果。
3. `pull_raw_issue`：对无 `issue_number` 的条目跳过并告警（防御）。
4. 修复后重跑 `wt-create --source platform` 验证。
