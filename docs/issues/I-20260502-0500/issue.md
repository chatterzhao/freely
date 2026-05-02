---
local_id: I-20260502-0500
kind: linked
status: in_progress
phase_state: done_ibm
canonical_issue_path: docs/issues/I-20260502-0500/issue.md
created_at: "2026-05-02T05:00:00Z"
updated_at: "2026-05-02T05:50:00Z"
---

# Issue: Freely 打包与自举验证

## 目标

从 develop 打包出可独立运行的 Freely 版本，用打包版本开发 Freely 自己，打包后验证通过作为 merge 到 develop 的前置门禁。

- issue_id: I-20260502-0500
- source_candidate: docs/pre-brainstorms/freely-packaging-selfhost/candidates.md#c-20260502-0500-a

## 产出

- `bin/freely-package`：打包脚本，根据 allowlist 复制文件到版本目录
- `bin/test-pre-merge-selfhost`：自举验证门禁，打包 → 启动 daemon → 验证 cycle
- `docs/system/workspace/package-allowlist.txt`：打包清单
