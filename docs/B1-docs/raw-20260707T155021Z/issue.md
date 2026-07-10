---
local_id: raw-20260707T155021Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260707T155021Z-A
platform_ids:
  github:
    issue_id: '3811'
    url: https://github.com/chatterzhao/freely/issues/3811
    synced_at: ''
  gitee:
    issue_id: IJZHLZ
    url: https://gitee.com/zhaoquan/freely/issues/IJZHLZ
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-07T15:50:43Z'
updated_at: '2026-07-07T15:50:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题

当前 review-guidelines 侧重于文档完整性检查。b2/red/dev/green 阶段的审查没有强制要求测试验证**行为正确性**（而不是代码存在性）。

11 个 PR 中没有一个行为测试——全是 grep -c + bash -n。bug 穿透了所有审查层。

## 修复

在 b2/red/dev/green 的审查指南中增加强制行为测试检查：
- B2: test_command 必须可执行且验证行为
- RED: actual_RED_output 必须是真实执行结果
- dev: 代码必须修复 RED 发现的失败
- GREEN: 禁止 ghost pass，测试必须验证行为正确性

## 原则

grep -c + bash -n 不是测试——是走过场。行为测试才是真正的测试。
