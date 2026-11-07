# Pre-Tests: pull 按可用平台回退并复用 sync-debt 记账
- issue_id: I-20261104T082549Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 单平台不可读时 raw-issue-pull 仍能从另一个可读平台物化；`--platform` / `--source-platform` 可显式指定读源并写回 primary_platform 与 platform_ids；未读平台记入既有 sync-debt 账本且不阻断工位创建；部分成功退出码为 3 而非 1；全部不可读仍 FATAL；显式指定不可读平台失败而不静默回退；双平台都 ok 时行为不变；stdout 恰好一个 JSON 文档
- acceptance_target: 双平台真正互为备份，网络抖动不再让工位创建全停
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离 git 项目 + fake adapter（不触网）
- required_evidence: 新增回归测试 12 项全 GREEN + 12 个回归全 PASS + 11 个基线对比零新增失败
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-raw-issue-pull-platform-fallback.py
- test_command: python3 docs/system/workspace/scripts/tests/test-raw-issue-pull-platform-fallback.py
- expected_output: Ran 12 tests ... OK
- expected_RED_output: Ran 12 tests ... FAILED (failures=9)
- actual_RED_output: 未修改 develop HEAD 基线 RED 9 项失败 —— github unreadable 时 pull FATAL；无 --platform / --source-platform；无 degraded_platforms 与 sync-debt 记账；无部分成功退出码 3；3 项既有能力保持 PASS（双平台 ok 时 primary 不变、全不可读仍 FATAL、物化 H1 与身份不变）（AT-001-RED.log）
- actual_output: Ran 12 tests ... OK；partial 从 gitee 物化、platform_ids 不含 github、`--platform gitee` 写回 primary_platform、显式不可读平台 fail-closed、CLI 退出码 3、stdout 单一 JSON、sync-debt 落账（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261104T082549Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7
- case_design: unittest + mock.patch 直接注入 discover_raw_replicas 的 ok/unknown 副本，覆盖默认回退、显式指定、显式不可读、全不可读、双平台 ok 不退化、R2 H1 与身份；static 断言 CLI 参数透传与 sync-debt 复用；退出码用隔离 git 项目 + fake adapter 真实执行 `bin/raw-issue-pull`，断言 returncode==3、stdout 可 json.loads、账本出现 raw-key::github 条目；wt-create 继续语义用隔离 shell 检查与端到端链路验证。
- red_how: fix RED — 用 `git show HEAD:<file>` 把 3 个真源还原到未修改 develop 状态后运行同一断言组，确认单平台故障即全停。

## Unit
- acceptance_target: 可用平台选择、显式指定、platform_ids 收窄、既有能力不退化
- testing_layer: unit
- target_environment: fix/raw-20261104T082549Z-pull-platform-fallback
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-raw-issue-pull-platform-fallback.py

## Integration
- acceptance_target: R1..R5.5、Q2、既有降级语义与 wt-create 工位能力不退化
- testing_layer: integration
- target_environment: 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
2. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir all
3. bash docs/system/workspace/scripts/tests/test-materialize-h1 all

## End-to-End
- acceptance_target: CLI 部分成功退出码 3、stdout 单一 JSON、sync-debt 落账、wt-create 继续
- testing_layer: end-to-end
- target_environment: 隔离 git 项目（不触网）
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-raw-issue-pull-platform-fallback.py PullFallbackTests.test_partial_success_has_distinct_exit_code_3

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实 fix 工位以项目真源命令执行；R2 物化 H1 自举生效；3 个真源还原到未修改 develop HEAD 做基线对比，11 个相关回归退出码逐一相同（全 0），输出差异仅计时数字 → 0 新增失败；隔离 git 项目端到端验证 CLI 退出码 3 / stdout 单一 JSON / sync-debt 落账 / wt-create 继续；bin/check-epics-map 对齐通过；双平台 raw 副本用封装命令关闭、三份 fingerprint 一致。
