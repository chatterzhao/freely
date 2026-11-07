# Pre-Tests: issue-sync 能找到 B2 文档，promote 不再必然失败
- issue_id: I-20261104T082556Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: B2 的 I-* 文档可被 `cmd_create` 创建（双平台 id 回写、不注入 `platform_state`）；`cmd_promote` 对 B2 目标成功（children + 平台建单 + promoted_from 注释）；文档缺失 rc≠0 且列出检查位置；同名两份 rc≠0 且列出候选；`bin/issue-sync` 无 B1 硬编码；`cmd_promote` 走共享解析器
- acceptance_target: B1→B2 平台同步链路可用，文档定位与布局无关且歧义 fail-closed
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离夹具项目树（stub `gh` + stub `gitee-issue.py`，真实 `bin/issue-sync`、真实生命周期模块）+ develop HEAD 基线快照对比
- required_evidence: 8 项静态断言 + 15 个行为场景全 GREEN；7 个相关回归基线对比退出码全 MATCH；真机：本轮 absorb 用修好的 `issue-sync promote` 完成
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-issue-sync-promote-b2
- test_command: bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2 all
- expected_output: SUMMARY: 23 ok, 0 failed
- expected_RED_output: SUMMARY: 16 failed（静态 6：无 `_issue_file_for`、5 处 B1 硬编码、promote 前缀搜索、`platform_state` 无条件写、无共享评论读取、仍依赖 `## Comments` 段落；行为 10：B2 create rc=1、platform_ids 空、promote rc=1、children 空、无 promoted_from、缺失/歧义错误信息不含检查位置与候选、系统事件评论未推到双平台）
- actual_RED_output: develop `d3751870a` 基线快照（`git archive develop -- bin docs`）内放入**最终版** AT-001 —— `SUMMARY: 7 ok, 16 failed`（AT-001-RED.log）：`no _issue_file_for resolver`、`5 command(s) still hard-code the B1 path`、`cmd_promote still prefix-searches the B2 tree`、`platform_state is written unconditionally`、`cmd_create on a B2 document rc=1: [ERROR] .../docs/B1-docs/I-.../issue.md not found`、`promote rc=1` 等
- actual_output: 工位同一断言 —— `SUMMARY: 23 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/platform/raw-20261104T082556Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,AT-001-REGRESSION-BASELINE.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7
- case_design: 夹具建一棵最小项目树（B1 raw + B2 I-* + stub 平台 CLI），把真实 `bin/issue-sync` 作为库加载后调用真实命令；`RAW_METADATA_CONTRACT_ROOT` 指向真实仓库以使用真实生命周期模块，`ROOT_DIR` 指向夹具以隔离文件写入；命令以子 shell 执行以便捕获 `exit` 后的真实退出码。
- red_how: fix RED — `git archive develop -- bin docs` 出基线快照，把最终版 AT-001 拷入后运行，基线文件一个不改。

## Unit
- acceptance_target: 静态契约（解析器存在、无 B1 硬编码、promote 走解析器、platform_state 条件写、语法）
- testing_layer: unit
- target_environment: fix/raw-20261104T082556Z-promote-b2-issue-file
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2 static

## Integration
- acceptance_target: 写通道、关闭路径、test-gate、raw 元数据、reconciliation、parity、wt-close 不退化
- testing_layer: integration
- target_environment: 工位 + 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-platform-write-channel
2. bash docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first
3. bash docs/system/workspace/scripts/tests/test-test-gate-record
4. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
5. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
6. python3 docs/system/workspace/scripts/tests/test-platform-open-parity.py
7. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-wt-close.py

## End-to-End
- acceptance_target: B2 文档的 create / promote / 缺失 / 歧义四类真实行为
- testing_layer: end-to-end
- target_environment: 隔离夹具项目树（stub 仅替换平台边界）
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2 behavior

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 平台侧创建/关闭在测试中用 stub 覆盖；真实写由本轮自身生命周期完成。
- real_environment_reason: 只有平台 CLI 被 stub 替换，`bin/issue-sync` 与生命周期模块都是真实文件真实执行；7 个相关回归 worktree/baseline 退出码全 MATCH（`test-command-lifecycle-wt-close.py` 1 项预存红，基线同用例同断言）。真实执行：本轮 absorb 直接使用 `freely issue-sync promote raw-20261104T082556Z I-20261104T082556Z-A`，修好的路径在真机上产出 platform_ids 并记录 children（此前该命令必然失败）。
