---
local_id: raw-20260630T095936Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3649'
    url: https://github.com/chatterzhao/freely/issues/3649
    synced_at: ''
  gitee:
    issue_id: IJXWE5
    url: https://gitee.com/zhaoquan/freely/issues/IJXWE5
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T09:59:56Z'
updated_at: '2026-06-30T09:59:56Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

当前 dev↔test consistency check 在两处（worktree-common.sh + wt-close）提示用户用 cherry-pick 同步，但：

1. **dev→test 方向**: cherry-pick 被 reference-transaction hook 阻止（test-pre-merge-* 是保护分支，只接受带 Freely-Merge-Path 的 merge commit）。提示不可执行，形成死锁。

2. **test→dev 方向**: 提示用户 cherry-pick 测试工位提交回开发工位。但 test-pre-merge 是丢弃式沙箱，不应有独立提交。正确做法是拒绝此方向，要求用户在开发工位提交，再 merge 到测试工位。

## 改动范围

### worktree-common.sh freely_wt_assert_dev_test_consistent()
- Check 1 (test→dev, L244-267): cherry-pick 提示 → 硬拒绝 + 正确做法指引
- Check 2 (dev→test, L269-294): cherry-pick 提示 → git merge 命令（含 Freely-Merge-Path receipt）

### wt-close _consistency_check()
- Check 2 (dirty test, L518-536): commit test results → 硬拒绝 + 正确做法
- Check 3 (test→dev, L538-561): cherry-pick 提示 → 硬拒绝（同 worktree-common）
- Check 4 (dev→test, L563-588): cherry-pick 提示 → git merge 命令

## 验收标准
- dev→test 不一致时提示用 git merge --no-ff + Freely-Merge-Path: pr-merge-guarded
- test→dev 不一致时硬拦截，提示正确流程：stash test 修改 → commit in dev → merge dev to test → 重测
- test 工位有未提交修改时硬拦截，不允许提交到测试工位
- pr-create-guarded / pr-merge-guarded / pr-review-guarded / wt-close 四处的提示一致
