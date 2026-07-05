---
local_id: raw-20260508T005431Z
kind: raw
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '251'
    url: https://github.com/chatterzhao/freely/issues/251
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-08T00:54:56Z'
intake_id: ''
author: platform
channel: github
session_refs: []
pre_tests_path: docs/epics/skill-standardize/verification/pre-tests.md
verification_artifact_dir: docs/epics/skill-standardize/code-reviews
platform_state: closed
---

- pre_tests_path: docs/epics/skill-standardize/verification/pre-tests.md
- verification_artifact_dir: docs/epics/skill-standardize/code-reviews

## 问题

docs/system/workspace/skills/ 下 33 个 skill 已部署到 ~/.claude/skills/。三个问题:

1. 改 skill 后不自动部署
2. 项目文件引用 skill 用路径而非名称
3. skill 内部互相引用用绝对路径

## 修复

- 新增 bin/deploy-skills 增量部署脚本
- AGENTS.md 新增 Skill 管理节
- chat-issue-routing 补 frontmatter
- continuity-watchdog 改为相对路径
