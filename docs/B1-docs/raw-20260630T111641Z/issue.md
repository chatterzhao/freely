---
local_id: raw-20260630T111641Z41Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260630T111641Z-A
platform_ids:
  github:
    issue_id: '3653'
    url: https://github.com/chatterzhao/freely/issues/3653
    synced_at: ''
  gitee:
    issue_id: IJXWVY
    url: https://gitee.com/zhaoquan/freely/issues/IJXWVY
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T11:17:03Z'
updated_at: '2026-06-30T11:17:03Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

wt-close 在 line 762-764 直接修改 dev 工位的 raw issue 文件（写 platform_state=closed），但不提交。如果 wt-close 后续步骤失败，文件保持脏状态，阻塞后续重试。

## 根因

状态更新放错了位置：
- wt-close 是收口清理命令，不应修改即将删除的工位文件
- pr-review-guarded 是 review 通过后的最后一道提交工序，应该在这里完成状态更新

## 改动

### pr-review-guarded
- review verdict=pass 后，更新 raw issue 的 phase_state=completed + platform_state（或由 I-* issue 承担）
- commit + push，走正常 merge 链路进入 develop

### wt-close
- 删除 line 762-764 的 `_fm_set_str` 本地文件写入
- 只做清理：关平台 issue（API）→ 删远程分支 → 删 worktree → 删本地分支

## 验收标准
- pr-review-guarded 在 review 通过后完成状态写入
- wt-close 不再产生未提交的文件修改
- wt-close 不再因自己的修改触发 consistency check 脏文件拦截
