---
candidate_id: C-20261104T083043Z-A
status: promoted
source_raw: raw-20261104T083043Z
created_at: 2026-11-05
milestone: M-20261104T083043Z-A
---

# Candidates

## C-20261104T083043Z-A: wt-create 中断恢复与 test 工位补建

- candidate_format_version: v2
- title: 让 wt-create 在部分成功后可重跑恢复，并兑现 legacy 补建承诺
- status: promoted
- decision_reason: 标准模式两步创建无事务边界，重跑被「分支已存在」与 fuzzy-match 双重拒绝；把 test 工位初始化抽成唯一函数后，恢复路径与标准路径共享同一真源，改动局部且可回归。
- next_action: 先写恢复能力回归测试确认 RED，再实现幂等状态机与初始化函数，GREEN 后走 test-pre-merge。
- revisit_trigger: 若后续需要在中断时自动回滚整个创建过程，另开 issue 处理 trap 回滚；本 PR 只负责恢复已存在的残留。
- acceptance_criteria:
  - dev 工位存在、test 工位缺失时，重跑原 `wt-create --raw-key ... --source platform --kind ... --slug ...` 会补建 test 工位并完整初始化，退出码 0。
  - dev 与 test 工位都存在时，重跑为幂等 no-op，退出码 0 且输出已存在状态，不产生重复工位。
  - dev 缺失而 test 存在时拒绝创建并退出非零。
  - legacy 模式传入 `test-pre-merge-<key>-<slug>` 时以对应 dev 分支为 base 创建，并执行 seed、`.freely` 状态克隆与 `test-gate.env` 初始化。
  - 帮助文本与实际行为一致；新增脚本级回归测试覆盖以上场景。
- promotion_gate: 回归测试 GREEN + test-pre-merge 验证 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 逐行核对 wt-create :254-324、:652-690、:722-787、:859-877，确认根因是存在性检查与内联初始化，非命令性能问题；本轮实测 1m57s 双工位创建成功可佐证。
  - verdict: pass
- promoted_issue_id: I-20261104T083043Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261104T083043Z/issues/I-20261104T083043Z-A.md
- milestone: M-20261104T083043Z-A
- session_refs: []
