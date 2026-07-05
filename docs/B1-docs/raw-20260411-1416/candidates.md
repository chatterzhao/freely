# Candidates: pre-tests cleanup/retirement enforcement

## Candidate

- milestone: `M-20260306-workspace-routing-foundation`
- session_refs: []
- id: `C-20260411-1416-A`
- name: `pre-tests-cleanup-and-retirement-enforcement-governance`
- status: promoted
- problem_statement: `completed` 与 `test-pre-merge-* -> develop` 已有 pre-tests gate，但 cleanup/retirement 尚未统一消费 issue-bound `pre-tests.md`，导致 lifecycle closure 与测试真源未完全一致。
- scope:
  - 新增 cleanup/retirement 前的 pre-tests gate
  - 接入 cleanup_governance / retire_worktree 决策点
  - 失败时产出 machine-readable 缺口并阻止 retirement
- non_goals:
  - 不新增 `tests.md`
  - 不在本 owner 完成 adequacy schema 全量扩展
  - 不改写 completion/merge 既有 gate
- dependencies:
  - `pre-tests-evidence-binding-and-completion-gate-governance`
  - `branch-management` cleanup lifecycle 真源
- landing_zones:
  - `docs/system/workspace/scripts/quality/`
  - `docs/system/workspace/hooks/`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
  - `docs/system/workspace/three-loop-capability-lifecycle.md`
- acceptance_highlights:
  - cleanup/retirement 必须读取 issue `pre_tests_path`
  - pending acceptance item 或 evidence 不足时禁止 retire
  - 输出 item-level 缺口定位
  - completion/merge 门禁保持不回退
- priority: `high`
- recommendation: `materialize now`
- promoted_issue_path: `docs/B2-docs/ibm/pre-tests-cleanup-and-retirement-enforcement-governance/issues/pre-tests-cleanup-and-retirement-enforcement-governance.md`
