---
local_id: raw-20260628T054513Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3603'
    url: https://github.com/chatterzhao/freely/issues/3603
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-28T05:45:34Z'
updated_at: '2026-06-28T05:45:34Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 根因

checkpoint-guard 用 MAX_CHANGED_FILES=25 / MAX_SCOPE_COUNT=4 做硬阻塞。文件数不能准确反映 scope 爆炸（50 文件重命名是一个关注点，3 个不相关 fix 才是真爆炸）。阻塞时机太晚，逼迫把同一问题拆碎。

## 修复

### 1. pre-commit hook
- 移除 --fail-on-required，checkpoint-guard 只输出警告不阻塞

### 2. checkpoint-guard 输出
- 无 --fail-on-required 时退出码始终 0
- 输出引导信息：同一问题→继续提交，不同问题→拆分

### 3. AGENTS.md + AGENTS.md.example
- 添加 scope 自查说明

## 不纳入
- PR review scope（已有 pr-review-guarded）
- git add hook（git 不支持 post-add hook）
