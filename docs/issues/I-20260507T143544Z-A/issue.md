---
local_id: I-20260507T143544Z-A
kind: linked
status: in_dev
phase_state: in_dev
promoted_from: raw-20260507T143544Z
candidate_ref: docs/pre-brainstorms/20260507T143544Z--intercept-guard/candidates.md#c-20260507t143544z-a-raw-issue-pull-工位拦截
canonical_issue_path: docs/issues/I-20260507T143544Z-A/issue.md
platform_ids: {}
primary_platform: ""
last_synced_comment_at: {}
hash: ""
created_at: 2026-05-07T14:35:44Z
updated_at: 2026-05-07T14:35:44Z
intake_id: ""
author: zhaoquan
channel: feat-execution
session_refs: []
pre_tests_path: ""
verification_artifact_dir: ""
---

# I-20260507T143544Z-A: raw-issue-pull 工位拦截

## 实现
- `bin/raw-issue-pull`: 分支拦截 + 修复 bash bug
- `docs/system/workspace/scripts/runtime/freely`: CLI dispatch 路由

## 测试
- develop 分支拒绝执行
- 不匹配分支拒绝执行
- 匹配工位可正常 pull
