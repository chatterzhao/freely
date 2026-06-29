---
local_id: raw-20260507T143544Z
kind: raw
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: '2026-06-29T13:39:27Z'
platform_ids:
  github:
    issue_id: '247'
    url: https://github.com/chatterzhao/freely/issues/247
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-07T14:36:17Z'
intake_id: ''
author: platform
channel: github
session_refs: []
pre_tests_path: docs/epics/raw-issue-pull-intercept/verification/pre-tests.md
verification_artifact_dir: docs/epics/raw-issue-pull-intercept/code-reviews
source_candidate: docs/pre-brainstorms/20260507T143544Z--intercept-guard/candidates.md
platform_state: closed
---

- pre_tests_path: `docs/epics/raw-issue-pull-intercept/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/raw-issue-pull-intercept/code-reviews`

## 问题

`bin/raw-issue-pull` 目前有 3 个缺陷：

### 1. 缺少工位/分支名拦截
当前从 `develop` 等受保护分支直接调用 `freely raw-issue-pull --raw-key xxx` 可以成功拉取任意 issue，没有任何校验当前分支或工位名是否包含该 raw-key。设计意图是：**只能在包含该 raw-key 的工位/分支中 pull 自己的 issue**。

### 2. `bin/freely raw-issue-pull` CLI dispatch 缺失
在 `docs/system/workspace/scripts/runtime/freely` 的 help 文本（line 555）中列出了该命令，但 dispatch case 语句中没有对应分支，调用返回 "unknown command"。

### 3. `platform-adapter.py` 中无调用者身份校验
`pull_raw_issue()` 直接搜索平台 issue 并写入文件系统，未校验调用上下文。

## 修复方案

1. 在 `bin/raw-issue-pull` 中加入前置校验：`git branch --show-current` 必须包含 `raw_key`
2. 在 `freely` runtime 中补充 dispatch 逻辑
3. 如果当前分支是受保护分支（develop/main/test-pre-merge-*），拒绝执行

## 涉及文件
- `bin/raw-issue-pull`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/sync/platform-adapter.py`
