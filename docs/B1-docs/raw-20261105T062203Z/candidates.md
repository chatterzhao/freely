---
candidate_id: C-20261105T062203Z-A
status: promoted
source_raw: raw-20261105T062203Z
created_at: 2026-11-05
milestone: M-20261105T062203Z-A
---

# Candidates

## C-20261105T062203Z-A: 恢复模式按 git 登记反查 dev 工位真实路径

- candidate_format_version: v2
- title: 恢复摘要与 scan_state_worktree 使用反查的真实 dev 工位路径，不再用新建目标路径函数
- status: promoted
- decision_reason: 根因是混用了「新建目标路径」与「已有工位路径」两种语义。R3 已提供 `_wt_registered_dir()` 作为「已有工位」事实来源，直接复用即可，不引入第二套推导；正常创建与 legacy 补建确实需要冲突避让，必须保留原函数。
- next_action: 写 AT-001 行为测试复现带 hash 后缀的错误路径（RED），改恢复块两处调用为反查结果并加失败/一致性校验，跑 GREEN 与 7 个回归。
- revisit_trigger: 若未来把 worktree 登记迁到数据库，另开 issue 更新反查真源；本 PR 以 `git worktree list --porcelain` 为唯一事实来源。
- acceptance_criteria:
  - 恢复摘要的 dev 路径存在且等于预建 dev 工位路径。
  - `scan_state_worktree` 等于同一真实路径。
  - 反查不到时明确报错退出，不猜路径。
  - test 工位补建、完整初始化、二次重跑幂等不受影响。
  - 正常创建 / legacy 补建仍使用 `freely_wt_resolve_target_path` 做冲突避让。
  - 7 个相关回归测试零新增失败。
- promotion_gate: AT-001 RED → GREEN + 7 个回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 隔离 git 仓库实测复现 `-300efa56` 后缀污染；逐行核对恢复块与另外 3 处正常新建调用点的语义差异；确认 R3 的 `_wt_registered_dir()` 可直接复用。
  - verdict: pass
- promoted_issue_id: I-20261105T062203Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261105T062203Z/issues/I-20261105T062203Z-A.md
- milestone: M-20261105T062203Z-A
- session_refs: []
