---
local_id: raw-20260625T030147Z47Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3464'
    url: https://github.com/chatterzhao/freely/issues/3464
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T03:01:47Z'
updated_at: '2026-06-25T04:25:36Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T030147Z-A
source_candidate: docs/B1-docs/raw-20260625T030147Z47Z/candidates.md#C-20260625T030147Z-A
---

## 问题

FREELY_REPO_PLATFORMS 目前手工维护，不科学。

## 设计

freely start 时：
1. 扫描 .git/config 所有 remote URL
2. 识别平台（github.com → github, gitee.com → gitee）
3. 更新 .freely/config.toml 的 FREELY_REPO_PLATFORMS
4. 注释标明此字段由 start 自动维护，勿手工编辑

## 影响

所有用 FREELY_REPO_PLATFORMS 的地方（feedback, pr-create, pr-merge, issue-sync）都不再需要自己扫描 git remote，统一读 config 即可。单点维护。

## 改动

- freely runtime: start 命令加入平台检测逻辑
- .freely/config.toml.example: 更新注释
