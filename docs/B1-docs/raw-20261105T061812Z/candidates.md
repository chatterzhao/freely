---
candidate_id: C-20261105T061812Z-A
status: promoted
source_raw: raw-20261105T061812Z
created_at: 2026-11-05
milestone: M-20261105T061812Z-A
---

# Candidates

被否决的替代方案（把四态判定并入 R4 路径解析重构、把顶层 return 一起修、批量改写历史工位）属于独立 issue 范围，完整记录见 brainstorms.md，不作为 candidate 立项。

## C-20261105T061812Z-A: 四态判定校验工位目录与初始化标记

- candidate_format_version: v2
- title: pre-flight 用注册目录 + test-gate.env 完成标记判定，恢复路径按残留项分别补建
- status: promoted
- decision_reason: 分支存在不等于工位可用；旧判定只看分支会让「工位目录被删」与「Step 2 半初始化」都误判为完成。修复必须复用 `_init_test_worktree_state()` 单一真源，且不得改变 no-op / 不一致拒绝 / legacy 补建的既有语义。
- next_action: 写 AT-001 行为测试复现三种残留（RED），新增两个判定 helper，改造 pre-flight 与恢复路径，跑 GREEN 并对 4 个既有 wt-create 测试做基线对比。
- revisit_trigger: 若未来把 worktree 状态改为数据库托管，另开 issue；本 PR 只以 `git worktree list` + 文件标记为事实来源。
- acceptance_criteria:
  - 「分支在、工位目录不在」重跑能补建两个工位且 test 完全初始化。
  - 「test 目录在但缺 test-gate.env」重跑能补齐标记，第二次重跑为 no-op。
  - 「dev 缺 / test 在」仍拒绝；双工位齐全仍幂等 no-op 且不产生重复工位。
  - 4 个既有 wt-create 回归以未修改 develop HEAD 做基线对比，零新增失败。
  - 不改 `freely_wt_resolve_target_path`（R4 独立）、不改顶层 `return`（#4201 独立）。
- promotion_gate: AT-001 RED → GREEN + 四态行为覆盖 + 既有回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 隔离 git 仓库精确复现两种误判；逐行核对 pre-flight 与恢复路径；核对 #4153/#4157/#4151 覆盖范围避免重复立项；实测 `git worktree add` 对已存在分支必须不带 -b。
  - verdict: pass
- promoted_issue_id: I-20261105T061812Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261105T061812Z/issues/I-20261105T061812Z-A.md
- milestone: M-20261105T061812Z-A
- session_refs: []
