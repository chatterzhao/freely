# Pre-Tests: 跨进程数据契约（第一阶段）
- issue_id: I-20261104T075857Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `contracts/cross-process/` 声明 state 协议/错误信封/退出码/超时语义/边界；`cross_process_boundary.py` 实现三态边界；`bin/check-cross-process-contract` 守护漂移；AT 进 CI；epics-map 注册 story
- acceptance_target: 三类跨边界失败（缺字段/类型错/超时）在机器上可区分且 fail-closed
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: `git archive develop` 隔离基线 / 工位真源；三条边界用真实子进程（`sh printf`、`sleep`）驱动 runner，不 mock、不访问网络
- required_evidence: 14 静态 + 3 行为 = 17 项全 GREEN；lint `ok (4 boundaries)`；`test-all --ci` 18/0
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-cross-process-contract.py
- test_command: python3 docs/system/workspace/scripts/tests/test-cross-process-contract.py
- expected_output: SUMMARY: 17 ok, 0 failed
- expected_RED_output: SUMMARY: 0 ok, 17 failed
- actual_RED_output: develop `c159e6cef` 基线 + 最终版 AT-001 → `0 ok, 17 failed`（AT-001-RED.log）：无 `contracts/cross-process/`、无 runner、无 lint、AT 未进两个 CI 列表、epics-map 无 story，三条边界行为因 runner 不存在全部不可执行。0 ok 表示没有任何一条是空集假通过。
- actual_output: 工位同一断言 → `17 ok, 0 failed`（AT-001-GREEN.log）；`bin/check-cross-process-contract` → `ok (4 boundaries)` rc=0；`test-all --ci` `18 ok / 0 failed`；`check-epics-map` 对齐。
- evidence_file: docs/B2-docs/data-contracts/cross-process-contract/raw-20261104T075857Z/verification/test-evidence/AT-001-RED.log,docs/B2-docs/data-contracts/cross-process-contract/raw-20261104T075857Z/verification/test-evidence/AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6
- case_design: 静态 14 项：契约存在/可解析/schema/state_file 五段/error_model 五个退出码与四个信封字段/timeout exit_code=4 且 distinguishable/≥3 条边界字段齐全/kind 覆盖三类/README 文档/lint 可执行/runner CLI/AT 双 CI 接线/epics-map story/退出码与 `REFUSE_EXIT=3` 交叉一致。行为 3 项：缺字段 → rc3+`missing_field`、类型错 → rc3+`type_error`、超时 → rc4+`timeout`。
- red_how: `git archive develop | tar -x -C /tmp/r30-base`，只注入最终版 AT-001，`--source-dir /tmp/r30-base` 运行；快照不含本轮任何实现文件。
- implementation_findings: ①`values()` 对缺失 key 返回空字符串是本族问题的根，但改 `state_file.py` 属 runtime（会触发 R27 单测门禁），因此本轮以「声明 + runner」兜住，`state_file.py` 一行未改；②超时必须是 4 而不是 3，否则「答错」和「太慢」仍不可区分，AT 的 b17 与 c06/c14 三处交叉断言；③契约的 `3` 必须与 `pr_body.REFUSE_EXIT = 3` 同义，`2` 与 check-* 的「真源缺失」同义，否则新契约自成一套编号；④RED 用 `0 ok` 而不是「部分 ok」，是因为三条行为断言依赖 runner 存在，天然全红，不存在空集假通过。

## Unit

- acceptance_target: 契约字段完整性、退出码常量一致性
- testing_layer: unit
- target_environment: 工位真源
- required_evidence: AT-001 静态 14 项 + lint rc=0
- blocker_taxonomy: execution_pending_or_failed
1. `python3 docs/system/workspace/scripts/tests/test-cross-process-contract.py`（17/0）
2. `python3 bin/check-cross-process-contract`（4 boundaries，rc=0）
3. `python3 bin/check-cross-process-contract --json` → `{"ok": true, "errors": []}`

## Integration

- acceptance_target: 新增 AT 进聚合测试且不拖红既有回归
- testing_layer: integration
- target_environment: test-pre-merge-20261104T075857Z-cross-process-contract test 工位（`test-gate run`）
- required_evidence: `test-gate` rc=0；`bin/test-all --ci` 18/0
- blocker_taxonomy: execution_pending_or_failed
1. `bin/test-all --ci`（18/0）
2. `python3 bin/check-epics-map`（16 epics / 213 stories）
3. `bash docs/system/workspace/scripts/tests/test-gate-fail-closed`、`test-verdict-contract`
4. 既有 AT 回归：R27 21/0、R28 21/0、R28.5 18/0、R29 16/0

## End-to-End

- acceptance_target: 真实 PR 链路上契约与 runner 不阻断流程
- testing_layer: end-to-end
- target_environment: 本 issue 自身的 `freely pr-create-guarded` / `freely pr-review-guarded` / `freely pr-merge-guarded`
- required_evidence: PR body 含 `## RED 证据`；review Step 2.5 对非 runtime diff 输出 skip；merge 门禁通过
- blocker_taxonomy: execution_pending_or_failed
1. `freely pr-create-guarded` → 双平台 PR 创建/复用，body 含 RED 证据段
2. `freely pr-review-guarded <branch>` → Step 2.5 输出 `skip: diff does not touch the core runtime`
3. `freely pr-merge-guarded develop <branch>` → 门禁通过并合并

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 本轮不改 `docs/system/workspace/scripts/runtime/`、不改 `bin/freely`，所以运行时行为零变化；三条边界断言用真实子进程跑真机可执行文件（`/bin/sh` + `sleep`），不是 mock；新增文件只被 AT 与 lint 消费。合并后 followthrough 重新打包，届时安装态可直接跑 `bin/check-cross-process-contract` 复核。
