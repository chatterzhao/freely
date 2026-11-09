# Pre-Tests: DB 读写边界收口
- issue_id: I-20261104T075910Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 除 `freely_db_manager.py` 与 `db_write_gate` 外，工作区不得存在未登记的写连接；只读连接必须是真只读（写操作抛错）；并发两个短写者都落库；读者不得看到未提交事务的行
- acceptance_target: 「单写者」从文档声明变成可机械验证的边界；辅助 store 有 owner 与迁移路径
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实工作区扫描（20 处 `sqlite3.connect`）+ 真实 `db_write_gate` 模块 + 临时 SQLite 文件（含并发线程与未提交事务）；develop HEAD 基线快照对比
- required_evidence: 5 静态 + 1 守卫 + 5 行为共 11 项全 GREEN；基线 RED `5 ok / 6 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-db-single-writer.py
- test_command: python3 docs/system/workspace/scripts/tests/test-db-single-writer.py
- expected_output: SUMMARY: 11 ok, 0 failed
- expected_RED_output: SUMMARY: 5 ok / 6 failed（lint / write gate / State 契约段 / 未登记写连接 / 只读拒绝写 全部缺失；5 项 PASS 是守卫与 SQLite 自身隔离——直连总数≥20、stub 恰好返回 None、单条 UPDATE 自动串行、未提交事务默认不可见）
- actual_RED_output: develop `93fa22297` 基线快照注入最终版 AT-001 → `SUMMARY: 5 ok, 6 failed`（AT-001-RED.log）。关键证据：`no unregistered writable connection remains (found 17: docs/system/workspace/scripts/quality/governance-closeout-gate:46, ...)`。
- actual_output: 工位同一断言 → `SUMMARY: 11 ok, 0 failed`（AT-001-GREEN.log），`[db-writers] OK: every connection is the daemon, the write gate, read-only, or registered`。
- evidence_file: docs/B2-docs/runtime/daemon/raw-20261104T075910Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: 静态组断言 lint 存在、gate 暴露三个工厂、State 契约登记三 store，并用 AT 内置的 `_unregistered_connections()` **独立重推**边界（不依赖 lint 自证）。守卫组断言工作区确有 ≥20 处直连（防止 RED 空跑）。行为组在临时库上验证：缺库返回 None、只读连接写操作抛 `sqlite3.Error`、两个线程各调一次 `write_tx` 后计数为 2、未提交事务期间读者计数为 0、提交后为 2。
- red_how: fix RED — `git archive develop -- bin docs .githooks templates .gitee-ci.yml .github` 出 `/tmp/r20-base`，把最终版 AT-001 拷入快照 tests 目录，以 `--source-dir /tmp/r20-base` 运行。

## End-to-End
- acceptance_target: 边界在真实工作区成立 + 并发写与隔离读
- testing_layer: end-to-end
- target_environment: 真实工作区 + 临时 SQLite 文件 + 线程并发
- required_evidence: AT-001（行为 5 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-db-single-writer.py

## Unit
- acceptance_target: lint 规则与 gate 工厂
- testing_layer: unit
- target_environment: fix/raw-20261104T075910Z-db-single-writer
- required_evidence: AT-001（静态 5 项 + 守卫 1 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-db-single-writer.py

## Integration
- acceptance_target: 既有 scan / 副本对账 / 门禁能力不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 相关回归
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
2. python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
3. python3 docs/system/workspace/scripts/tests/test-handoff-store.py
4. python3 docs/system/workspace/scripts/tests/test-scan-frontmatter-nested.py
5. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 行为测试全部用临时 SQLite 文件与线程，不触碰真实 `.freely/freely.db`；`mode=ro` 改造只读真实库的**只读**路径，未在真实库上执行任何写。
- real_environment_reason: 该缺陷只能在真实工作区扫描 + 真实 SQLite 事务并发下验证；改动后 `test-raw-reconciliation.py`、`test-raw-replica-degraded.py`、`test-handoff-store.py`、`test-scan-frontmatter-nested.py`、`bin/test-all --ci` 全绿，证明只读改造未破坏 `scan` 与副本对账。
