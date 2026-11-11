# Pre-Tests: 协调契约与枚举迁出
- issue_id: I-20261104T075903Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `contracts/coordination/` 单一契约 + `scripts/runtime/coordination/` 包 + 消除 agents sys.path + lint/import 图 + 单页文档 + CI + epics-map
- acceptance_target: 协调语义有机器可读真源且 import 关系可静态分析
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: `git archive develop` 隔离基线 / 工位真源；lint 行为用临时 fixture 项目，不访问真实平台
- required_evidence: 14 静态 + 2 行为 = 16 项全 GREEN；lint 12 reasons；`test-all --ci` 17/0
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-coordination-contract.py
- test_command: python3 docs/system/workspace/scripts/tests/test-coordination-contract.py
- expected_output: SUMMARY: 16 ok, 0 failed
- expected_RED_output: SUMMARY: 1 ok, 15 failed
- actual_RED_output: develop `90abdd4f4` 基线 + 最终版 AT-001 → `1 ok, 15 failed`（AT-001-RED.log）：无契约、无 coordination 包、watchdog 仍注入 agents/ 并裸名导入、枚举仍在 agents/、无 lint/文档、AT 未进 CI、epics-map 无 story。1 项 ok 是负向守卫（coordination 包不存在时反向依赖扫描为空集）。
- actual_output: 工位同一断言 → `16 ok, 0 failed`（AT-001-GREEN.log）；`bin/check-coordination-contract` → `ok (12 reasons)`；`test-all --ci` `17 ok / 0 failed`；`check-epics-map` 16 epics / 212 stories aligned；`from coordination.input_required_reason import InputRequiredReason` 冒烟 12 个 reason。
- evidence_file: docs/B2-docs/agent-orchestration/coordination-contract/raw-20261104T075903Z/verification/test-evidence/AT-001-RED.log,docs/B2-docs/agent-orchestration/coordination-contract/raw-20261104T075903Z/verification/test-evidence/AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6
- case_design: 静态断言契约存在/可解析/四段齐全/coordination 包/agents sys.path 清零（watchdog 与整个 runtime）/包导入/legacy 删除/契约↔枚举一致/单页文档/lint 存在/import 方向/CI 接线/epics-map；行为上用临时 fixture 验证 lint 拒绝契约与枚举漂移、接受合规。
- red_how: `git archive develop | tar -x -C /tmp/r29-base`，只注入最终版 AT-001，`--source-dir /tmp/r29-base` 运行。
- implementation_findings: ①BSD grep 的 BRE `\|` 交替不支持，首轮普查误报「无 sys.path.insert」，必须用 `grep -E` 或 Python 逐行扫描；②除 watchdog 外还有 3 个 tests 文件依赖 agents sys.path，迁移后必须同步改 import，否则 `tests/test_input_required_reason.py` 直接 ModuleNotFoundError（GREEN 首轮实测抓到）；③契约用 JSON 兼容 YAML 1.2 子集，安装态无 PyYAML 也能读；④epics-map 的 `epic-agent-orchestration` 颜色要从现有 rect 动态提取，不能硬编码；⑤本阶段 task_states/exit_contracts 只记录真源，不做与实现的强校验，留待后续轮次。

## Unit

- acceptance_target: 契约↔枚举一致性、sys.path 与 import 形态的静态判定
- testing_layer: unit
- target_environment: 工位真源 + 临时 fixture 项目
- required_evidence: AT-001 静态 14 项 + lint 两个 fixture 退出码 + 包导入冒烟
- blocker_taxonomy: execution_pending_or_failed
1. `python3 docs/system/workspace/scripts/tests/test-coordination-contract.py`（16/0）
2. `python3 bin/check-coordination-contract`（12 reasons，rc=0）
3. 契约/枚举漂移 fixture → rc≠0；合规 fixture → rc=0
4. `python3 -c "from coordination.input_required_reason import InputRequiredReason"` → 12 个 reason

## Integration

- acceptance_target: 迁移不拖红既有聚合测试与回归
- testing_layer: integration
- target_environment: test-pre-merge-20261104T075903Z-coordination-contract test 工位（`test-gate run`）
- required_evidence: `test-gate` rc=0；`bin/test-all --ci` 17/0
- blocker_taxonomy: execution_pending_or_failed
1. `bin/test-all --ci`（17/0）
2. `python3 bin/check-epics-map`（16 epics / 212 stories）
3. `bash docs/system/workspace/scripts/tests/test-gate-fail-closed`、`test-verdict-contract`
4. `python3 docs/system/workspace/scripts/tests/test-skill-frontmatter-contract.py`（21/0）、`test-skill-merge-compat.py`（18/0）

## End-to-End

- acceptance_target: 真实 PR 链路上契约与导入迁移不阻断流程
- testing_layer: end-to-end
- target_environment: 本 issue 自身的 `freely pr-create-guarded` / `freely pr-review-guarded` / `freely pr-merge-guarded`
- required_evidence: PR body 含 `## RED 证据`；review Step 2.5 放行；merge 门禁通过
- blocker_taxonomy: execution_pending_or_failed
1. `freely pr-create-guarded` → 双平台 PR 创建/复用
2. `freely pr-review-guarded <branch>` → Step 2.5 对 runtime 侧变更检查 RED 证据
3. `freely pr-merge-guarded develop <branch>` → 门禁通过并合并

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 本轮改了 `watchdog_sse.py` 的导入形态（runtime 文件），但未改任何业务分支：`watchdog_sse.py` 已有的 runtime sys.path 仍能解析 `coordination` 包，包内枚举正文逐字未动；`from coordination.input_required_reason import InputRequiredReason` 已在真实工位冒烟成功（12 reasons）。合并后 followthrough 会重新打包，届时安装态可再做一次导入冒烟。pytest 在本机不可用（无该模块），故用直接导入冒烟 + 现有 `test-all --ci` 覆盖。
