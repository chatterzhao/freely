# Brainstorms: 收口 agent 协调的协议、状态机与路由决策

- source_raw: raw-20261104T075903Z
- 覆盖域：协议类型/客户端/路由订阅/决策逻辑/理由枚举/角色真相 6 处；契约、单一实现包、sys.path 消除、import 图、单页文档。

## 真源普查（不照 issue 旧行号改）

- `runtime/watchdog_sse.py:15-16` **确实**有两处 `sys.path.insert`，第二条指向 `agents/`。
  第一次普查用 BSD grep 的 BRE `\|` 交替（本机不支持）误报为空，改用 `grep -E` / Python 逐行扫描才确认 —— **这个坑本会话已踩多次，必须记住**。
- `agents/input_required_reason.py` 被 `watchdog_sse.py:25` 以裸模块名 `from input_required_reason import` 导入；另有 `tests/test_input_required_reason.py`、`test_watchdog_sse.py`、`test_integration_lifecycle.py` 三处同样依赖 agents sys.path。
- `contracts/` 只有 `config/schema.yaml`，协调语义没有任何机器可读契约。
- `manager_exit_contract_kind()` 在 `runtime/freely:16172`，`delegate_workers` 等 exit kind 散在函数体里。

## 前置评审：issue 的 5 步方案过大

「建 `scripts/coordination/` 单一实现，server/client/router/决策全部搬过去」会重写
a2a_types(435) / a2a_server(920) / a2a_task(1165) / watchdog_sse(562) 四个运行时文件，
且每轮 PR 都要求 RED→GREEN 证据，风险不可控。按 R22/R23.5/R28 的 scope 收敛先例，
本轮做**第一阶段**：契约 + 枚举迁出 + sys.path 消除 + lint/import 图 + 单页文档；
server/client/router 收敛与角色 schema 拆后续轮次。

## Decision

1. `contracts/coordination/contract.yaml`（JSON 兼容 YAML 1.2 子集）：task_states / 12 个 input-required reasons / SSE topics / exit_contracts，并标注每段真源。
2. 枚举从 `agents/` 迁到 `scripts/runtime/coordination/`（同 runtime 目录，`watchdog_sse.py` 已有的 runtime sys.path 即可导入）。
3. 删除 agents 的 sys.path 行，watchdog 改包导入；三个测试的 sys.path / import 同步迁移。
4. `bin/check-coordination-contract`：契约↔枚举一致、agents sys.path 为 0、coordination 不反向 import runtime/freely、watchdog 走包导入；0/1/2。
5. 单页文档 `contracts/coordination/README.md`；AT 进 CORE/CI_CORE；epics-map 注册 story。

## 验收标准核对

- `grep -rn "sys.path.insert.*agents"` 为 0：**达成**（runtime 与 tests 均清零；历史 B1/B2 研发留痕里没有该字符串组合）。
- 新增 reason 只需改契约 + 一处枚举（diff ≤2）：**达成**（lint 保证两者一致，无第三处硬编码）。
- import 图无反向依赖：**达成**（lint 静态扫描 coordination 包）。
- 单页文档列出状态机与 exit contract 合法值：**达成**。
