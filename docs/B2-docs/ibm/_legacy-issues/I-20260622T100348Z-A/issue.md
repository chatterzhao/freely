---
local_id: I-20260622T100348Z-A
kind: I
phase_state: completed
source_candidate: docs/B1-docs/raw-20260622T100348Z48Z/candidates.md#C-20260622T100348Z-A
verification_artifact_dir: docs/B2-docs/I-20260622T100348Z-A/code-reviews
raw_refs:
  - raw-20260622T100348Z48Z
candidate_refs:
  - C-20260622T100348Z-A
created_at: '2026-06-22T10:04:05Z'
updated_at: '2026-06-22T10:04:05Z'
---

# I-20260622T100348Z-A: --reason Documentation in All Command --help

## Summary

为所有带 bypass 门禁的命令完善 --help 输出，让用户无需触发 GATE 就能了解：
- 何时需要 --reason（与 --force/--skip/--discard/--verdict 配合使用）
- --reason 的精确格式: `--reason "违规绕过门禁中，理由充分，是：<业务理由>"`
- 有效业务理由 vs 无效技术症状的区分

## Changes

- **freely usage()**: 为 init/start/daemon/task-mode/wt-close 添加 `[--reason <text>]`
  新增 "Bypass gates" 独立章节，含格式说明和有效/无效示例
- **wt-close usage()**: 每个 bypass flag 的有效理由类型，正确示例
- **pr-review-guarded --help**: 详细选项说明、--reason gate 触发条件、示例

## Acceptance Criteria
- [x] freely --help 显示所有 --force 命令的 --reason 参数
- [x] freely --help 显示 "Bypass gates" 章节含格式和示例
- [x] wt-close --help 显示 --reason 格式要求和 per-flag 有效理由
- [x] pr-review-guarded --help 显示 --reason gate 触发条件和示例
