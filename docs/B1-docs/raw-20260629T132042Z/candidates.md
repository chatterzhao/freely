---
candidate_id: C-20260629T132042Z-A
status: promoted
source_raw: raw-20260629T132042Z
created_at: 2026-06-29
milestone: M-20260629T132042Z-A
---

## C-20260629T132042Z-A: legacy issue

- candidate_format_version: v2
- title: replace ./bin/ with freely in hook scripts and start-lead-agent
- status: promoted
- decision_reason: 与 #3622 全链路命令规范化保持一致，216 个文件已完成，仅剩 6 个 .sh 文件因 gate 判定撤回需单独修复。采用全文机械替换策略（Option A），与已完成的 216 个文件处理方式一致。
- next_action: 进入 B2_IBM → 物化 I-* issue → 写 pre-tests → 执行替换 → RED-GREEN 验证
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - 6 个 .sh 文件中所有 `./bin/<command> <args>` 替换为 `freely <command> <args>`
  - `source ./bin/worktree-common.sh` 和对应的文件存在性检查保留不变
  - 存在性/可执行性检查（`[[ -x "./bin/..."`）替换为 `which freely` 检查
  - 用户提示/错误消息中的 `./bin/xxx` 路径引用同步更新
  - 通过完整 IBM 门禁（governance-merge-gate + governance-promotion-gate）
  - hooks 在 `freely` 体系下正常工作
- promotion_gate: B2 完成 pre-tests/tasks/code-review → dev 实现 → test-GREEN → pr-create → merge
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: in-session
  - summary: 评审 6 个 .sh 文件中的 ./bin/ 引用，确认替换策略正确（区分 CLI 命令与库引用），与 #3622 规范化方向一致
  - verdict: pass
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260629T132042Z-A/issue.md
- milestone: M-20260629T132042Z-A
- session_refs: []
