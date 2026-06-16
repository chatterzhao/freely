---
local_id: raw-20260521T222919Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2097'
    url: https://github.com/chatterzhao/freely/issues/2097
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-21T22:29:31Z'
updated_at: '2026-05-22T09:18:36Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-22T09:18:36Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## 根因

scan 脚本 (task-lifecycle-scan.py) 使用 CHAIN_STATIONS 体系（18个站）产出 stage 名，如 `raw_created`, `b1_dir`, `platform_create`, `i_created` 等。

prompt builder (freely:15147) 使用旧的 B1/B2 体系，for 循环只匹配 `B1_proposed`, `B2_active` 等 14 个旧名。

两套命名系统零交集。scan 产出的 619 条数据在 for 循环中被全部跳过，Manager prompt 中 scan section 展示 0 条 item。Manager 看到空 scan → stop_ai。

## 需要改的地方

### 1. freely:15113-15129 — stage_labels 字典
将所有 CHAIN_STATIONS 的 stage 名加入，并配中文标签。

### 2. freely:15147 — for stage in 列表
替换为 CHAIN_STATIONS 的完整 stage 列表。

### 3. freely:15142-15143 — 提示词说明
更新"原则"文本，反映新的 station 模型。

### 4. task-lifecycle-scan.py:817-836 — CHAIN_STATIONS
确认 CHAIN_STATIONS 是 stage 名唯一真源，如有缺失补充。

### 5. test 文件
检查 test-freely-task-source-scan 等测试是否有 stage 名断言需更新。
