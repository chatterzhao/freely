# Pre-Tests: 恢复 a2a_task.py CLI 可加载性
- issue_id: I-20261110T101358Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `a2a_task.py` 延迟注解求值；CLI 冒烟 AT 存在且接入 `bin/test-all`；模块可 import；`list` / `update` 返回业务错误而非 `NameError`；`SSEPool` / `_sse_pool` / `A2AClient` 仍定义；`bin/test-all --ci` 实际执行新冒烟
- acceptance_target: 派发链路 CLI 入口可用，且今后任何加载级失败都会被 CI 捕获
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 `a2a_task.py` 副本在隔离临时项目 / 临时 DB 上执行（不碰真实 `.freely/freely.db`、不访问平台、不连 A2A Server）；develop HEAD 基线快照对比
- required_evidence: 3 静态 + 5 行为共 8 项全 GREEN；基线 RED `2 ok / 6 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-a2a-task-cli-loadable.py
- test_command: python3 docs/system/workspace/scripts/tests/test-a2a-task-cli-loadable.py
- expected_output: SUMMARY: 8 ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok / 6 failed（无 future import、冒烟未接入 test-all、import/list/update 全部 NameError、SSEPool 类等未定义；2 项 PASS 是守卫：冒烟文件存在、`list` 无 server 时产出错误形状）
- actual_RED_output: develop `ab86c1b16` 基线快照注入最终版 AT-001 → `SUMMARY: 2 ok, 6 failed`（AT-001-RED.log）。关键：`module imports without NameError (rc=1, err="...NameError: name 'SSEPool' is not defined")`。
- actual_output: 工位同一断言 → `SUMMARY: 8 ok, 0 failed`（AT-001-GREEN.log）；`CLI list returns business error (got '{"error": "A2A Server not running at ...")`；`SSEPool / _sse_pool / A2AClient remain defined`。
- evidence_file: docs/B2-docs/runtime/daemon/raw-20261110T101358Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组断言模块含 `from __future__ import annotations`、冒烟文件存在、`bin/test-all` 含该测试名。行为组把模块复制到临时目录、设置 `PROJECT_ROOT` 到隔离项目，分别验证：①`import` 成功且无 NameError ②真实 CLI `list --role worker --status submitted` 无 traceback ③产出正常空/错误结果 ④真实 CLI `update --task-id fake --status launched` 无 NameError ⑤`SSEPool`/`_sse_pool`/`A2AClient` 仍定义。另实跑 `bin/test-all --ci` 确认新冒烟被选中执行。
- red_how: fix RED — `git archive develop -- bin docs .githooks templates .gitee-ci.yml .github contracts` 出 `/tmp/r23h-base`，**只**拷最终版 AT-001，以 `--source-dir /tmp/r23h-base` 运行。

## End-to-End
- acceptance_target: 真实 CLI 入口加载与业务错误返回
- testing_layer: end-to-end
- target_environment: 真实模块副本 + 隔离临时项目
- required_evidence: AT-001（行为 5 项）+ `bin/test-all --ci` 实跑
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-a2a-task-cli-loadable.py
2. bin/test-all --ci

## Unit
- acceptance_target: 静态契约与 CI 接线
- testing_layer: unit
- target_environment: fix/raw-20261110T101358Z-a2a-import-future
- required_evidence: AT-001（静态 3 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-a2a-task-cli-loadable.py

## Integration
- acceptance_target: 既有契约 / 副本 / 状态能力不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 相关回归
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
2. python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
3. python3 docs/system/workspace/scripts/tests/test-reviewer-contract.py
4. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
5. python3 docs/system/workspace/scripts/tests/test-state-key-whitelist.py
6. python3 docs/system/workspace/scripts/tests/test-raw-title-codeblock.py
7. bash docs/system/workspace/scripts/tests/test-materialize-h1 all
8. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 模块副本在临时目录执行，`PROJECT_ROOT` 指向隔离项目；A2A Server 未启动是预期状态，CLI 返回明确业务错误；不访问 GitHub/Gitee、不碰真实 `.freely/freely.db`、不派发真实 agent、不杀本机进程。develop 与安装态均做过只读 `python3 a2a_task.py list` 复核以确认缺陷真实性。
- real_environment_reason: 缺陷只在「真实 Python 解释器加载真实模块」时暴露；8 项回归 + `test-all --ci` 全绿，确认一行修复未改变任何运行时语义。既有 `test-github-label-autocreate.py` 失败经 develop 基线对比确认与本轮无关。
