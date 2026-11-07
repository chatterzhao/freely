---
candidate_id: C-20261106T084804Z-A
status: promoted
source_raw: raw-20261106T084804Z
created_at: 2026-11-06
milestone: M-20261106T084804Z-A
---

# Candidates

被否决的替代方案（把函数内 return 一起改、把主流程抽成 main() 以支持 source、改 shim、顺手改四态判定）属越界或退化，完整记录见 brainstorms.md，不作为 candidate 立项。

## C-20261106T084804Z-A: 顶层 return 改为 exit

- candidate_format_version: v2
- title: wt-create 主流程三处顶层 `return 1` 改为 `exit 1`，失败时输出业务错误而非 bash 语法错误
- status: promoted
- decision_reason: 该文件是被 `exec bash` 直接执行的入口脚本，顶层 return 非法；修复只需 3 行，且必须保留函数内部 return 与所有清理动作/文案。
- next_action: 写 AT-001 RED（顶层 return 计数 + 三条失败分支端到端），改 3 行，跑 GREEN 与基线退化审计。
- revisit_trigger: 若未来确实需要支持被 source，应另开 issue 显式抽出 `main()` 并用 `BASH_SOURCE` 守卫，不在本 issue 范围。
- acceptance_criteria:
  - 三处失败分支均 exit 1，输出含业务错误文案且不含 `can only \`return'`。
  - 失败后 dev 分支被清理，不产生半成品工位。
  - 顶层 return 计数 = 0，函数内 return 数量保持 22，`bash -n` 通过。
  - shim 仍 `exec bash`；三条业务文案与清理动作逐字不变。
  - 相关回归零新增失败（2 个预存红测试归 #4151）。
- promotion_gate: AT-001 RED → GREEN + 回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 用括号深度分析逐行核对全文件 return 作用域；隔离 git 仓库注入三条失败分支实测 bash 语法错误与清理行为；逐条证伪 #4153（方向相反）与 #4157（不同文件）。
  - verdict: pass
- promoted_issue_id: I-20261106T084804Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261106T084804Z/issues/I-20261106T084804Z-A.md
- milestone: M-20261106T084804Z-A
- session_refs: []
