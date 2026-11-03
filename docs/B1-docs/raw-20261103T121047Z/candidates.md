---
candidate_id: C-20261103T121047Z-A
status: promoted
source_raw: raw-20261103T121047Z
created_at: 2026-11-03
milestone: M-20261103T121047Z-A
---

# Candidates

## C-20261103T121047Z-A: merge 时 issue-sync 按 lane raw key 收敛 + Gitee reopen 形态修复

- candidate_format_version: v2
- status: promoted
- decision_reason: 事故根因是 merge-guard 用 diff 全量文档推进生命周期；收紧到分支 raw key 是最小、可测、不改变正常行为的修复。Gitee reopen 与 close 形态不一致属于同批平台收口缺陷，合并修复。
- next_action: 先写 scope 过滤与 reopen request 的 RED 单测，再实现 helper + patch，GREEN 后走 test-pre-merge。
- revisit_trigger: 若未来确实需要在一个 lane 收口多个 raw issue，必须显式使用 issue-sync close，而不是依赖 merge diff。
- acceptance_criteria:
  - pr-merge-guarded 只同步 id 含分支 raw key 的 issue；其他 changed raw docs 不被改 phase、不被关闭。
  - 分支名无 raw key 时保持旧行为。
  - gitee-issue.py reopen 使用 /repos/{owner}/issues/{number} + {"repo": <name>, "state": "open"}（与 close 同形态）。
  - 两个单测 RED→GREEN；正常 lane 收口行为不变。
- promotion_gate: 单测 GREEN + test-pre-merge + governance gate
- open_questions: 是否需要在 merge 日志中显式打印被跳过的文档数量（本 PR 暂不加）。
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 复盘事故日志与新旧代码路径，确认 diff 全量同步是根因；scope filter 可行性由纯函数单测覆盖
  - verdict: pass
- promoted_issue_id: I-20261103T121047Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/merge-guard-issue-sync-scope/raw-20261103T121047Z/issues/I-20261103T121047Z-A.md
- milestone: M-20261103T121047Z-A
- session_refs: []
