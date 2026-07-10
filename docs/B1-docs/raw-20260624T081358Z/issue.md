---
local_id: raw-20260624T081358Z58Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T081358Z-A
platform_ids:
  github:
    issue_id: '3411'
    url: https://github.com/chatterzhao/freely/issues/3411
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T08:14:25Z'
updated_at: '2026-06-24T08:14:25Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 问题
freely-fix-execution、freely-test-execution、freely-feat-execution 和 AGENTS.md 中，测试步骤写成了 "stop/start daemon → 验证"，假设所有项目都是 daemon 型应用。

Freely 面向任意类型项目（CLI 工具、库、配置项目等），测试方式应由 pre-tests.md 定义，不能由 skill 文档硬编码。

## 要改的位置
- freely-fix-execution/SKILL.md: L56, L119, L141 — "stop/start daemon" 
- freely-test-execution/SKILL.md: L31, L37, L65-70 — "启动 daemon" 步骤
- freely-feat-execution/SKILL.md: L82 — "启动项目测试"
- AGENTS.md: L103 — test-pre-merge 验证描述

## 修复原则
- 测试方式由 pre-tests.md 中的 test_command 和 target_environment 决定
- skill 文档只描述流程（"按 pre-tests.md 执行验证"），不硬编码验证手段
- 正确委托链：B2_IBM 写 pre-tests.md → dev-loop RED-GREEN → test-execution 逐条执行
