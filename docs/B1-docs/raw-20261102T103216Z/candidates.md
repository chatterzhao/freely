---
candidate_id: C-20261102T103216Z-A
status: promoted
source_raw: raw-20261102T103216Z
created_at: 2026-11-02
milestone: M-20261102T103216Z-A
---

# Candidates

## C-20261102T103216Z-A: 受控调用方显式标记（不依赖 ps）

- candidate_format_version: v2
- title: wt-create / wt-close 通过显式标记获得授权，hook 不再只靠 ps 识别调用方
- status: promoted
- decision_reason: `ps` 在沙箱不可用时，reference-transaction 与 pre-push 的调用方识别恒失败，连被授权的 wt-create/wt-close 也被拦；分支建不出、远程分支删不掉。用封装命令设置的显式标记替代进程树探测，保留直接命令的默认拦截。
- next_action: B2 物化 `I-20261102T103216Z-A`；先写 hook 级 RED 测试，再改 hook 与调用方。
- revisit_trigger: 出现“手工 export 标记即可绕过”的真实滥用，或 hook 被非封装工具调用时行为异常。
- acceptance_criteria:
  - `FREELY_WT_CREATE=1` 时 reference-transaction 放行受控分支创建；无标记时仍拦截
  - `FREELY_ALLOW_REMOTE_BRANCH_DELETE=1` 时 pre-push 放行删除；无标记时仍拦截
  - `wt-create` 在 ps 不可用环境可创建 fix 工位
  - `wt-close` 在 ps 不可用环境可删除双平台远程分支
  - 直接 `git worktree add -b` 与直接 `git push --delete` 仍被拦
- promotion_gate: hook 级测试 RED→GREEN + 真实 wt-create/wt-close 验证 + `governance-merge-gate --range develop..HEAD`
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 已验证 `.githooks/*` 只是包装层，真实 hook 在 `docs/system/workspace/hooks/`；两个 hook 共用 ps 探测模式
  - verdict: pass
- promoted_issue_id: I-20261102T103216Z-A
- promoted_issue_path: docs/B2-docs/git-worktree/wt-close/raw-20261102T103216Z/issues/I-20261102T103216Z-A.md
- milestone: M-20261102T103216Z-A
- session_refs: []
