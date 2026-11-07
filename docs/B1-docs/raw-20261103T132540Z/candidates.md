---
candidate_id: C-20261103T132540Z-A
status: promoted
source_raw: raw-20261103T132540Z
created_at: 2026-11-07
milestone: M-20261103T132540Z-A
---

# Candidates

被否决的替代方案（读侧内联第二份正则、只认单一 verdict 写法、保留无 reason 覆盖、`completed` 全量套用未完成分支要求）属契约分叉或立即自锁，记录见 brainstorms.md。

## C-20261103T132540Z-A: 合并门禁读 verdict，评审判定不再默认通过

- candidate_format_version: v2
- title: pr-merge-guarded 解析 review verdict 而非查文件存在；pr-review-guarded 默认 needs_changes 且覆盖须带 reason；governance-merge-gate 的 completed 豁免保留 review+verdict 要求
- status: promoted
- decision_reason: 「文件存在 = 评审通过」让合并门禁对 develop 的全部强制力恒为真；写侧默认 pass 与读侧不读内容叠加，使评审结论不携带信息。
- next_action: 建单一 verdict 真源（Python 解析 + bash wrapper），改读侧/写侧/审计侧三处消费者，写 AT-001 RED→GREEN，跑回归基线对比与真实工位冒烟。
- revisit_trigger: 若未来引入第四种 verdict 取值，或 #4154 契约索引入驻 `verdict` 字段，需同步本契约与索引两处，不得再复制解析逻辑。
- acceptance_criteria:
  - review 文件写 `verdict: fail` 时 `pr-merge-guarded` 非零退出并打印原因；缺 verdict 字段同样不放行。
  - `grep -n '_review_verdict="pass"' bin/pr-review-guarded` 无命中；`freely-review` 超时/空输出写出 `needs_changes`。
  - `--verdict` 覆盖缺 `--reason` 被拒；带 reason 时 reason 写入 review 文档。
  - `governance-merge-gate` 对 `phase_state=completed` 且无 review 产物、或 review 声明非 pass 的输入报错。
  - 401 份真实 review 文档解析零不可判定（历史两种写法兼容，无自锁）。
- promotion_gate: AT-001 RED → GREEN + 回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐行复核三处消费者与写侧默认值；普查 401 份 review 文档确认两种 verdict 写法并存（399 有 verdict、9 份粗体）；用基线快照跑最终版 AT-001 得 14 项静态 FAIL（helper 缺失、读侧按存在打印 pass、写侧默认 pass、gate 裸 continue 等），确认能力整体缺失。
  - verdict: pass
- promoted_issue_id: I-20261103T132540Z-A
- promoted_issue_path: docs/B2-docs/gate/governance/raw-20261103T132540Z/issues/I-20261103T132540Z-A.md
- milestone: M-20261103T132540Z-A
- session_refs: []
