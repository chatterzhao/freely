# Pre-Tests: 关闭路径先校验后执行，部分成功独立退出码
- issue_id: I-20261104T082603Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 非终态 raw 执行 close 必须退出非零且**零平台调用**（平台状态不变、frontmatter 不变）；终态 raw 全平台成功才落 `platform_state=closed` 并退出 0；部分成功退出 3 且不落本地状态、逐平台 status 可读；全失败退出 1 且不落本地状态；adapter `close-multi`/`close-raw` 与 `create-issue` 同口径 0/3/1；非严格路径（I-*）任一平台失败不得写 `platform_state=closed`
- acceptance_target: 让「平台已关、本地未关」在结构上不可能发生，并让「部分成功」既不被伪装成成功也不被伪装成全部失败
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离夹具项目树（stub `platform-adapter.py` 作为唯一平台边界）+ 真实 `raw_lifecycle_effects.py` 与真实 `bin/issue-sync` + develop HEAD 基线快照对比
- required_evidence: 新增回归测试 10 项静态断言 + 17 个行为场景全 GREEN；6 个相关回归基线对比退出码全 MATCH；真实仓库上由本轮 `wt-close` 以终态 raw 真实执行同一命令面闭环
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first
- test_command: bash docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first all
- expected_output: SUMMARY: 27 ok, 0 failed
- expected_RED_output: SUMMARY: 11 failed（静态 7：close_platforms 顺序 MISORDERED、终态错误不带 current phase、adapter 无 `_close_exit_code`、关闭记账 0 次使用、issue-sync 压掉 effect 退出码、无 partial 分支、legacy 路径无条件写 closed；行为 4：非终态仍调用平台 adapter、adapter 记账探针崩、issue-sync 部分成功 rc=1、issue-sync 非终态先关平台）
- actual_RED_output: develop HEAD `04afa025d` 基线快照（`git archive develop -- bin docs`）内放入**最终版** AT-001 运行 —— `SUMMARY: 16 ok, 11 failed`（AT-001-RED.log）。逐项：静态 7 项全 FAIL；`non-terminal close still called the platform adapter: close-multi {...}`（核心缺陷：先关平台后校验）；`adapter accounting probe crashed`；`issue-sync rc=1 (want 3)`；`issue-sync closed platforms first`
- actual_output: 工位运行同一份断言 —— 静态 10 项全 ok、行为 17 项全 ok，`SUMMARY: 27 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/platform/raw-20261104T082603Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,AT-001-REGRESSION-BASELINE.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7
- case_design: 行为组把**真实** `raw_lifecycle_effects.py` 指向隔离 root，root 内的 `platform-adapter.py` 是 stub（记录调用参数、按环境变量输出逐平台 JSON 与退出码），因此「有没有真的去关平台」可被断言为「stub 是否被调用」；`issue-sync` 组用 `BASH_SOURCE` 守卫把真实脚本作为库加载（`set +e` 以观察真实退出码）驱动 `cmd_close`；adapter 组用 importlib 直接调用 `_close_exit_code` 验四类映射。
- red_how: fix RED — `git archive develop -- bin docs` 出基线快照，把最终版 AT-001 拷入后运行，基线文件一个不改。

## Unit
- acceptance_target: 静态契约（四段式顺序、单一记账、禁止无条件自证、语法可解析）
- testing_layer: unit
- target_environment: fix/raw-20261104T082603Z-issue-sync-close-terminal-first
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first static

## Integration
- acceptance_target: 写通道、元数据生命周期、reconciliation、parity、handler probe、wt-close 既有能力不退化
- testing_layer: integration
- target_environment: 工位 + 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-platform-write-channel
2. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
3. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
4. python3 docs/system/workspace/scripts/tests/test-platform-open-parity.py
5. python3 docs/system/workspace/scripts/tests/test-platform-handler-probe.py
6. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-wt-close.py

## End-to-End
- acceptance_target: 真实脚本 + 真实 issue-sync 在非终态与部分成功两种场景下的退出码与落盘
- testing_layer: end-to-end
- target_environment: 隔离夹具项目树（stub 仅替换平台边界）
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first behavior

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 链路中只有平台边界（`platform-adapter.py`）被 stub 替换，`raw_lifecycle_effects.py`、`raw_metadata_contract.py`、`bin/issue-sync` 都是真实文件真实执行；6 个相关回归以未修改 develop 基线对比退出码全 MATCH（`test-command-lifecycle-wt-close.py` 的 1 项失败为预存红，基线同样失败、失败用例名与断言完全一致）。真实平台写不在测试中触发（避免污染真实 issue），改由本轮 `wt-close --raw-key` 在**本 issue 自身**上以终态 raw 真实跑通同一命令面闭环（absorbed → 双平台 close → `platform_state=closed`），这是同一段代码的真实执行证据，记录在 GREEN 证据与收口摘要中。
