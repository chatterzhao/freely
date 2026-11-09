# Pre-Tests: `runtime/freely` 被 source 时无副作用
- issue_id: I-20261103T132605Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: source `runtime/freely` 不改变调用方 shell 选项、缺库时返回可判定错误而非杀掉调用方、库加载段无 `exit` 字面量、直接执行仍以 1 退出、`stop_project_runtime` 用返回码
- acceptance_target: 4 个控制面脚本（watchdog / dispatcher / promotion gate / supervisor）在库缺失时能自己决定降级，而不是整进程退出
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 临时 5 层目录沙箱（使 `SELF_ROOT` 指向沙箱根）+ 真实 `freely` 副本 + 真实 `bash` 子进程；develop HEAD 基线快照对比
- required_evidence: 2 静态 + 4 行为共 6 项全 GREEN；基线 RED `1 ok / 5 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-source-safe-library.py
- test_command: python3 docs/system/workspace/scripts/tests/test-source-safe-library.py
- expected_output: SUMMARY: 6 ok, 0 failed
- expected_RED_output: SUMMARY: 1 ok / 5 failed（前 70 行 2 处 `exit 1`；`freely_stop` 用 `|| exit 1`；隔离夹具里 source 无输出即失败；sourcing 改变 shell 选项；缺库杀掉调用方。1 项 PASS 是「直接执行仍 rc=1」——行为未变）
- actual_RED_output: develop `9618a0f34` 基线快照注入最终版 AT-001 → `SUMMARY: 1 ok, 5 failed`（AT-001-RED.log）。关键：`found [(34, 'exit 1'), (41, 'exit 1')]`；happy-path source 输出为空（进程被顶层 exit 终止）。
- actual_output: 工位同一断言 → `SUMMARY: 6 ok, 0 failed`（AT-001-GREEN.log）：`OPTIONS_UNCHANGED`、`SURVIVED rc=1 err=missing watchdog availability module`。
- evidence_file: docs/B2-docs/runtime/daemon/raw-20261103T132605Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组断言前 70 行无 `^\s*exit [0-9]`、`freely_stop` 分支为 `|| return 1`。行为组在临时 5 层目录放 `freely` 副本（使 `SELF_ROOT` 落在沙箱），分别验证：happy path 能 source 且无错误变量；`set +o` 前后一致；删掉库后 source 返回非零且调用方 shell 存活；直接执行该副本缺库仍 rc=1。
- red_how: fix RED — `git archive develop -- bin docs .githooks templates .gitee-ci.yml .github` 出 `/tmp/r21-base`，把最终版 AT-001 拷入快照 tests 目录，以 `--source-dir /tmp/r21-base` 运行。

## End-to-End
- acceptance_target: 真实 bash 子进程里的 source 语义
- testing_layer: end-to-end
- target_environment: 临时 5 层沙箱 + 真实 `freely` 副本
- required_evidence: AT-001（行为 4 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-source-safe-library.py

## Unit
- acceptance_target: 库加载段静态契约
- testing_layer: unit
- target_environment: fix/raw-20261103T132605Z-no-toplevel-exit
- required_evidence: AT-001（静态 2 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-source-safe-library.py

## Integration
- acceptance_target: 既有 source 调用方与全量测试不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 相关回归
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-close-comment-scan
2. bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2
3. python3 docs/system/workspace/scripts/tests/test-concurrency-singletons.py
4. python3 docs/system/workspace/scripts/tests/test-db-single-writer.py
5. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 测试只 source `freely` 的副本，不启动 daemon、不写真实 `.freely/run`；真实环境只做只读核对（`bash -n` + 4 个调用方语法）。
- real_environment_reason: 该缺陷只在「其他脚本 source 本库」时暴露，必须在真实 bash 子进程里验证；本轮 `bin/test-all --ci`、`test-concurrency-singletons.py`、`test-db-single-writer.py`、`test-issue-sync-promote-b2`、`test-wt-close-comment-scan` 全绿，说明 sourced 语义变化未影响既有调用方。
