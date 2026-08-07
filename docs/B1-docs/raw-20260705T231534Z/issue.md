---
local_id: raw-20260705T231534Z
kind: raw
phase_state: dropped
platform_ids:
  github:
    issue_id: '3758'
    url: https://github.com/chatterzhao/freely/issues/3758
    synced_at: ''
  gitee:
    issue_id: IJYVW9
    url: https://gitee.com/zhaoquan/freely/issues/IJYVW9
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-05T23:15:55Z'
updated_at: '2026-07-05T23:15:55Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题

项目已支持安装 freely 后直接使用 `freely xxx` 命令，但文档、skill、hook 脚本、错误提示等仍大量使用 `./bin/freely xxx` 或 `./bin/xxx` 的旧格式。

## 范围

- hooks: pre-commit.sh (8处), pre-merge-commit.sh (7处), pre-push.sh (3处)
- skills: ~10 个 skill 文件
- 文档: LAWS.md, milestones.md, skills/README.md 等

## 规则

- 用户可见的文档/提示 → `freely xxx`
- hook 脚本内部执行 → `freely xxx`（依赖 PATH 中有 freely）或保留绝对路径
- 脚本内部 source/引用 → 按实际情况处理
