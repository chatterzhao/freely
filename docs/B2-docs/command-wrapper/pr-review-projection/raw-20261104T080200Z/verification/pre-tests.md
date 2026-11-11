# Pre-Tests: pr-review-guarded 迁回 scripts/
- issue_id: I-20261104T080200Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 806 行实现移到 `scripts/worktree/pr-review-guarded`、`bin/` 变 ≤8 行投影、注册表覆盖全部超阈值入口、门禁 0/1/2、清单与后续 raw
- acceptance_target: `bin/` 回到投影层，且超阈值入口不再能静默存在
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: `git archive develop` 隔离基线 / 工位真源；门禁用临时 fixture 项目验证拒绝路径
- required_evidence: 12 静态 + 4 行为全 GREEN；`bin/check-bin-projection` rc=0；`test-all --ci` 全绿
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-bin-projection.py
- test_command: python3 docs/system/workspace/scripts/tests/test-bin-projection.py
- expected_output: SUMMARY: 16 ok, 0 failed
- expected_RED_output: SUMMARY: 1 ok, 15 failed
- actual_RED_output: develop `cad8b5875` 基线 + 最终版 AT-001 → `1 ok, 15 failed`（AT-001-RED.log）：`bin/pr-review-guarded` 仍是 806 行实现、`scripts/worktree/pr-review-guarded` 不存在、无注册表、无门禁、无清单、AT 未接线、epics 无 story；唯一 ok 是负向守卫：基线上 `bin/pr-review-guarded` 本身就是实现，无参数调用同样 fail-fast 并打印用法，所以「投影仍能分派」在基线上偶然成立，不构成迁移证据；其余 15 项全红。
- actual_output: 工位同一断言 → `16 ok, 0 failed`（AT-001-GREEN.log）；`bin/check-bin-projection` → `ok (99 bin entries, 38 registered over 40 lines)`；`check-epics-map` 对齐；`bin/pr-review-guarded` 4 行投影，实现 809 行在 `scripts/worktree/`。
- evidence_file: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261104T080200Z/verification/test-evidence/AT-001-RED.log,docs/B2-docs/command-wrapper/pr-review-projection/raw-20261104T080200Z/verification/test-evidence/AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6
- case_design: 静态 12 项（两个文件存在且可执行、投影 ≤8 行且 exec 指向真源、迁移后仍含 MAX_ROUNDS/REVIEWER_SKILL/verdict 逻辑、门禁可执行、注册表头完整、已迁移命令不在注册表、无过期条目、无永久豁免、impl 条目都挂后续 raw、清单 ≥30 行并引用 raw、双 CI 接线、epics story）；行为 4 项（真树上门禁通过、未登记超阈值被拒、过期豁免被拒、投影仍能分派到真源）。
- red_how: `git archive develop | tar -x -C /tmp/r32-base`，只注入最终版 AT-001，`--source-dir /tmp/r32-base` 运行。
- implementation_findings: ①「超 40 行就迁」是错判据——`bin/` 里有 dispatcher 与自包含工具，硬迁会造影子实现，因此用「登记 + 过期即失败」而非「一律迁移」；②新写的 `bin/check-bin-projection` 自己也 93 行，必须登记，否则门禁自指失败（已重生成注册表纳入）；③迁移只需改 `ROOT_DIR` 推导（`BASH_SOURCE` 上溯 5 层），其余 806 行逐字未动；④门禁的三条拒绝路径都用临时 fixture 项目验证，不依赖真树状态。

## Unit

- acceptance_target: 门禁三态与注册表一致性
- testing_layer: unit
- target_environment: 工位真源 + 临时 fixture 项目
- required_evidence: AT-001 静态 5–9 + 行为 13–15
- blocker_taxonomy: execution_pending_or_failed
1. `python3 bin/check-bin-projection`（rc=0）
2. 未登记超阈值 fixture → rc=1 且提示 `not registered`
3. 过期豁免 fixture → rc=1 且提示 `delete its registry entry`
4. 注册表缺失 → rc=2

## Integration

- acceptance_target: 迁移不拖红既有回归与聚合测试
- testing_layer: integration
- target_environment: test-pre-merge-20261104T080200Z-pr-review-projection test 工位（`test-gate run`）
- required_evidence: `test-gate` rc=0；`test-all --ci` 全绿；epics 对齐
- blocker_taxonomy: execution_pending_or_failed
1. `bin/test-all --ci`
2. `python3 bin/check-epics-map`
3. `bash docs/system/workspace/scripts/tests/test-gate-fail-closed`、`test-verdict-contract`
4. 既有 AT：R27 21、R28 21、R28.5 18、R29 16、R30 17、R31 16

## End-to-End

- acceptance_target: 真实 PR 链路上 `bin/pr-review-guarded` 投影仍能跑完整 review
- testing_layer: end-to-end
- target_environment: 本 issue 自身的 `freely pr-review-guarded <branch>`
- required_evidence: review gate 正常执行（返回 manual_required 或 verdict）、Step 2.5 输出、PR body 含 RED 证据
- blocker_taxonomy: execution_pending_or_failed
1. `freely pr-create-guarded` → 双平台 PR
2. `freely pr-review-guarded <branch>` → 经投影调用真源，正常输出 round 与 verdict
3. `freely pr-merge-guarded develop <branch>` → 门禁通过并合并

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 本轮唯一行为面是 `bin/pr-review-guarded` 变成投影，而该投影在本 issue 自己的 PR 流程里被真实调用（`freely pr-review-guarded` 走的就是这条路径），等于每轮都自证一次；其余 98 个入口只被「读」不被改。未改 `scripts/runtime/`，故 Step 2.5 预期 skip。
