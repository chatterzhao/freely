# Tasks: 协调契约与枚举迁出
- issue_id: I-20261104T075903Z-A
- pre_tests_path: docs/B2-docs/agent-orchestration/coordination-contract/raw-20261104T075903Z/verification/pre-tests.md

## 任务分解

- [x] T1: `wt-create --raw-key raw-20261104T075903Z --source platform --kind feature` 建 dev/test 工位；真源普查（修正 BSD grep 误判，确认 watchdog 两处 sys.path）。
- [x] T2: 前置评审把 5 步大重构收敛为第一阶段；写 AT-001（14 静态 + 2 行为）；develop `90abdd4f4` 基线 RED `1 ok / 15 failed`。
- [x] T3: `contracts/coordination/contract.yaml` + 单页 README（状态机/reasons/topics/exit contracts + 真源标注）。
- [x] T4: 枚举迁入 `scripts/runtime/coordination/`，删除 `agents/input_required_reason.py`；watchdog 去 agents sys.path 并改包导入。
- [x] T5: GREEN 首轮抓到 3 个 tests 文件仍依赖旧裸导入 → 同步迁移 sys.path 与 import，直接导入冒烟验证 12 reasons。
- [x] T6: 新增 `bin/check-coordination-contract`（0/1/2）；AT 进 CORE/CI_CORE；epics-map 注册 `coordination-contract` story。
- [x] T7: GREEN `16 ok / 0 failed`；lint 12 reasons；`test-all --ci` 17/0；epics-map 16/212。
- [x] T8: server/client/router 收敛与角色 schema 标注为后续轮次，不夹带进本 PR。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001（RED fidelity） |
| T3 | AT-001（静态 1–3、10） |
| T4, T5 | AT-001（静态 4–9）+ 冒烟 |
| T6 | AT-001（静态 11、14–16 + 行为 12–13） |
| T7, T8 | 回归/CI 与范围标注 |
