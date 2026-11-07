---
candidate_id: C-20261104T082556Z-A
status: promoted
source_raw: raw-20261104T082556Z
created_at: 2026-11-07
milestone: M-20261104T082556Z-A
---

# Candidates

被否决的替代方案（只改 promote、复制到 B1、find 取首个）见 brainstorms.md。

## C-20261104T082556Z-A: 文档解析统一到单一 helper，promote 与 create 共用

- candidate_format_version: v2
- title: 新增 `_issue_file_for` 解析 B1/B2 双布局（缺失 rc 1、歧义 rc 2）、5 个命令统一使用、`platform_state` 仅在字段已存在时写
- status: promoted
- decision_reason: B1-only 路径假设让 B2 的 I-* 在任何命令下都无法被找到，promote 必然失败，导致 B1→B2 平台同步链路断开、只能手改 phase_state 绕过。
- next_action: 建 AT-001（5 静态 + 11 行为：B2 create、promote、缺失、歧义），改 `bin/issue-sync`。
- revisit_trigger: 若引入第三种文档布局（如 B3）或把 issue 文档迁到数据库，解析器必须随之收口。
- acceptance_criteria:
  - B2 的 I-* 执行 `cmd_create` 成功，两个平台 id 回写，且不注入 `platform_state`。
  - `cmd_promote` 对 B2 目标成功：raw 记录 `promoted_children`、B2 文档追加 `promoted_from` 注释、平台建单。
  - 文档缺失 → 非零退出并列出检查过的位置。
  - 同名文档两份 → 非零退出并列出候选（不静默取一个）。
  - `bin/issue-sync` 中不再有 `file="$ISSUES_DIR/$local_id/issue.md"` 硬编码。
- promotion_gate: AT-001 RED → GREEN + 回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 复现 R12 absorb 阶段的真实报错；核对 5 处同一路径假设；证伪 #4184/#4185/#4188/#4186/#4154 覆盖范围。
  - verdict: pass
- promoted_issue_id: I-20261104T082556Z-A
- promoted_issue_path: docs/B2-docs/gate/platform/raw-20261104T082556Z/issues/I-20261104T082556Z-A.md
- milestone: M-20261104T082556Z-A
- session_refs: []
