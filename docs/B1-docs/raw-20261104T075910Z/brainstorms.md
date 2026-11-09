---
raw_id: raw-20261104T075910Z
status: brainstormed
created_at: 2026-11-09
---

# Brainstorms

## 覆盖域（逐个核对 issue 的点）

issue 只点了 6 个文件，实际扫描 `docs/system/workspace/scripts/**` 得到 **20 处** 生产直连（另有 tests 20 处豁免）：

| 分类 | 数量 | 位置 |
|---|---|---|
| 只读 | 11 | `governance-closeout-gate:46`、`governance-merge-gate:1324/2114`、`freely:7112/17347/24943/25042`、`task-lifecycle-scan.py:586`、`watchdog_sse.py:382`、`wt-create:678/733` |
| 写 | 6 | `agent_protocol.py:82/116`、`cleanup-agent-working.sh:7`、`discussion_events.py:177`、`freely:20729`、`handoff_store.py:44` |
| 唯一合法写者 | 1 | `freely_db_manager.py:119` |
| 遗留 | 1 | `task-lifecycle-scan.bak.py`（3 处，已排除） |

issue 漏记了 `wt-create`、`freely` 的 5 处、`governance-*` 三处 —— 说明「单写者已失效」的范围比报告更大。

## 方案方向

### 方向 A：全部改走 db manager 的 JSON-RPC（最彻底）

- 所有读写都发 socket 请求给 daemon。
- 优点：物理上只有一个连接。
- 缺点：**把只读 CLI 也变成 daemon 依赖**——`governance-gate`、`scan`、`wt-create` 一旦 daemon 没起就全挂；而这些正是「daemon 挂了要能诊断」的工具。引入新故障域，风险高于收益。

### 方向 B：读显式只读 + 写集中到唯一工厂（选中）

- 读：`mode=ro` URI + `PRAGMA query_only`（永不建库、永不取写锁、看不到未提交行）。
- 写：新增 `runtime/db_write_gate.py`，`write_tx()` 用 `BEGIN IMMEDIATE` + `busy_timeout` + 锁重试；既有 6 处短写者以 `# db-writer:` 显式登记，逐轮迁移。
- lint：`bin/check-db-writers` 强制上述四类形态。
- 优点：不引入 daemon 依赖；边界可机械验证；辅助 store 有登记与迁移路径。
- 缺点：登记写者仍是「合法的第二个写入方」，但**数量从 17 降到 3 个 store**，且每个都有 owner 与迁移计划。

### 方向 C：只加 lint，不改连接语义

- 缺点：lint 只能证明「没有新增违规」，既有的读写混杂仍在，`mode=ro` 缺失意味着读方仍可能取写锁。

**选 B**。A 的故障域问题不可接受，C 治标不治本。

## fidelity 基线

验收必须能在**没有 lint 脚本**的情况下独立成立，否则「lint 通过」只是自证。因此 AT-001 里另写了一份 `_unregistered_connections()` 重新推导边界：

- RED 必须直接看到「未登记写连接 > 0」；
- 只读断言必须是**行为**的（写操作抛错），不是「代码里有 mode=ro 字样」；
- 半提交读断言必须真的构造未提交事务。

## 价值判定

- 不过时：20 处直连实测仍在，`freely_db_manager.py` 仍是唯一长期写者但已被 6 处短写者共享。
- 不重叠：R19 修的是 daemon 双实例（进程级），本条是「连接级写入方唯一性」，两者正交；R19 的 flock 让「单 daemon」成立，本条让「单写入方」可追溯。
- 高价值：`_generate_chat_id` 的注释明确假设「Single-writer daemon」，该假设此前是**假的**。

## 被否决

- **全部走 RPC**：只读 CLI 会依赖 daemon，放大故障域。
- **只加 lint**：既有读写混杂不变。
- **把 3 个辅助 store 直接删掉并合表**：需要数据迁移与兼容期，超出本条；本轮只登记 + 提供迁移路径。
- **把 `mode=ro` 改成 `immutable=1`**：会忽略 WAL 中已提交的数据，读到旧快照。
