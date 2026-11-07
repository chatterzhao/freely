# Pre-Tests: 读失败显式标记，健康路径零变化
- issue_id: I-20261105T122053Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 两平台健康时 `list_open_issue_records()` 返回纯 107 条字典、结构与记录字段不变、无额外键；单平台或全部平台读失败时结果含 `__degraded__` 且点名平台与错误、保留可读平台记录；handler 异常不产生假记录或 TypeError；scan 的 `get_platform_open_issues()` 能产出 `__degraded__` 且既有降级消费者工作；parity 降级时 SKIP + 重试提示、不报假差异，健康时仍正常比较；REST 回退保留
- acceptance_target: 平台故障与平台无 open issue 在结果里可区分，扫描不基于部分清单误判生命周期
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离 fake handler + 真实双平台读取
- required_evidence: 新增回归测试 9 项全 GREEN + 13 个回归全 PASS + 12 个基线对比零新增失败 + 真实双平台健康路径无标记
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-open-list-read-degraded.py
- test_command: python3 docs/system/workspace/scripts/tests/test-open-list-read-degraded.py
- expected_output: Ran 9 tests ... OK
- expected_RED_output: Ran 9 tests ... FAILED (failures=5)
- actual_RED_output: 未修改 develop HEAD 基线 RED 5 项失败 —— 单平台/全部平台失败无 `__degraded__`、handler 无 read_health、异常被 `_safe` 转成 error 对象后 `**record` 抛 TypeError、parity 报出假差异；4 项既有能力保持 PASS（健康 107 条、scan 既有消费者、scan 产出标记、parity 健康比较）（AT-001-RED.log）
- actual_output: Ran 9 tests ... OK；`__degraded__` 含 platform/platforms/error/ok/partial；真实双平台健康路径 102 条（github=52, gitee=50）无标记（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/platform/issue-parity/raw-20261105T122053Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6
- case_design: fake handler 注入 57 GitHub + 50 Gitee 记录验证健康路径结构与键格式；注入 read_health ok=False / 抛异常 / 全平台失败验证降级标记与不产生假记录；加载真实 scan 模块并 mock `_get_pa` 验证 `get_platform_open_issues()` 透传 `__degraded__`；加载真实 parity 模块并 mock handlers 验证降级 SKIP 与重试提示；另用真实双平台读取验证健康路径无标记。
- red_how: fix RED — 用 `git show HEAD:<file>` 把 2 个真源还原到未修改 develop 状态后运行同一断言组，确认读失败被压成干净空清单。

## Unit
- acceptance_target: read_health 契约、聚合层降级标记、异常不产生假记录
- testing_layer: unit
- target_environment: fix/raw-20261105T122053Z-open-list-degraded
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-open-list-read-degraded.py AggregatorTests

## Integration
- acceptance_target: R1..R6.5、Q1/Q2、降级语义、四态/反查/恢复不退化
- testing_layer: integration
- target_environment: 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
2. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir all
3. python3 docs/system/workspace/scripts/tests/test-raw-issue-pull-platform-fallback.py

## End-to-End
- acceptance_target: 真实双平台健康路径与 scan/parity 降级语义
- testing_layer: end-to-end
- target_environment: 真实 fix 工位（不触网 mock + 一次真实双平台读取）
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-open-list-read-degraded.py ScanTests
2. python3 docs/system/workspace/scripts/tests/test-open-list-read-degraded.py ParityTests

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实 fix 工位以项目真源命令执行；R2 物化 H1 自举生效；真实双平台 `list_open_issue_records()` 返回 102 条且无 `__degraded__`；2 个真源还原到未修改 develop HEAD 做基线对比，12 个相关回归退出码逐一相同（全 0），输出差异仅计时数字 → 0 新增失败；bin/check-epics-map 对齐通过；双平台 raw 副本用封装命令关闭、三份 fingerprint 一致。
