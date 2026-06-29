---
local_id: raw-20260629T164530Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260629T164530Z-A
platform_ids:
  github:
    issue_id: '3632'
    url: https://github.com/chatterzhao/freely/issues/3632
    synced_at: ''
  gitee:
    issue_id: IJXOMU
    url: https://gitee.com/zhaoquan/freely/issues/IJXOMU
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-29T16:45:50Z'
updated_at: '2026-06-29T16:45:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 背景

上一版 PR #3629 把 raw key 作为 positional 参数解析，与 --platform-only 等 flag 模式冲突。需要重构为 --raw-key flag，与 --branch 并列。

## 设计

### --raw-key 与 --branch 并列

    wt-close --raw-key 20260629T160852Z
    wt-close --raw-key raw-20260629T160852Z
    wt-close --raw-key fix/raw-20260629T160852Z-wt-close-raw-key-param
    wt-close --raw-key feature/raw-20260629T160852Z-my-feat
    wt-close --branch fix/raw-20260629T160852Z-my-fix

--raw-key 自动提取 raw key（兼容 raw-{key}、fix/raw-{key}-{slug}、feature/raw-{key}-{slug}），然后查找对应的 fix|feature 分支。--branch 保留原有行为。

### 与操作模式正交

    # 查分支 + 正常关闭
    wt-close --raw-key 20260629T160852Z

    # 查分支 + 强制
    wt-close --raw-key 20260629T160852Z --force --reason "..."

    # 不查分支，纯平台关闭
    wt-close --raw-key 20260629T160852Z --platform-only --reason "..."

### 修复 --platform-only 的 unbound variable bug

line 588 处 raw_key 未绑定。

### help 强调

- 明确写传 --raw-key 或 --branch，不要传 test-pre-merge
- test-pre-merge Phase 6b 自动关联

### 修复 + 前缀 bug

git branch --list 输出的 + 前缀（worktree 分支标记）需要 strip。

## 验收
- --raw-key 支持 raw-{key}、fix/raw-{key}-{slug}、feature/raw-{key}-{slug} 输入
- --branch 保留原有行为
- --raw-key + --platform-only 不走分支解析
- --raw-key + --force 正常工作
- help 明确 test-pre-merge 自动处理
