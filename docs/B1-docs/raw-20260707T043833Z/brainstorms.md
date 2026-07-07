---
b1_id: B1-20260707T043833Z
phase_state: completed
source_raw: raw-20260707T043833Z
source_url: https://github.com/chatterzhao/freely/issues/3795
produced_candidate: C-20260707T043833Z-A
---
# B1: 彻底移除本地 raw issue 创建路径

## Discovery: 7 个文件包含本地路径

| # | 文件 | 本地路径 | 操作 |
|---|------|---------|------|
| 1 | `chat-inbox.py` | materialize/consume 本地 raw issue | 删除文件 |
| 2 | `freely_db_manager.py` | new-issue chat_type 创建 + 查询 | 移除 new-issue 逻辑 |
| 3 | `governance-merge-gate` | GATE 2a chat-inbox catch-all | 移除 catch-all |
| 4 | `freely-db-cli` | --type new-issue 默认值 | 移除默认值 |
| 5 | `freely` main | `chat --new-issue` 命令 + `_write_chat_to_issue` | 重定向到 feedback |
| 6 | `task-lifecycle-scan.py` | chat inbox scanning | 移除扫描逻辑 |
| 7 | `wt-create` | source 校验 | 已强制 platform ✅ |

## Decision: 不留 fallback，全部硬拦截
- chat-inbox.py: 整个文件删除（唯一调用方是 main freely 脚本）
- DB: 保留 chats 表但移除 new-issue 创建路径，仅保留 comment 类型
- Gate: 移除 auto-materialization，改为报错引导 feedback
- CLI: `--type new-issue` 默认值改为必填参数，不存在时拒绝

## Candidate: C-20260707T043833Z-A, promoted
