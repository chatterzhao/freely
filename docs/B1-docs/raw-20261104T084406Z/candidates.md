---
candidate_id: C-20261104T084406Z-A
status: promoted
source_raw: raw-20261104T084406Z
created_at: 2026-11-08
milestone: M-20261104T084406Z-A
---

# Candidates

被否决的替代方案（必填 22 字段 / 批量回填 / 只加 label / 塞进 body）见 brainstorms.md。

## C-20261104T084406Z-A: severity 从校验值变成可追溯的一等数据

- candidate_format_version: v2
- title: raw frontmatter 可选 severity 字段 + 契约校验/读视图回填 + 双平台 severity/Pn label + scan 按 P0→P2 排序
- status: promoted
- decision_reason: `--severity` 校验后四级全丢，优先级无法分诊；且 adapter 根本没有 labels 通道，不补齐链路就无法满足「按 label 过滤」的验收。
- next_action: 建 AT-001（6 静态 + 14 单元 + 10 行为，隔离 stub 驱动真实 feedback/issue-sync/adapter），改契约层、feedback、adapter、issue-sync。
- revisit_trigger: 若引入第三平台或把 label 体系换成自定义字段，需重新对齐 `create_issue` 的兼容调用与 `_labels()` 的口径。
- acceptance_criteria:
  - `--severity P0` 创建后 frontmatter 含 `severity: P0`，默认路径显式写 `P2`。
  - 平台 issue 带 `severity/P0` label：create-issue argv 含标签且真实 adapter 转发给两个 handler；旧 2 参 handler 不受影响。
  - `scan` 输出按 P0→P1→P2 排序，存量无字段文档按 P2 参与。
  - 存量回填：所有 raw 在读视图都有合法 severity，零历史文件重写。
  - 严格 21 字段文档仍通过 `validate()`，零退化。
- promotion_gate: AT-001 RED → GREEN + 14 个相关回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐行核对四处丢弃点；基线快照跑最终版 AT-001 得 `3 ok / 14 failed`；证伪 #4149/#4154/#4166/#4151 覆盖范围；确认 824 份历史文档不做重写。
  - verdict: pass
- promoted_issue_id: I-20261104T084406Z-A
- promoted_issue_path: docs/B2-docs/gate/platform/raw-20261104T084406Z/issues/I-20261104T084406Z-A.md
- milestone: M-20261104T084406Z-A
- session_refs: []
