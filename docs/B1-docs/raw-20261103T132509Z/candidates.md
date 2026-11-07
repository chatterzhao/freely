---
candidate_id: C-20261103T132509Z-A
status: promoted
source_raw: raw-20261103T132509Z
created_at: 2026-11-03
milestone: M-20261103T132509Z-A
---

# Candidates

被否决的替代方案（删除 commit-msg.sh 并把 README 三层降级为事后审计、无差别保留 test-pre-merge-* 的 receipt 要求、只校验 trailer 文本而不验受控 handshake、改动 pr-merge-guarded 的写入值）属削弱治理或自锁，记录见 brainstorms.md，不作为 candidate 立项。

## C-20261103T132509Z-A: 接线 commit-msg 提交期阻断

- candidate_format_version: v2
- title: 新增 fail-closed commit-msg shim，校验受保护 merge 的 receipt 与受控 handshake，补齐三层治理第一层
- status: promoted
- decision_reason: 130 行实现完整但无人执行，是「看起来有、实际不跑」的假安全感；接线成本最低且能真正补上提交期阻断。必须同时用受控 handshake 挡住自填 trailer，且不能拦每轮 test 工位 sync merge。
- next_action: 探针验证 merge --continue 的 hook 触发与状态可见性；写 AT-001 RED（隔离仓库真实 merge）；新增 shim、改真源与 README；跑 GREEN 与 13 个回归基线对比；真实工位 commit/PR 冒烟。
- revisit_trigger: 若 R9.5 修好 governance-check 第三层后需要统一两代 receipt 取值契约，另开 issue 对齐；本 PR 不改 governance-check / pr-merge-guarded。
- acceptance_criteria:
  - `.githooks/commit-msg` 存在、用 `-f`、缺真身 `exit 2`，`post-checkout` 不变。
  - develop merge 缺 trailer 被拒且打印原因；自填 trailer 无受控 handshake 被拒；合法 guarded merge 通过。
  - test-pre-merge sync merge 通过（不自锁）；普通 commit 与通用规范保持。
  - README 三层表述与实现一致；13 个回归以未修改 develop HEAD 基线对比零新增失败。
- promotion_gate: AT-001 RED → GREEN + 13 个回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 精读 130 行孤儿实现与 pr-merge-guarded trailer/handshake 生命周期；探针实测 hook 触发与状态可见；真实历史 25 条 commit 兼容性检查；隔离仓库 6 个真实 merge/commit 场景；3 个真源还原到 develop 做 RED 与 13 个回归基线对比。
  - verdict: pass
- promoted_issue_id: I-20261103T132509Z-A
- promoted_issue_path: docs/B2-docs/gate/governance/raw-20261103T132509Z/issues/I-20261103T132509Z-A.md
- milestone: M-20261103T132509Z-A
- session_refs: []
