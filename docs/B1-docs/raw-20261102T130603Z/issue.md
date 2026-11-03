---
schema_version: '1'
local_id: raw-20261102T130603Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261102T130603Z-A
platform_ids:
  github:
    issue_id: '4125'
    url: https://github.com/chatterzhao/freely/issues/4125
    synced_at: ''
  gitee:
    issue_id: IKSF6N
    url: https://gitee.com/zhaoquan/freely/issues/IKSF6N
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-02T13:06:03Z'
updated_at: '2026-11-02T13:06:08Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-03T06:25:00Z'
closeout_note: ''
---
# fix: 平台 handler 探活依赖网络且无 None 守卫，导致 PR 入口抛 AttributeError


workflow_kind: fix

## 现象

PR 创建/更新入口在推送 review 提交时报：

    AttributeError: 'NoneType' object has no attribute 'push_branch'
    ERROR: guarded PR update did not complete on every configured platform.

重跑一次即成功。同一提交、同一网络配置、同一分支。

## 根因

1. `_handler_for(platform)` 每次调用都执行 `h.detect()`，而 GitHubHandler.detect() 跑的是 `gh repo view --json nameWithOwner`——一次**网络**调用（本机实测约 1.1s，代理抖动时 3/10 失败）。
2. detect 失败即返回 None。`guarded_pr_update` 在 plan 阶段已经用同一函数选出过平台，执行阶段再取一次；这次抖动就直接调用 `handler.push_branch(...)`，异常没有被转成结构化失败。

## 影响

- 每次 PR 创建/更新都可能随机失败，且错误是 Python 栈而不是可执行的恢复指引。
- 一次 PR 流程里 `_handler_for` 被调用多次，每次多付约 1.1s，纯浪费。

## 方案

1. 探活结果进程内记忆：仅在首次成功时缓存 True；失败不缓存（下次仍可恢复）。同进程内后续调用零网络开销。
2. 探活本身走 `_retry_read`（已有 3 次有界重试），避免单次抖动把平台判成不存在。
3. 执行阶段对 `handler is None` 结构化失败（`{'status':'error','stage':'execute','error':'platform handler unavailable'}`），不抛 AttributeError。
4. 不改 `configured_platforms()` 语义，不改平台注册表。

## 验收

1. 同一进程内连续 10 次取 github handler，只触发 1 次 detect。
2. 第一次 detect 抛错、第二次成功时仍返回 handler（重试生效）。
3. handler 不可用时返回结构化 error，不抛异常。
4. 既有 PR / adapter 相关测试全绿。
