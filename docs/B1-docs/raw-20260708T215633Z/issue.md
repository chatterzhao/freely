---
local_id: raw-20260708T215633Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3833'
    url: https://github.com/chatterzhao/freely/issues/3833
    synced_at: ''
  gitee:
    issue_id: IJZS1G
    url: https://gitee.com/zhaoquan/freely/issues/IJZS1G
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-08T21:56:54Z'
updated_at: '2026-07-08T21:56:54Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

### 1. 硬编码平台名
scan 中多处硬编码 "github"/"gitee"，应该从 config.toml FREELY_REPO_PLATFORMS 读取：
- L296: "platforms": ["github", "gitee"] → _detect_platforms()
- L436: return ["github"] → 读 config
- L476: if "github" in platforms → 遍历所有平台
- L368: extract_github_id() → extract_platform_ids()

### 2. 只查 GitHub 状态
get_all_platform_issue_states 只查 GitHub CLOSED。Gitee 状态不查。issue.md 的 platform_ids 有 github 和 gitee 两个 ID，但 scan 只用 github_id 比对。

### 3. 跨平台不同步
当 GitHub=CLOSED、Gitee=OPEN 时，本地 platform_state 只有一个值。scan 应该逐平台比对，发现不一致时直接用 platform-adapter API 同步——**不需要开工位**。

### 4. platform_state 字段语义不清
issue.md 的 platform_state 是单值，但实际有两个平台各有一个状态。应该改为逐平台读取和比对。

## 修复

1. 所有平台名从 config.toml / _detect_platforms() 动态获取，不硬编码
2. 用 platform_ids dict 逐平台查状态（platform-adapter 现有 API）
3. 跨平台不一致 → 纯 API 同步，不创建 worktree
4. scan output 增加 per_platform 字段，列出每个平台的实际状态

## 原则
- 平台间同步用 API，不改本地文件 → 不需要 worktree
- 本地文件需要修改 → 才走 worktree 流程
- 所有平台列表从 config 动态读，支持未来加新平台
