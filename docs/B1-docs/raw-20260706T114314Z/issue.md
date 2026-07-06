---
local_id: raw-20260706T114314Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260706T114314Z-A
platform_ids:
  github:
    issue_id: '3781'
    url: https://github.com/chatterzhao/freely/issues/3781
    synced_at: ''
  gitee:
    issue_id: IJZ6M5
    url: https://gitee.com/zhaoquan/freely/issues/IJZ6M5
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-06T11:43:40Z'
updated_at: '2026-07-06T11:43:40Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因
当前 hook 拦截时提示不够具体:
- 没有说清这个场景应该用哪个 freely 命令
- 没有列出可用命令能力
- AI agent 不知道 freely 有哪些命令,选错绕过

## 修复方案
### 1. Hook 拦截提示改造
每个拦截点必须给出精确的下一步命令:
- pre-commit block → '所有变更必须通过 freely feedback + freely wt-create 创建工位完成'
- pre-push block → 'freely pr-create-guarded 是推送唯一入口'
- gh wrapper block → 'freely pr-merge-guarded 替代 gh pr merge'
- wt-close block → 'cd test 工位 → freely daemon start → 跑测试 → freely wt-close'

### 2. freely 命令能力文档
在 AGENTS.md 或 SKILL.md 补充所有 freely 命令的用途和使用时机,
让 AI agent 清楚知道有哪些封装命令可以替代原始 git/gh 命令
