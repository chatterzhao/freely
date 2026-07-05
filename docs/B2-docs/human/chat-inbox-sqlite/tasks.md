# Tasks: chat-inbox-sqlite

1. Implement `chat-inbox.py` for SQLite-backed chat storage.
2. Wire `_write_chat_to_issue` to insert instead of file write.
3. Update `wt-create` to materialize from DB records.
4. Update `task-source-scan.py` to include chat_intake sources.
5. Ensure `freely init` creates chat-inbox.db lazily.
