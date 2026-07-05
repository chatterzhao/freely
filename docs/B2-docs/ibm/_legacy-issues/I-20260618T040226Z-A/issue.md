---
local_id: I-20260618T040226Z-A
kind: linked
status: in_dev
phase_state: completed
promoted_from: raw-20260618T040226Z
source_candidate: docs/B1-docs/raw-20260618T040226Z/candidates.md
canonical_issue_path: ""
platform_ids: {}
primary_platform: ""
created_at: 2026-06-18T04:02:26Z
author: zhaoquan
channel: freely-feat-execution
session_refs: []
pre_tests_path: docs/epics/pr-review-guarded/verification/pre-tests.md
verification_artifact_dir: docs/epics/pr-review-guarded/code-reviews
---

# I-20260618T040226Z-A: pr-review-guarded command

## 实现范围

### 新增
1. `bin/pr-review-guarded` + 真源脚本
2. review 文档格式 `pr-review-{PR#}.md`

### 流程链路更新（8 个 skill）
3-10. feat/fix/dev-loop/B1/B2 skill 全链路声明

### 脚本修改
11. wt-create 下一步提示
12. pr-create-guarded 成功提示
13. pr-merge-guarded review verdict 前置检查
14. governance-merge-gate review 文档检查

### 文档
15. AGENTS.md
16. ibm-framework.md

### Hook
17. pre-push hook 提示
