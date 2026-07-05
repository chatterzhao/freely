# PRD: 移除 git 跟踪的 .pyc 文件
- issue_id: I-20260703T051533Z-A

## Goal
消除 __pycache__ .pyc 文件导致的 dirty working tree，使 daemon 可以正常启动。

## 实现
git rm --cached 6 个 .pyc 文件。.gitignore 已有 __pycache__/ 规则。
