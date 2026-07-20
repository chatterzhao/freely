# Tasks: DB 基础设施补齐 — review RPC + 原子分配 + Reviewer 注册修复
- issue_id: I-20260720T120329Z-A
- source_candidate: docs/B1-docs/raw-20260720T120329Z/candidates.md#C-20260720T120329Z-A

## Task Breakdown

### T1: 新增 reviews 表
- [x] 在 `freely_db_manager.py` `_ensure_tables()` 中添加 `CREATE TABLE IF NOT EXISTS reviews` (含 UNIQUE(raw_key, review_stage))
- [x] 添加 `CREATE INDEX IF NOT EXISTS idx_reviews_raw_key`
- [x] 添加 schema migration try/except（如后续加列）
- dependencies: none
- file: freely_db_manager.py

### T2: 新增 record_review RPC handler
- [x] 在 `freely_db_manager.py` 添加 `@_h("agent_working.record_review")` handler
- [x] UPSERT by (raw_key, review_stage)
- [x] 参数对齐 `agent_working.py:agent_record_review()` (L282-304): raw_key, review_stage, verdict, reviewed_by, findings
- dependencies: T1
- file: freely_db_manager.py

### T3: 新增 get_reviews RPC handler
- [x] 在 `freely_db_manager.py` 添加 `@_h("agent_working.get_reviews")` handler
- [x] 返回 `{reviews: {stage: {verdict, reviewed_by, reviewed_at, findings}}}`
- [x] 参数对齐 `agent_working.py:agent_get_reviews()` (L308)
- dependencies: T1
- file: freely_db_manager.py

### T4: agent_next_free 原子化
- [x] `agent_working.py` `agent_next_free()`: 新增 `raw_key=None` 参数
- [x] 有 raw_key 时调用 `next_free_and_assign`，无 raw_key 时 fallback `next_free`
- [x] 验证返回的 agent_id 已写入 agent_working 表（原子保证）
- dependencies: none (DB handler 已存在)
- file: agent_working.py

### T5: 移除 upsert_only 路径
- [x] `agent_working.py` `agent_assign()`: 移除 `update_only` 参数
- [x] 移除 `upsert_only` RPC 方法调用，统一使用 `agent_working.upsert`
- [x] 移除 reviewer 的 UPDATE_ONLY 注释/逻辑
- dependencies: none
- file: agent_working.py

### T6: 集成验证
- [x] 启动 DB daemon + 执行 AT-001 到 AT-005
- [x] 运行现有 `tests/` 套件确认无回归
- dependencies: T1, T2, T3, T4, T5
- file: verification/

## Task Order
```
T1 ──→ T2
  └──→ T3
T4 ──→ T6
T5 ──→ T6
```
T1/T4/T5 无依赖可并行。T2/T3 依赖 T1。T6 依赖全部。
