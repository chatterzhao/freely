# PRD: DB 基础设施补齐 — review RPC + 原子分配 + Reviewer 注册修复

## Goal

补齐 `agent_working` DB 层的 3 个基础设施缺口，使上层消费者（C-B: agent-id.env 退役）可以安全切换到 agent_working 唯一真源。

## Solution

### F1+F2+F3: reviews 表 + RPC handlers (freely_db_manager.py)

**新增 reviews 表**（在 `_ensure_tables()` 中 `agent_working` 表之后）：

```sql
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_key TEXT NOT NULL,
    review_stage TEXT NOT NULL,
    verdict TEXT NOT NULL,
    reviewed_by TEXT NOT NULL,
    reviewed_at TEXT NOT NULL DEFAULT (datetime('now')),
    findings TEXT DEFAULT '[]',
    UNIQUE(raw_key, review_stage)
);
CREATE INDEX IF NOT EXISTS idx_reviews_raw_key ON reviews(raw_key);
```

Schema migration: `ALTER TABLE` try/except 包裹（与现有 migration 模式一致）。

**record_review RPC handler**:

```python
@_h("agent_working.record_review")
def h_aw_record_review(daemon: DbDaemon, params: dict) -> dict:
    raw_key = params["raw_key"]
    review_stage = params["review_stage"]
    verdict = params["verdict"]
    reviewed_by = params["reviewed_by"]
    findings = params.get("findings", "[]")
    daemon.conn.execute("""
        INSERT INTO reviews (raw_key, review_stage, verdict, reviewed_by, reviewed_at, findings)
        VALUES (?,?,?,?,datetime('now'),?)
        ON CONFLICT(raw_key, review_stage) DO UPDATE SET
            verdict=excluded.verdict, reviewed_by=excluded.reviewed_by,
            reviewed_at=datetime('now'), findings=excluded.findings
    """, (raw_key, review_stage, verdict, reviewed_by, findings))
    daemon.conn.commit()
    return {"status": "ok", "raw_key": raw_key, "review_stage": review_stage}
```

**get_reviews RPC handler**:

```python
@_h("agent_working.get_reviews")
def h_aw_get_reviews(daemon: DbDaemon, params: dict) -> dict:
    rows = daemon.conn.execute(
        "SELECT * FROM reviews WHERE raw_key=? ORDER BY review_stage",
        (params["raw_key"],)).fetchall()
    reviews = {}
    for r in rows:
        reviews[r["review_stage"]] = {
            "verdict": r["verdict"], "reviewed_by": r["reviewed_by"],
            "reviewed_at": r["reviewed_at"], "findings": r["findings"]}
    return {"reviews": reviews}
```

### F4: agent_next_free 原子化 (agent_working.py)

当前调用链：`agent_next_free()` → `agent_working.next_free` RPC（只查不分配）→ 调用方再调 `agent_assign()`。

并发窗口：两个 Manager 同时查到同一 free agent → 都 assign → 重复分配。

修复：`agent_next_free` 新增 `raw_key` 可选参数，有值时调 `next_free_and_assign` 原子 RPC：

```python
def agent_next_free(project: str, role: str, pool_size: int, raw_key: str = None) -> Optional[str]:
    if raw_key:
        result = _db_rpc(project, "agent_working.next_free_and_assign", {
            "role": role, "pool_size": str(pool_size), "raw_key": raw_key})
        return result.get("agent_id") if result.get("assigned") else None
    result = _db_rpc(project, "agent_working.next_free", {
        "role": role, "pool_size": str(pool_size)})
    return result.get("agent_id") or None
```

调用方适配（`freely` L6014-6065）：传入 `raw_key`。

### F5: Reviewer 注册修复 (agent_working.py)

`agent_assign` 移除 `update_only` 参数和 `upsert_only` RPC 路径。所有 role 统一使用 `agent_working.upsert`（INSERT_OR_UPDATE）。

## Dev-Loop Handoff

1. `freely_db_manager.py`: 新增 reviews 表 + record_review handler + get_reviews handler
2. `agent_working.py`: agent_next_free 新增 raw_key 参数 → next_free_and_assign
3. `agent_working.py`: agent_assign 移除 update_only
4. 验证：pre-tests.md 5 个 acceptance items
