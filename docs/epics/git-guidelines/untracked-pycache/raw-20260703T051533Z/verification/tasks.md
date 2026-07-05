# Tasks
- issue_id: I-20260703T051533Z-A

## Task List
### A1: 移除 git 跟踪的 .pyc 文件
- [x] git rm --cached 全部 6 个 .pyc 文件
### A2: 验证
- [x] git ls-files *.pyc 返回 0
- [x] daemon 可以正常启动
