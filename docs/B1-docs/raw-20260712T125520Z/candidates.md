## C-20260712T125520Z-A: AI_MODE fix #2
- status: absorbed
- absorbed_into: I-20260712T124601Z-A
- milestone: M-20260712T124601Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20260712T124601Z/issues/I-20260712T124601Z-A.md
- decision_reason: 与 raw-20260712T124601Z（第一轮 AI_MODE hotfix）属同一根因——AI_MODE 未设默认值导致 set -u 下 unbound variable crash。两轮修复目标一致、范围相邻，合并到同一个 I-* issue 统一管理生命周期，避免冗余 issue 碎片化。
