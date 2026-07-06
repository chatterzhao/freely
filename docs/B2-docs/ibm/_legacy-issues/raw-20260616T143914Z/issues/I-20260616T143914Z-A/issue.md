---
local_id: I-20260616T143914Z-A
kind: linked
phase_state: completed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260616T143914Z/code-reviews
source_candidate: docs/B1-docs/raw-20260616T143914Z14Z/candidates.md#C-20260616T143914Z-A
platform_ids: {}
primary_platform: github
canonical_issue_path: docs/B1-docs/raw-20260616T143914Z14Z/candidates.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-16T14:39:14Z'
updated_at: '2026-06-16T14:39:14Z'
intake_id: ''
author: zhaoquan
channel: claude
session_refs: []
source_raw: raw-20260616T143914Z14Z
candidate_id: C-20260616T143914Z-A
milestone_id: M-20260616T143914Z-A
---

# I-20260616T143914Z-A: 规范流程文档治理

## Map

### PRD
在 AGENTS.md.example、CONSTITUTION.md、5 个 skill SKILL.md 中补齐完整规范流程，统一"当前处于流程什么位置"标记。

### Pre-tests
- [ ] `freely init` 后 AGENTS.md 包含完整流程章节
- [ ] 每个 skill SKILL.md 头部有位置标记，格式一致
- [ ] CONSTITUTION.md 分支规范处引用完整链路

### Tasks
1. 编辑 `AGENTS.md.example`：新增 "规范流程" 章节
2. 编辑 `freely-feat-execution/SKILL.md`：补 feedback 入口 + 位置标记
3. 编辑 `freely-fix-execution/SKILL.md`：补位置标记
4. 编辑 `freely-doc-B1_IBM-execution/SKILL.md`：补位置标记
5. 编辑 `freely-doc-B2_IBM-execution/SKILL.md`：补位置标记
6. 编辑 `freely-dev-loop-execution/SKILL.md`：补位置标记
7. 编辑 `CONSTITUTION.md`：分支规范处补完整链路引用
8. 编辑 `three-loop-capability-lifecycle.md`：加 AGENTS.md 交叉引用

### Code-review
- 所有位置标记格式一致
- AGENTS.md.example 流程章节覆盖三种变体 + 命令/skill + loop
- 无拼写/格式错误
