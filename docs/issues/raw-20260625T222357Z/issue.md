---
local_id: raw-20260625T222357Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3516'
    url: https://github.com/chatterzhao/freely/issues/3516
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T22:24:16Z'
updated_at: '2026-06-25T22:24:16Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T222357Z-A
source_candidate: docs/pre-brainstorms/20260625T222357Z--review-test-worktree/candidates.md#C-20260625T222357Z-A
promoted_issue_path: docs/issues/I-20260625T222357Z-A/issue.md
pre_tests_path: docs/epics/review-test-worktree/verification/pre-tests.md
---

## 设计

Review agent 进入 test-pre-merge 工位审查，不偏听 Worker。统一 fix/feature。

### 前置检查（pr-review-guarded bash 层）
1. 找 test-pre-merge 路径
2. test-pre-merge 必须 clean（脏 -> 让 Worker commit）
3. fix/feature 和 test-pre-merge 必须同步
4. 两个工位都不脏

### Review agent（ACP session，工作目录=test-pre-merge）

#### 第一层：代码质量
- git diff <fix/feature>..HEAD 只有 pre-tests.md + evidence
- test_command 没被改弱

#### 第二层：完成度
- pre-tests.md vs raw issue vs brainstorms
- 测试层级匹配改动范围
- actual_output 全 GREEN，无 ghost pass

#### 第三层：代码安全
- fix/feature 改动都在 test-pre-merge
- test-pre-merge 无多余代码
- cherry-pick 路径不丢代码

### 判定
- 全过 -> pass -> pr-merge
- 任一层 fail -> Worker 改 -> 再 Review

### 改动
- bin/pr-review-guarded: 找 test-pre-merge，检查 clean+同步
- docs/system/workspace/skills/freely-tdd-review/SKILL.md: 三层定义+pass/fail
