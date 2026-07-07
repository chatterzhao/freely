---
local_id: raw-20260707T064609Z
kind: raw
phase_state: absorbed
absorbed_into: 'I-20260707T064609Z-A'
platform_ids:
  github:
    issue_id: '3797'
    url: https://github.com/chatterzhao/freely/issues/3797
    synced_at: ''
  gitee:
    issue_id: IJZD65
    url: https://gitee.com/zhaoquan/freely/issues/IJZD65
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-07T06:46:30Z'
updated_at: '2026-07-07T06:46:30Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

commands.md（PR #3789）作为封装命令权威参考，但与源码实际支持的选项/子命令有差距：

| 命令 | 遗漏 |
|------|------|
| feedback | edit 子命令、--severity |
| wt-create | --base、--skill、legacy 接口 |
| pr-create-guarded | --title、--body、--base |
| pr-review-guarded | --reviewer、--slot、--verdict、--reason |
| pr-merge-guarded | complete 子命令、--dry-run |
| wt-close | --force、--discard-unmerged、--platform-only、--skip-platform、--dry-run、--reason |
| develop-push | status、defer、clear 子命令 |
| issue-sync | 整条命令未收录 |
| deploy-skills | 整条命令未收录 |

## 修复

以源码 help/usage 为准，逐条对齐 commands.md 中每个命令的语法、选项、子命令、场景说明。
AGENTS.md 速查表不需要改动——它只需最常见的场景即可，细节在 commands.md。

## 原则

- 以源码为准，不以现有文档为准
- commands.md 是唯一权威参考——AGENTS.md、SKILL.md、hook 消息引用它
- 每个命令说清楚所有支持的选项和子命令
