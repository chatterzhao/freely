---
local_id: raw-20260527T012528Z28Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2332'
    url: https://github.com/chatterzhao/freely/issues/2332
    synced_at: '2026-05-30T05:18:47Z'
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: 2026-05-27 01:25:28+00:00
updated_at: '2026-06-21T20:13:52Z'
intake_id: ''
author: zhaoquan
channel: local
session_refs: []
platform_state: closed
---

## 背景

当前 scan（`task-lifecycle-scan.py`）的扫描结果分两路存储：

1. **`.scan-state`**（`docs/issues/.scan-state`）：JSON 文件，记录 `last_scan_at` + 182 个已同步 issue 的 `{mtime, synced_at}` 映射，约 19KB
2. **next_action 输出**：scan 直接输出到 stdout，freely bash 捕获后驱动 supervisor 循环的下一步动作。这部分不持久化，每次 scan 重新生成

问题：
- `.scan-state` 是文件存储，和 SQLite 并行维护，增加复杂度
- next_action 无历史记录，无法追踪"上次 scan 建议了什么"vs"实际执行了什么"
- 文件写入不是原子的（不像 SQLite 有事务）
- `.scan-state` 被 gitignore 是对的（它是缓存），但当前和 raw issues 放同一目录容易混淆

## 评估维度

### 1. 是否迁移到 SQLite

| 维度 | 文件存储 | SQLite 存储 |
|------|---------|------------|
| 原子性 | 无（写入中途崩溃 = 损坏） | 事务保证 |
| 并发安全 | 无锁 | WAL + daemon 单写者 |
| 查询能力 | 需要完整读取+解析 | SQL 过滤、聚合 |
| 历史追踪 | 需要多文件管理 | 一行一条记录 |
| 与 DB 统一 | 额外维护路径 | 统一到 daemon |
| 外部可读性 | `cat` 即可 | 需要 SQL 查询 |

### 2. 覆盖写 vs 增量记录

**方案 A：覆盖写（当前模式）**
- 每次 scan 覆盖同一个 key
- 简单，无膨胀
- 丢失历史，无法对比

**方案 B：每次 scan 新记录**
- `scan_id` + `created_at` 标识每次扫描
- 可追踪历史演变
- 需要定期清理旧记录

**建议**：方案 B——scan 结果作为时序数据，每次 scan 一条记录，保留最近 N 次（如 50 次），超出自动清理。

### 3. 存储格式：JSON blob vs 拆分字段

**方案 A：JSON blob**
```sql
CREATE TABLE scan_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    result_json TEXT NOT NULL  -- 完整 JSON
);
```
- 灵活，schema 变更无需 ALTER TABLE
- 无法用 SQL 查询内部字段

**方案 B：拆分字段**
```sql
CREATE TABLE scan_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    -- 统计
    total_items INTEGER,
    pending_items INTEGER,
    blocked_items INTEGER,
    -- 每项的 next_action 单独存
    ...
);
CREATE TABLE scan_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id TEXT NOT NULL,
    raw_key TEXT,
    current_stage TEXT,
    next_action TEXT,
    ...
);
```
- 可用 SQL 精确查询
- schema 变更成本高

**建议**：混合方案——统计摘要拆分为字段，详细 items 存 JSON blob（items 结构频繁变化，JSON 更灵活）。

## 推荐设计

```sql
CREATE TABLE IF NOT EXISTS scan_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id TEXT NOT NULL UNIQUE,        -- YYYYMMDDTHHMMSSZ-{uuid}
    created_at TEXT NOT NULL,
    project TEXT NOT NULL,
    summary_json TEXT NOT NULL DEFAULT '{}',   -- 统计摘要 {"total": N, "pending": N, ...}
    items_json TEXT NOT NULL DEFAULT '[]',     -- 详细 items 数组
    platform_sync_batch_json TEXT DEFAULT '',   -- 平台同步批次
    scan_duration_ms INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_scan_created ON scan_results(created_at);
```

- `summary_json`：结构化统计，可 SQL 查询（考虑用 generated columns 或 JSON 函数）
- `items_json`：完整 items 数组，灵活演化
- 每次 scan INSERT 新记录，保留最近 50 次
- 替代 `.scan-state` 文件，删除文件存储路径

## 待决策

1. 保留最近多少次 scan 记录（建议 50）？
2. `summary_json` 是否值得拆分为独立列（total/pending/blocked）以便 SQL 查询？
3. 迁移时是否保留 `.scan-state` 作为 fallback？
