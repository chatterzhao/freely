---
local_id: raw-20260708T122837Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3820'
    url: https://github.com/chatterzhao/freely/issues/3820
    synced_at: ''
  gitee:
    issue_id: IJZR5X
    url: https://gitee.com/zhaoquan/freely/issues/IJZR5X
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-08T12:28:59Z'
updated_at: '2026-07-08T12:28:59Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

lifecycle-v3 简化了分类但丢弃了旧 scan 的核心能力：

1. **无 batch 聚合**：271 条独立项直接注入 prompt，Manager 无法处理
2. **无 stage 分级**：所有项混在 2a_non_terminal，不区分 close_platform / B1_proposed / B2_done
3. **无 derive_action**：无具体 next_action 推导，AI 不知道第一步做什么

## 修复

恢复旧 scan (bak.py) 的：
- add_platform_sync_batch：平台同步项聚合为一条 batch
- stage 分级：close_platform / close_local / B1_proposed / B2_active / 收口
- _derive_action：根据 stage + incomplete 推导具体操作

保留新 scan 的改进：
- argparse --project
- platform-adapter 集成
- extract_platform_ids 多平台支持

## 目标

scan 输出的每一条 item，Manager 都知道具体做什么
