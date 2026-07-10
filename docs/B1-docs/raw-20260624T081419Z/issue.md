---
local_id: raw-20260624T081419Z19Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T081419Z-A
platform_ids:
  github:
    issue_id: '3412'
    url: https://github.com/chatterzhao/freely/issues/3412
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T08:14:51Z'
updated_at: '2026-06-24T08:14:51Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题
freely-fix-execution 中 test-pre-merge 到 fix 工位的修改转移方式用的是 cp 逐个文件路径。

git stash 对同一仓库的所有 worktree 可见，更原子化：一次 push 捕获全部 dirty changes（含新文件 --include-untracked），到 fix 工位 apply 取出。

## 要改的位置
- freely-fix-execution/SKILL.md: 全部 cp 引用（description、核心原则、操作表、关键说明、适用场景、阶段 2、阶段 5、硬性规则）

## 修复原则
- test 工位: git stash push --include-untracked -m "fix: <描述>"  (dirty state 进入 stash，工位自动干净)
- fix 工位: git stash apply (不用 pop，留备份) → git status 检查 → git stash drop → git add 精确文件 → git commit
- 不需要 cp 逐个文件路径，不需要手动清理 "残余 dirty"
