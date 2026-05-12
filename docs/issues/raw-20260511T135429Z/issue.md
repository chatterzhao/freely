---
local_id: raw-20260511T135429Z
kind: raw
priority: medium
status: open
source: platform
platform_ids:
  github:
    issue_id: "303"
    owner: chatterzhao
    repo: freely
created_at: "2026-05-11T13:54:29Z"
title: "feat: pre-push hook support FREELY_SKIP_IBM_GATE bypass"
---

## 问题

FREELY_SKIP_IBM_GATE=1 在 pre-merge-commit 已支持，pre-push 不认。

## 修复

pre-push.sh 调用 governance-merge-gate 前检查 FREELY_SKIP_IBM_GATE=1。
