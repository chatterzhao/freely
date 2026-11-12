# Pre-Tests: registry 契约测试机器无关化
- issue_id: I-20261112T015715Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `test-contract-single-source.py` 自建 stub 并注入子进程 env；干净 PATH 不带任何外部 shim 下该测试 13/0、`test-all --ci` 22/0；负向控制证明断言未变永真；产品代码与 CI 面不退化
- acceptance_target: CI 验收子集机器无关，`test-gate` 证据不再需要人工 PATH shim
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: `git archive develop` 隔离基线（RED）/ fix 工位真源（GREEN）；行为项一律在**不含 cline、不带 shim** 的干净 PATH 下执行
- required_evidence: 10 静态 + 3 行为 = 13 项全 GREEN；`test-all --ci` 22/0；`test-gate run` 不带 shim rc=0
- evidence_level: real_env
- artifact_ref: docs/system/workspace/scripts/tests/test-ci-machine-independence.py
- test_command: python3 docs/system/workspace/scripts/tests/test-ci-machine-independence.py --source-dir .
- expected_output: SUMMARY: 13 ok, 0 failed
- expected_RED_output: develop `e003532b5` 基线 + 最终版 AT-001 → `5 ok / 8 failed`：S1/S2/S3/S9/S10 与 B1/B2/B3 判红；S4/S5/S6/S7/S8 是不退化基线事实，恒绿。
- actual_RED_output: `git archive develop | tar -x -C /tmp/r335-base.*`，只注入最终版 AT-001，`--source-dir` 运行 → `SUMMARY: 5 ok, 8 failed`（rc=1，AT-001-RED.log）。首版 AT 的 S1 只检查「用了 tempfile」，而基线测试本就用 tempfile → 假绿；改为断言「私有 stub 目录」后重跑得此结果，5 项绿全部是有意义的不退化检查。
- actual_output: 干净 PATH（`command -v cline` = none，未设任何 shim）下 AT-001 → `13 ok, 0 failed`；`test-contract-single-source.py` → `13 ok, 0 failed`；`bin/test-all --ci` → `22 ok, 0 failed, known-broken=591`（AT-001-GREEN.log）。负向控制 B3 真机通过：改掉 registry 的 cline 首词后 `registry present` 判红，证明断言未变永真。
- evidence_file: docs/B2-docs/gate/ci-machine-independence/raw-20261112T015715Z/verification/test-evidence/AT-001-RED.log,docs/B2-docs/gate/ci-machine-independence/raw-20261112T015715Z/verification/test-evidence/AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7,T8
- case_design: 静态 10 项（S1 测试自建 `TemporaryDirectory` stub / S2 三处 `subprocess.run` 均带 `env=env` / S3 stub 名为 `cline` 且 chmod 0o755 / S4 无硬编码机器路径 / S5 不写 `os.environ[...]` 全局 / S6 registry missing 与 explicit --tools 两条断言仍在 / S7 `bin/deploy-skills` 与 develop 基线字节一致 / S8 `CI_CORE` 未删既有项 / S9 AT 进 `CORE` 与 `CI_CORE` / S10 epics story 存在且 `check-epics-map` ok）；行为 3 项（B1 干净 PATH 单跑 `test-contract-single-source.py` → 13/0 / B2 干净 PATH `bin/test-all --ci` → 22/0 / B3 负向控制：沙箱里把 registry 的 `cline.test_command` 首词改为绝不存在的二进制名后，`registry present` 断言必须判红，证明输出里的 cline 来自 registry 读取而非 stub 硬编码）。
- red_how: `git archive develop | tar -x -C /tmp/r335-base`，只注入最终版 AT-001，`--source-dir /tmp/r335-base` 运行；基线不含自建 stub 与 AT 接线，故静态与行为同时判红。
- implementation_findings: ①首版 AT 的 S1 只检查「用了 tempfile」，基线测试本就用 tempfile → 假绿，改为断言私有 `tool-probe-bin` stub 目录后重跑 RED；②`test-all --ci` 会调用 AT 自身导致无限递归，AT 用 `FREELY_AT_NESTED=1` 在嵌套层跳过 B2，顶层仍完整验证；③负向控制沙箱须复制 `runtime/freely`、`wt-create`、`raw_key_canon.py` 等 7 个文件，否则原测试的静态断言会连带判红造成假阳性；④stub 用 `dict(os.environ)` 拷贝而非改全局，避免异常时 PATH 泄漏；⑤`bin/deploy-skills` 与 develop 基线 sha256 一致，产品代码零改动。

## Unit

- acceptance_target: stub 的作用域与 env 注入不泄漏到其它用例；三条行为断言在同一前提下执行
- testing_layer: unit
- target_environment: fix 工位真源 + 沙箱树
- required_evidence: AT-001 静态 S1–S6 + 原测试自身 `13 ok, 0 failed`（含 registry missing fail-closed 与 explicit --tools）
- blocker_taxonomy: execution_pending_or_failed
1. `python3 docs/system/workspace/scripts/tests/test-contract-single-source.py`（13/0）
2. `python3 docs/system/workspace/scripts/tests/test-ci-machine-independence.py --source-dir .`（13/0）
3. 检查测试结束后 `os.environ["PATH"]` 未被改写（AT 静态 S5 + 进程隔离）

## Integration

- acceptance_target: 新增 AT 不拖红既有回归，三个既有门禁仍成立
- testing_layer: integration
- target_environment: test-pre-merge-20261112T015715Z-contract-test-cline-stub 工位（`test-gate run`）
- required_evidence: `test-gate` rc=0；`test-all --ci` 22/0
- blocker_taxonomy: execution_pending_or_failed
1. `bin/test-all --ci`（22/0，known-broken=591 与基线一致）
2. 七个既有 AT：R27 21、R28 21、R28.5 18、R29 16、R30 17、R31 16、R32 16、R33 20
3. `./bin/check-runtime-size`、`./bin/check-bin-projection`、`python3 bin/check-epics-map`
4. `bash docs/system/workspace/scripts/tests/test-gate-fail-closed`、`test-verdict-contract`

## End-to-End

- acceptance_target: 真实收口链路上 `test-gate run` 不再需要任何外部 shim
- testing_layer: end-to-end
- target_environment: 本 issue 自身的 `freely pr-create-guarded` / `pr-review-guarded` / `pr-merge-guarded` / `wt-close`
- required_evidence: `test-gate.env` 的 `TEST_COMMAND` 不含 shim 路径；`TEST_STATUS=completed` / `TEST_EXIT_CODE=0`；`wt-close` 的 `pretests-retirement-gate passed`
- blocker_taxonomy: execution_pending_or_failed
1. `freely test-gate run --worktree <test 工位> --command <标准命令串>`（**不带 shim**）→ rc=0
2. `freely pr-create-guarded` → `[PRETESTS-GATE] pretests execution evidence: OK ✓`
3. `freely pr-merge-guarded develop <branch>` → 合并；`wt-close` → `done ✓`

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 本机（含 login shell）`command -v cline` 为 none，GREEN 日志首行记录 `clines on PATH: none`；全程未创建、未注入任何外部 shim。测试自建的 stub 只存在于 `TemporaryDirectory` 与子进程 env 内，进程退出即清理。真机链路：干净 PATH 下 AT-001 13/0、原契约测试 13/0、`bin/test-all --ci` 22/0；`test-gate run` 不带 shim 的 rc=0 在 E2E 段验证。
