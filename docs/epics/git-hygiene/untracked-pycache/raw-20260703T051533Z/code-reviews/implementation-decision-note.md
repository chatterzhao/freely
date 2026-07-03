---
issue_id: I-20260703T051533Z-A
issue_path: docs/epics/git-hygiene/untracked-pycache/raw-20260703T051533Z/issues/I-20260703T051533Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260703T051533Z-A
- issue_path: docs/epics/git-hygiene/untracked-pycache/raw-20260703T051533Z/issues/I-20260703T051533Z-A.md

## Implementation Decision Note
- decision: git rm --cached 全部 6 个 .pyc 文件
- why_this: .gitignore 已有 __pycache__/ 规则，pyc 是编译产物不应被跟踪
- alternatives_considered: 无——这是唯一正确做法
- boundary_non_goals: 不修改 .gitignore（规则已存在）
- residual_risk: 未来可能有人再次 git add -f 加回 pyc，pr-create-guarded 的 git 跟踪检查可作为兜底
