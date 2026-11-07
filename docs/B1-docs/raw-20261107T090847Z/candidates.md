---
candidate_id: C-20261107T090847Z-A
status: promoted
source_raw: raw-20261107T090847Z
created_at: 2026-11-07
milestone: M-20261107T090847Z-A
---

# Candidates

被否决的替代方案（只认新值、改 pr-merge-guarded 写入值、用删除检查来避免提前退出、把 audit 包进 subprocess 吞掉错误）属历史不兼容或削弱治理，记录见 brainstorms.md。

## C-20261107T090847Z-A: 两代 receipt 兼容 + 审计链总能跑完

- candidate_format_version: v2
- title: governance-check 的 merge_path allowlist 兼容两代取值，并修复 set -e 提前退出使 receipt 审计与汇总总能执行
- status: promoted
- decision_reason: README 宣称的第三层必须既不过度误报也不静默失效；两代取值在历史里共存，控制流修复不能靠删检查实现。
- next_action: 写 AT-001 RED（隔离仓库真实 merge + 完整脚本汇总），改 allowlist 与 5 处控制流，跑 GREEN 与 9 个回归基线对比，真实 develop 验证。
- revisit_trigger: 若未来引入第三代 receipt 值，另开 issue 统一三处契约；本 PR 只对齐现有两代。
- acceptance_criteria:
  - 真实 `pr-merge-guarded` merge 不报 unknown；历史 `merge-guarded` 仍被接受；非法/缺失值仍 fail。
  - 完整 `governance-check` 在预存 `[FAIL]` 存在时仍输出汇总行；审计层实际运行。
  - 不删除/削弱任何既有检查；`pr-merge-guarded` / `commit-msg.sh` / `post-checkout` 不变。
  - 9 个相关回归以未修改 develop HEAD 基线对比零新增失败。
- promotion_gate: AT-001 RED → GREEN + 9 个回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 抽取 audit 函数在真实 develop HEAD 复现假阳性；`bash -x` 与隔离空仓库定位 `set -u` unbound variable 与三处 rg/return 非零；核对历史两代取值统计；逐条证伪 #4147/#4151/#4146 覆盖；真实 develop 复验 PROBE_ERRORS=0。
  - verdict: pass
- promoted_issue_id: I-20261107T090847Z-A
- promoted_issue_path: docs/B2-docs/gate/governance/raw-20261107T090847Z/issues/I-20261107T090847Z-A.md
- milestone: M-20261107T090847Z-A
- session_refs: []
