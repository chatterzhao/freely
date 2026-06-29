---
local_id: raw-20260624T072546Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T072546Z-A
platform_ids:
  github:
    issue_id: '3410'
    url: https://github.com/chatterzhao/freely/issues/3410
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T07:26:03Z'
updated_at: '2026-06-29T13:40:11Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题
wt-create 和 .githooks/reference-transaction.sh 的报错信息中硬编码了 "GitHub"、"gh issue create"、"--repo <user/repo> --title ..." 等平台专属文本。

Freely 设计为平台可配置（支持 GitHub、Gitee，未来可能加 GitLab、GitCode），不同平台通过 platform-adapter 封装抹平，报错信息不应假定某个具体平台。

## 要改的位置
- .githooks/reference-transaction.sh:111 — 硬编码参数格式
- docs/system/workspace/scripts/worktree/wt-create: L12,28-29,119-120,152,158,425-428,440 — 多处 "GitHub"、"gh issue create" 等

## 修复原则
- 不提及具体平台名（GitHub/Gitee）
- 不写死命令参数格式（--repo --title --body）
- 统一指向 freely feedback --help
- 如果出错是因为没有 raw issue → 提示用 feedback 命令创建，不知道怎么用就 --help
