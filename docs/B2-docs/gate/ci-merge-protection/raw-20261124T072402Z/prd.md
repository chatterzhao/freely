# PRD: 更正 governance check 文档断言

- issue_id: I-20261124T072402Z-A
- source_candidate: docs/B1-docs/raw-20261124T072402Z/candidates.md#C-20261124T072402Z-A

## Goal

消除 workflow 注释与实现的矛盾：注释第 3 条声称 pr-merge-guarded 会把 check 置 success，实际该 check 恒 in_progress——而这正是拦截网页合并、强制走本地治理链路的设计态。防止后来者（含 AI）再基于错误注释"修复"一个不存在的缺陷。

## 实现方案

1. 更正 `.github/workflows/pr-merge-guard.yml` 注释：
   - 删除/改写第 3 条「Only pr-merge-guarded sets it to success」；
   - 明确「check 保持 in_progress 是 designed state；合并走本地 pr-merge-guarded（git merge + push），不经过 GitHub UI，因此永不置 success；分支保护使 UI Merge 按钮保持禁用」。
2. 新增静态 AT `test-governance-check-doc-alignment.py`：断言注释不再含误导性的 "sets it to success" 声称、含 "in_progress" 设计态说明、且 pr-merge-guarded 源码没有调用 `_set_governance_check_pass`（防止有人按错误注释接线）。
3. AT 接入 `bin/test-all` CORE/CI_CORE。

## 不退化边界

- 不改 workflow 的 jobs/permissions/triggers 与运行行为。
- 不改 pr-merge-guarded 的合并逻辑。
- 不改分支保护配置（保持启用态）。
- 不触碰平台 issue 生命周期。

## Dev-Loop Handoff

见 `verification/pre-tests.md`。RED：develop 基线注释仍含错误声称、AT 不存在 → 失败；GREEN：更正后全绿。
