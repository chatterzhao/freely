# Implementation Decision Note
- issue_id: I-20261104T075903Z-A
- issue_path: docs/B2-docs/agent-orchestration/coordination-contract/raw-20261104T075903Z/issues/I-20261104T075903Z-A.md
- decision: 新增 `contracts/coordination/contract.yaml` 与单页文档；枚举从 `agents/` 迁入 `scripts/runtime/coordination/`；watchdog 与 3 个测试改包导入、清除 agents sys.path；新增 `bin/check-coordination-contract` 守护契约↔枚举一致、sys.path、import 方向；AT 进 CI、epics-map 注册 story。
- why_this: 协调语义没有机器可读真源，且 reason 枚举靠 sys.path hack 才能 import，新增 reason 会跨 6 处漂移；先做零业务语义变化的契约与迁移，给后续 server/client/router 收敛留出可机检的落点。
- alternatives_considered: ①按 issue 原方案一次性把四个运行时文件搬进单一实现——重写面过大、RED/GREEN 证据难以收敛，否决；②保留 `agents/input_required_reason.py` 作为 shim——两份真相或额外 sys.path，否决；③只写文档不迁移——sys.path 与漂移仍在，否决。
- boundary_non_goals: 不改 a2a_types/a2a_server/a2a_task；不改 `manager_exit_contract_kind` 逻辑；不改 workflow 全链路；不把 task_states/exit_contracts 与实现做强校验（本阶段只记录真源）；不改三个测试的任何断言。
- residual_risk: ①契约的状态机/topics/exit 值来自真源人工提取，后续要做机器校验；②server/client/router 收敛、角色 schema 待后续轮次；③三个测试有重复 runtime sys.path 行（无害）；④本机无 pytest，用直接导入冒烟 + `test-all --ci` 覆盖。

## BSD grep 坑（复用）

本机 BSD grep 的 BRE `\|` 交替不生效，首轮 `grep -n "sys.path.insert\|input_required_reason"` 返回空，
差点把「issue 描述过时」当成前置评审结论。凡是用到交替、或多关键字扫描，一律 `grep -E` 或 Python 逐行。
