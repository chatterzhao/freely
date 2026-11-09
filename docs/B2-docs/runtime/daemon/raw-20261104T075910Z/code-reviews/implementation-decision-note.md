# Implementation Decision Note
- issue_id: I-20261104T075910Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20261104T075910Z/issues/I-20261104T075910Z-A.md
- decision: 读全部改 `mode=ro` 只读 URI；写集中到 `runtime/db_write_gate.py`（`BEGIN IMMEDIATE` + 锁重试），既有多写者以 `# db-writer:` 显式登记并进入 State 契约；`bin/check-db-writers` 强制边界
- why_this: 单写者不变量已在文档里声明，但工作区有 20 处直连（issue 只列 6），`_generate_chat_id` 的「Single-writer daemon」注释是假的。不设机械边界，每轮都会新增直连。
- alternatives_considered: ①全部走 daemon RPC——只读 CLI（`governance-gate`/`scan`/`wt-create`）会依赖 daemon，而它们正是 daemon 挂了时要用的诊断工具，故障域被放大；②只加 lint 不改语义——读写混杂不变，读方仍可能取写锁；③把 3 个辅助 store 直接合表——需要数据迁移与兼容期，超出本条；④`immutable=1`——会忽略 WAL 已提交数据，读到旧快照。
- boundary_non_goals: 不改表结构与写入语义；不改 `freely_db_manager.py`；不把只读 CLI 改成 RPC；不删除遗留备份文件；不迁 3 个辅助 store（只登记 + 迁移路径）。
- residual_risk: ①三个辅助 store 仍是合法第二写入方，登记只是「可追溯」不是「已消除」；②`# db-writer:` 注释可被随意添加，lint 拦不住「故意登记」，但登记必须同时出现在 State 契约里，review 可查；③`mode=ro` 要求库文件存在，若某处以「库不存在则建库再读」为前提会行为变化——本轮的 11 处都由调用方先判存在，已跑回归确认；④`write_tx` 的重试上限 10s，极端锁竞争下仍会抛错（比静默丢写好）。
- verification: AT-001 develop 基线 RED `5 ok / 6 failed`（`found 17` 处未登记写连接）→ 工位 GREEN `11 ok / 0 failed`；`bin/check-db-writers` 扫 20 处全部合规；`test-raw-reconciliation.py`/`test-raw-replica-degraded.py`/`test-handoff-store.py`/`test-scan-frontmatter-nested.py`/`bin/test-all --ci` 全绿。
- self_bootstrap_findings: ①issue 只报了 6 处，实际 20 处，`wt-create` / `freely`×4 / `governance-*`×3 全被漏记；②「半提交读」在基线本来就不会发生（SQLite 快照隔离），所以这一项是**验证性**的而非修复性的，RED 里它 PASS 属正常；③`mode=ro` 改造后必须先判库存在，否则原「建库再读」的路径会抛错——已在改造时逐处确认调用方先判存在。

## Implementation Decision Note
- decision: 读 `mode=ro` + 写集中 `db_write_gate` + lint 边界 + 辅助 store 登记
- why_this: 20 处直连让「单写者」声明失效，且无机械约束
- alternatives_considered: 全 RPC / 只加 lint / 直接合表 / immutable=1
- boundary_non_goals: 表结构、daemon、CLI 依赖、备份清理、store 迁移均不动
- residual_risk: 登记≠消除、注释可被滥用、mode=ro 需库存在、write_tx 有重试上限
