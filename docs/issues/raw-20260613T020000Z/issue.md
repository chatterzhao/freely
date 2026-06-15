---
local_id: raw-20260613T020000Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2578'
    url: https://github.com/chatterzhao/freely/pull/2578
primary_platform: github
canonical_issue_path: ''
created_at: '2026-06-13T02:00:00Z'
platform_state: closed
updated_at: '2026-06-15T04:39:35Z'
---

pr-create-guarded 和 pr-merge-guarded 硬编码 GitHub，不支持多平台配置。
多平台项目 merge 后 develop 只在单一 remote 同步，跨平台 PR 存在串平台风险。

absorbed_into: I-20260612T140944Z-A
