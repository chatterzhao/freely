# Pre-Tests: 安装态自检一等入口 + 文档对齐

- issue_id: I-20261114T080106Z-A

## Acceptance Items

### acceptance-1

- id: AT-001
- requirement: `./bin/install-state-check --json` 存在且逐字转发真源；不一致时 rc≠0/ok:false 并给出修复命令；commands.md 与 goal 命令写法一致；runtime/freely 行数不变且无 dispatch 行；薄投影不复制判定逻辑；基线红
- acceptance_target: 吃狗粮前提可按文档照抄地自检
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实执行薄投影与真源脚本（相同 cwd/env），临时空 home 构造不一致
- required_evidence: AT-001 GREEN 15/0；基线 4/7
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-install-state-cli.py
- test_command: python3 docs/system/workspace/scripts/tests/test-install-state-cli.py
- expected_output: SUMMARY: 15 ok, 0 failed
- expected_RED_output: SUMMARY: 4 ok, 7 failed
- actual_RED_output: develop 7cf9dabf6 无 `bin/install-state-check`、commands.md 无该命令写法；S1/S3/S4/S5/S8–S10 红、行为组因缺投影跳过（AT-001-RED.log）
- actual_output: SUMMARY: 15 ok, 0 failed；S6/S7 证明 runtime 预算未动、B1 证明 JSON 与真源逐字一致、B3–B5 证明不一致被拒绝并给出修复命令（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/platform/issue-sync-entrypoint/raw-20261114T080106Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ''
- task_refs: T1,T2,T3
- case_design: 静态断言薄投影 ≤40 行、含真源路径、不含 `install_state` 判定逻辑、runtime 行数 ≤27158 且无 dispatch 行、commands.md 含正确命令与预算理由；行为组在相同 cwd 下对比投影与真源的 `--json` 输出，并用空 `--home` 构造不一致场景。
- red_how: fix RED — `git archive develop` 导出基线树，用 `--source-dir` 运行同一 AT。

## Unit

- acceptance_target: 薄投影结构
- testing_layer: unit
- target_environment: fix/raw-20261114T080106Z-install-state-cli
- required_evidence: AT-001 S1–S10
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-install-state-cli.py

## Integration

- acceptance_target: 既有打包/CI 不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；check-bin-projection / check-runtime-size / projections verify 均绿
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End

- acceptance_target: 下一轮开工前按 goal 自检
- testing_layer: end-to-end
- target_environment: 下一轮开工
- required_evidence: `./bin/install-state-check --json` → ok:true 且 project_head == develop
- blocker_taxonomy: execution_pending_or_failed
1. 下一轮开工前自检

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 用户要求「打包安装，不然吃狗粮可能吃到过期的」时实测撞到 `./bin/freely install-state-check` → unknown command；本轮修通后同一命令改为 `./bin/install-state-check --json` 并实测 ok:true（project_head = packaged_from = 7cf9dabf6）。
