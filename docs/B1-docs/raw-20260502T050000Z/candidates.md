---
name: freely-packaging-selfhost-candidate
description: 打包与自举验证——从 develop 打包可独立运行的 Freely 版本，用打包版本开发 Freely 自己，作为 merge 到 develop 的前置门禁
type: candidate
phase_state: promoted
priority: P0
promoted_issue_path: ""
milestone: current
session_refs:
  - {tool: "manual", session_id: "pre-brainstorm-creation", jsonl_path: "unavailable"}
next_action: 推进到 B2_IBM，创建 issue 进行实现
revisit_trigger: 无
---

## C-20260502T050000Z-A: legacy issue
- status: promoted

# Candidate: 打包与自举验证

## 目标

从 develop 打包出可独立运行的 Freely 版本，用打包版本开发 Freely 自己，打包后验证通过才能 merge 到 develop。

## 范围

- `bin/freely-package`：打包脚本
- `bin/test-pre-merge-selfhost`：自举验证门禁脚本
- `docs/system/workspace/package-allowlist.txt`：打包清单
- 版本号规则：YYYYMMDD-nightly（日常），YYYY.MM.DD-stable（从 main）

## 关联预研

`docs/B1-docs/raw-20260502T050000Z/brainstorms.md`
