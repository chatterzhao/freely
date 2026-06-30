---
local_id: raw-20260630T134353Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260630T134353Z-A
platform_ids:
  github:
    issue_id: '3659'
    url: https://github.com/chatterzhao/freely/issues/3659
    synced_at: ''
  gitee:
    issue_id: IJXXLQ
    url: https://gitee.com/zhaoquan/freely/issues/IJXXLQ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T13:44:15Z'
updated_at: '2026-06-30T13:44:15Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 改动

### 1. --auto 标志
- `freely init --auto` 跳过 ACP 工具下载的交互式确认
- 所有工具自动下载（静默），方便 AI agent 调用
- 不带 --auto 则保持交互式确认

### 2. 已有路径跳过
- 先查 config.toml 的 FREELY_ACP_<TOOL>_BIN
- 已有且可执行 → 跳过搜索和下载
- 没有 → 搜系统 → 找到则静默写 config.toml
- 仍未找到 → 交互确认（或 --auto 下自动下载）

### 3. freely init --help 更新
- 说明 --auto 的作用
- 说明 ACP 工具准备步骤（搜索 → 写入 config.toml → 下载）
