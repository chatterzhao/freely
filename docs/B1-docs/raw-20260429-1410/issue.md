---
local_id: raw-20260429-1410
kind: raw
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
platform_ids:
  github:
    issue_id: '276'
    url: https://github.com/chatterzhao/freely/issues/276
    synced_at: '2026-05-10T09:29:24Z'
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: 2026-04-29 14:10:06+00:00
updated_at: '2026-06-17T00:21:24Z'
intake_id: 20260429-071005-docs-system-workspace-scripts-ut
author: zhaoquan
channel: supervisor
session_refs: []
platform_state: closed
---

# 任务：检查项目大文件并重构

## 第一步：编写行数统计脚本
编写 `docs/system/workspace/scripts/util/count-lines.sh`，统计项目中所有脚本文件的行数，
按行数降序排列。重点关注：
- `docs/system/workspace/scripts/runtime/` 下的所有文件
- `docs/system/workspace/skills/` 下的所有文件
- `.githooks/` 下的所有文件

输出格式：`行数 文件路径`

## 第二步：识别需要重构的文件
- 超过 1000 行的文件标记为需要重构
- 超过 2000 行的文件标记为紧急需要重构
- 列出每个大文件的主要函数以及它们适合抽取到哪个新模块

## 第三步：执行重构
对最紧急的文件（freely 主文件，~20000行），将其 ACP 相关代码（bridge 生命周期、
liveness 检测、monitor dispatch）抽取到新模块 `docs/system/workspace/scripts/runtime/acp-lifecycle.sh`。

要求：
1. 每个重构步骤先 plan，再执行
2. 重构后确保 `bash -n` 语法检查通过
3. 保留原有所有功能，不改变行为
