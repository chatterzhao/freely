---
local_id: I-20260429-1745-A
issue_title: "Fix daemon self-detection suicide + bash 3.2 pipefail crash"
kind: linked
status: in_dev
phase_state: in_dev
promoted_from: raw-20260429-1745
platform_ids:
  github: {}
  gitee: {}
primary_platform: github
canonical_issue_path: "docs/epics/workspace-routing-foundation/bash32-daemon-compat-fix/issues/I-20260429-1745-A.md"
last_synced_comment_at: {}
hash: ""
created_at: "2026-04-29T17:45:00Z"
updated_at: "2026-04-29T17:45:00Z"
session_refs:
  - {tool: ccds, session_id: "20260429-bash32-fix", role: "author"}
---

## Pre-Brainstorm Summary

macOS bash 3.2 兼容性修复：两处防御性代码改动，不改变核心逻辑。
- `resolve_active_supervisor_pid_for_start`：显式排除 `$$` 防止自检测
- `select_launch_kind`：用 `nullglob` 数组检查代替裸 `ls` 管道

## Scope

两处修复均为最小化针对性改动，仅增加防御性代码：
- 不升级 bash 版本要求
- 不修改 shebang
- 不改变核心业务逻辑

## References

- B1: docs/pre-brainstorms/20260429-1745--bash32-daemon-compat-fix/
- Issue: docs/epics/workspace-routing-foundation/bash32-daemon-compat-fix/issues/I-20260429-1745-A.md
