---
local_id: I-20260617T145428Z-A
kind: linked
status: in_dev
phase_state: completed
promoted_from: raw-20260617T145428Z
source_candidate: docs/B1-docs/raw-20260617T145428Z/candidates.md
canonical_issue_path: ''
platform_ids:
  github:
    issue_id: '2945'
    url: https://github.com/chatterzhao/freely/issues/2945
    synced_at: '2026-06-17T17:08:52Z'
primary_platform: github
last_synced_comment_at: {}
hash: ''
created_at: 2026-06-17 14:54:28+00:00
updated_at: '2026-06-17T17:08:52Z'
intake_id: ''
author: zhaoquan
channel: freely-fix-execution
session_refs: []
pre_tests_path: docs/B2-docs/freely-db-cli-agents-fix/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/freely-db-cli-agents-fix/code-reviews
platform_state: closed
---

# I-20260617T145428Z-A: Fix freely-db-cli syntax + AGENTS.md flow + hook skill routing

- source_candidate: `docs/B1-docs/raw-20260617T145428Z/candidates.md`
- pre_tests_path: `docs/B2-docs/freely-db-cli-agents-fix/verification/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/freely-db-cli-agents-fix/code-reviews`

## 实现

### freely-db-cli syntax fix
`docs/system/workspace/scripts/runtime/freely-db-cli` 第 282 行 `_task_update_params` 函数：补回缺失的 `for k in (` 前缀。

### AGENTS.md workflow fix
重构"核心开发流程"部分：入口改为"或"关系的分支（feedback / scan），feedback 显式列为入口。与 `skill:freely-feat-execution` 的链路定义一致。

### pre-commit hook message fix
`docs/system/workspace/hooks/pre-commit.sh` 的 develop 拦截消息：指向 `skill:freely-fix-execution` / `skill:freely-feat-execution`，增加反绕过警告（CONSTITUTION.md §5）。

### 提交
- `f6cfb9ca`: freely-db-cli + AGENTS.md
- `b29e3e1c`: pre-commit hook message
- `99429c31`: B1_IBM governance
