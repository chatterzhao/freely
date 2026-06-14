---
issue_id: raw-20260519T094555Z
kind: raw
priority: P0
phase_state: absorbed
absorbed_into: I-20260413-0420-A
source: feedback
created_at: '2026-05-19T09:45:55Z'
title: extract_handoff_block 兼容 json fence——AI写json非handoff
platform_ids:
  github:
    issue_id: '649'
    url: https://github.com/chatterzhao/freely/issues/649
    synced_at: '2026-05-19T09:46:01Z'
updated_at: '2026-06-14T12:59:58Z'
primary_platform: github
platform_state: closed
force_closed_at: '2026-05-19T09:50:44Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

AI写三个反引号json而非三个反引号handoff。extract_handoff_block只搜handoff。修复：增加json回退，检查exit_kind字段。
