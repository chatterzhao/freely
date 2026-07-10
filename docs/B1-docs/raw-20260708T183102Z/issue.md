---
local_id: raw-20260708T183102Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260708T183102Z-A
platform_ids:
  github:
    issue_id: '3824'
    url: https://github.com/chatterzhao/freely/issues/3824
    synced_at: ''
  gitee:
    issue_id: IJZRZJ
    url: https://gitee.com/zhaoquan/freely/issues/IJZRZJ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-08T18:31:24Z'
updated_at: '2026-07-08T18:31:24Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

\n\n## 问题

### Bug 1: _sync_issues_changed_in_merge 读文件路径错
pr-merge-guarded 第 459 行: local issues_dir="$PWD/docs/B1-docs" — 从 develop 读。但 merge 前 issue.md 只在 fix worktree 上存在（B1 阶段创建），develop 上没这个文件 → [[ -f ]] 失败 → continue 跳过 → issue-sync 静默不执行。

### Bug 2: worktree 解析脆弱
pr-merge-guarded 第 456 行: awk ... index($2, br) | head -1 — 分支名字串匹配，不用 raw_key 精确定位。git worktree list 排序不可靠。

### Bug 3: wt-close issue-sync 冗余写入
wt-close 第 733 行在正常流程下重复执行 issue-sync close。pr-merge-guarded 已经关了平台 issue 并写了 platform_state: closed。wt-close 再写一次 → 可能产生 diff → 阻塞。

### Bug 4: wt-close 遇到 diff 时引导 --force 丢弃
当 diff 是 issue-sync 写入的有价值状态（platform_state: closed）时，不应该建议 force 丢弃。应该提示 stash → wt-close → 正规化流程。

### Bug 5: wt-close 第 752 行 updated_at 时间戳
_fm_set_str "$_wt_i_file" "updated_at" "$(date ...)" — 跟 PR #3817 同款 bug。每次写入都产生 diff。

## 修复

1. pr-merge-guarded _sync_issues_changed_in_merge: 从 $_wt_path 读文件
2. pr-merge-guarded worktree 解析改用 raw_key
3. wt-close 正常路径检测 platform_state: closed 已存在 → 跳过
4. wt-close 正常路径缺失 platform_state → 提示 stash→close→正规化
5. wt-close 去掉 updated_at 时间戳写入
