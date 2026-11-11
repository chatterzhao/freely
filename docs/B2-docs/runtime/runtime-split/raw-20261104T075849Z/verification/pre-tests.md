# Pre-Tests: runtime 拆分第一阶段
- issue_id: I-20261104T075849Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: helper 单源 + 3 个子命令外移成 `exec` 投影 + 行数守卫 + 依赖矩阵 + Rust PoC
- acceptance_target: 单体可被持续拆分且行数只降不升，外移命令行为不变
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: `git archive develop` 隔离基线 / 工位真源；行为断言用临时 git 仓库（真 branch 名）驱动 `bin/test-gate`，不 mock
- required_evidence: 12 静态 + 4 行为 = 16 项全 GREEN；单测 16 文件 98 断言；`test-all --ci` 19/0
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-runtime-split.py
- test_command: python3 docs/system/workspace/scripts/tests/test-runtime-split.py
- expected_output: SUMMARY: 16 ok, 0 failed
- expected_RED_output: SUMMARY: 0 ok, 16 failed
- actual_RED_output: develop `d33855eb0` 基线 + 最终版 AT-001 → `0 ok, 16 failed`（AT-001-RED.log）：无 `bin/test-gate`、无 `bin/evidence`、无 `lib/common.sh`、单体仍内联 9 个 helper、3 个 cmd 未投影、无行数守卫、无矩阵、无 Rust PoC、AT 未接线、epics 无 story；4 条行为因 bin 不存在全部不可执行。无空集假通过。
- actual_output: 工位同一断言 → `16 ok, 0 failed`（AT-001-GREEN.log）；`bin/check-runtime-size` → `ok (27158 lines, budget 27158)`；`unit/run.sh` → 16 文件 98 ok；`bin/test-all --ci` → `19 ok / 0 failed`（known-broken=591 与基线一致）；`check-epics-map` → 17 epics / 214 stories。
- evidence_file: docs/B2-docs/runtime/runtime-split/raw-20261104T075849Z/verification/test-evidence/AT-001-RED.log,docs/B2-docs/runtime/runtime-split/raw-20261104T075849Z/verification/test-evidence/AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7
- case_design: 静态 12 项（两个 bin 可执行、lib 定义 7 个 helper、单体 source lib、单体不再定义 7 个 helper + 2 个私有 helper、3 个 cmd 是 exec 投影、守卫与预算文件、矩阵 ≥50 行覆盖 56 个 cmd、PoC 四要素、双 CI 接线、epics story、预算 < 基线且 ≥ 实际）；行为 4 项（守卫返回真实行数、test-gate 拒绝非 test 工位且接受 test-pre-merge 并落盘 gate env、evidence 拒绝缺失文件、两个入口拒绝未知子命令）。
- red_how: `git archive develop | tar -x -C /tmp/r31-base`，只注入最终版 AT-001，`--source-dir /tmp/r31-base` 运行；快照不含本轮任何实现文件。
- implementation_findings: ①外移的真实阻塞是 helper 内联，不先建 `lib/common.sh` 就只能复制或 source 单体；②`STATE_DIR_NAME` 保留在单体（有调用方先设再用），lib 用 `${STATE_DIR_NAME:-.freely}` 兜底，避免双份真相；③`exec` 投影会替换调用进程，因此被外移命令只能以子进程方式被调用 —— 与既有 `cmd_wt_create` 一致；④R30 的接线断言是「自身为数组第一行」，插入新 AT 即变红，已改为成员判定（真实回归）；⑤`check-file-size` 对单体是 skip，行数承诺必须由专用守卫承担；⑥epics 的 epic 名必须等于 B2 目录名（本轮 `runtime` 恰好匹配）。

## Unit

- acceptance_target: 迁移后的 helper 行为等价、外移命令失败契约不变
- testing_layer: unit
- target_environment: 工位真源 + 临时 git 仓库
- required_evidence: `tests/unit/t-runtime-split-01.sh` 24 断言；unit 全量 16 文件 98 断言
- blocker_taxonomy: execution_pending_or_failed
1. `bash docs/system/workspace/scripts/tests/unit/t-runtime-split-01.sh`（24/0）
2. `bash docs/system/workspace/scripts/tests/unit/run.sh`（16 文件 98/0）
3. helper 等价：`state_dir` 兜底、`STATE_DIR_NAME` 覆盖、timestamp 形状、`log_error` 只写 stderr
4. 单体不再定义 9 个 helper；`bin/test-gate` / `bin/evidence` 的 2/1 退出码契约

## Integration

- acceptance_target: 外移后既有聚合测试与其它 AT 不退化
- testing_layer: integration
- target_environment: test-pre-merge-20261104T075849Z-runtime-split test 工位（`test-gate run`）
- required_evidence: `test-gate` rc=0；`test-all --ci` 19/0
- blocker_taxonomy: execution_pending_or_failed
1. `bin/test-all --ci`（19/0）
2. 既有 AT：R27 21/0、R28 21/0、R28.5 18/0、R29 16/0、R30 17/0
3. `python3 bin/check-epics-map`（17 epics / 214 stories）
4. `bash docs/system/workspace/scripts/tests/test-gate-fail-closed`、`test-verdict-contract`

## End-to-End

- acceptance_target: 真实 PR 链路上 runtime 变更带齐 RED 证据 + 函数级单测
- testing_layer: end-to-end
- target_environment: 本 issue 自身的 `freely pr-create-guarded` / `freely pr-review-guarded` / `freely pr-merge-guarded`
- required_evidence: PR body 含 `## RED 证据`；review Step 2.5 因改了 runtime 且已加 `tests/unit/` 单测而 **pass**（不是 skip）
- blocker_taxonomy: execution_pending_or_failed
1. `freely pr-create-guarded` → 双平台 PR，body 含 RED 证据段
2. `freely pr-review-guarded <branch>` → Step 2.5 `pass: N runtime file(s), 1 unit test(s)`
3. `freely pr-merge-guarded develop <branch>` → 门禁通过并合并

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 本轮改的是 runtime 的**加载结构**（helper 移入 lib、3 个命令变投影），不是业务分支：真机冒烟已证明 `freely --help` 正常加载、`test-gate record` 对非 test 工位仍 rc=2、对 test-pre-merge 工位仍写 gate env、`evidence add` 仍拒绝缺失文件、未知子命令仍 exit 1。`bin/freely` 的「可执行 + 可 source」双身份由 4 个 source 脚本继续使用，未改其调用方式。合并后 followthrough 会重新打包安装态，届时可在安装版本上再跑一次 `bin/check-runtime-size` 与 `freely test-gate --help`。
