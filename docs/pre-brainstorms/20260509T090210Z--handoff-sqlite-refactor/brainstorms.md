# Brainstorm: 交接文档重构为 SQLite handoffs 表

- 来源: raw-20260509T090210Z (#267)
- 日期: 2026-05-09
- 基于: #265 B1 预研中的交接表设计

## 现状

主管-worker 交接通过三个分散文件管理：
- `exit-contract.env` — env 格式，仅 WORKER_PROMPTS_CSV
- `manager-continuity-*.md` — markdown，自由格式
- `worker-prompts/*.txt` — markdown，Worktree/Branch header

Runtime launch 通过 awk regex 解析 markdown → 脆弱，不校验工位合法性。

## 目标

一个 `handoffs` 表替代所有交接文件。role 字段区分主管/worker。

## 表设计

```sql
CREATE TABLE handoffs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  handoff_id TEXT NOT NULL UNIQUE,
  role TEXT NOT NULL,              -- 'manager' | 'worker'
  raw_key TEXT NOT NULL,
  worktree TEXT,                   -- 绝对路径，worker 有值
  branch TEXT,                     -- worker 有值
  prompt_file TEXT,                -- 交接文档路径
  parent_handoff_id TEXT,          -- worker → manager
  intent_kind TEXT,
  status TEXT NOT NULL DEFAULT 'pending',
  exit_kind TEXT,
  session_id TEXT,
  launched_at TEXT,
  completed_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

## INSERT/UPDATE 规则

- Manager 完成 patrol → INSERT role=manager, status=completed
- Manager 委派 worker → INSERT role=worker, status=pending
- Worker launch → UPDATE status=launched
- Worker 完成 → UPDATE status=completed
- 工位不对 → UPDATE status=rejected

追加不覆盖。同一 issue 多次委派 = 多条记录。

## 需要改的文件

| 文件 | 改动 | 优先级 |
|------|------|--------|
| `worker-store.py` → `handoff.py` | 建表、CRUD、迁移 | P0 |
| `freely` L1559+ | launch pipeline 改读表 | P0 |
| `freely` L1932-1937 | 废弃 exit_contract 文件函数 | P0 |
| `start-lead-agent.sh` | 读表替代读文件 | P1 |
| `monitor-ai-cli.sh` | 读表替代读文件 | P1 |

## 迁移路径

1. handoff.py 建表
2. 旧 env 文件 → 迁移 → INSERT 历史记录
3. 新写入走表，旧文件保留为文本备份
4. 表成为唯一数据源
