---
candidate_id: C-20260629T160852Z-A
status: promoted
source_raw: raw-20260629T160852Z52Z
created_at: 2026-06-29
milestone: M-20260629T160852Z-A
---

## C-20260629T160852Z-A: legacy issue

- candidate_format_version: v2
- title: wt-close 支持 raw-{key} 参数 + help 强调不要传 test 分支
- status: promoted
- decision_reason: API 与 wt-create --raw-key 对称，减少认知负担。Phase 6b 已有自动关联逻辑，只需加参数入口和 help 提示
- next_action: 修改 docs/system/workspace/scripts/worktree/wt-close → 合并
- revisit_trigger: N/A
- acceptance_criteria:
  - wt-close 接受 raw-{key} 格式输入，内部推导 fix/feature 分支名
  - help 明确写传 fix|feature 分支，test-pre-merge 自动处理
  - 兼容现有 branch 参数
- promotion_gate: 修改 wt-close 脚本 + 测试通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: in-session
  - summary: wt-close Phase 6b 已有 test-pre-merge 自动清理逻辑，只需加 raw key 入口 + help
  - verdict: pass
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260629T160852Z-A/issue.md
- milestone: M-20260629T160852Z-A
- session_refs: []
