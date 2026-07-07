# tasks: 移除本地 raw issue 创建路径
- issue_id: I-20260707T043833Z-A
## Task 1: 删除 chat-inbox.py
- [x] git rm chat-inbox.py
## Task 2: freely_db_manager.py 移除 new-issue
- [x] 移除 update-issue-id / base-keys / materialize
## Task 3: governance-merge-gate 移除 catch-all
- [x] GATE 2a 从 auto-materialize 改为 error
## Task 4: freely-db-cli 移除 new-issue 默认
- [x] --type 默认值从 new-issue 改为空
## Task 5: freely main 重定向 chat --new-issue
- [x] new-issue 改为 error 引导到 feedback
## Task 6: 验证 0 残留
- [x] grep 确认 0 个 new-issue 引用
