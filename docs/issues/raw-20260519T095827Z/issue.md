---
issue_id: raw-20260519T095827Z
kind: raw
priority: P1
phase_state: absorbed
absorbed_into: I-20260413-0420-A
source: feedback
created_at: '2026-05-19T09:58:27Z'
title: '统一handoff栅栏格式: fence用json，语义用handoff'
platform_ids:
  github:
    issue_id: '650'
    url: https://github.com/chatterzhao/freely/issues/650
    synced_at: '2026-05-19T09:58:35Z'
updated_at: '2026-06-13T10:50:23Z'
primary_platform: github
platform_state: closed
force_closed_at: '2026-05-19T10:04:37Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

handoff是语义名，json是数据格式。正确写法:fence用json，内容为handoff数据。全文替换:agent文档中所有handoff fence改为json fence，handoff.py提取逻辑json优先，freely提示词同步。
