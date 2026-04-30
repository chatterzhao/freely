# Pre-tests — chat-inbox SQLite

- issue_id: `I-20260429-2040-A`
- issue_path: `docs/epics/workspace-routing-foundation/chat-inbox-sqlite/issues/I-20260429-2040-A.md`

## 验收项

1. `freely chat --new-issue "test"` → develop git status 无变化
2. `.freely/chat-inbox.db` 存在，chats 表有数据，consumed=0
3. `freely init` 幂等建表
4. `wt-create feature/raw-{ts}-test --base develop` 有对应 DB 记录时成功
5. `wt-create feature/raw-{ts}-test` 无对应记录时拒绝
6. `task-source-scan` 输出含 chat_intake source
7. `chat-inbox discard <id>` → consumed=-1，scan 不再输出
