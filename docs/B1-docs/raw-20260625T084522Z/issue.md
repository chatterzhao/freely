---
local_id: raw-20260625T084522Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3495'
    url: https://github.com/chatterzhao/freely/issues/3495
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T08:45:41Z'
updated_at: '2026-06-25T08:45:41Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T084522Z-A
source_candidate: docs/B1-docs/raw-20260625T084522Z/candidates.md#C-20260625T084522Z-A
promoted_issue_path: docs/issues/I-20260625T084522Z-A/issue.md
pre_tests_path: docs/epics/test-exec-anti-ghost-pass/verification/pre-tests.md
---

## 问题

test-execution skill 当前只管执行 test_command、填 actual_output。但如果 pre-tests.md 本身是糊弄的（test_command 为空或 echo pass），它照跑不误。

## 应加强

执行前增加检查步骤：
1. 检查 test_command 是否真实可执行（不是 echo pass 等占位符）
2. 检查 expected_output 是否具体（不是任意输出）
3. 检查 evidence_level 是否与改动匹配
4. 如果检查不通过，**拒绝执行**，告诉用户回 B2_IBM 重新设计

## 改动

freely-test-execution SKILL.md
