# Pre-Tests: wt-create 顶层 return 改为 exit
- issue_id: I-20261106T084804Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 三处顶层失败分支均 exit 1，输出只有业务错误文案且不含 bash `can only return` 语法错误；失败后 dev 分支清理、不产生半成品工位；顶层 return 计数为 0、函数内 return 数量保持 22、bash -n 通过；shim 仍 exec bash；三条业务文案与清理动作逐字不变；四态判定/恢复/legacy/seed 单一真源不退化
- acceptance_target: 失败语义由显式 exit 表达，不再依赖 set -e 隐式兜底，也不遮蔽业务错误
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离 git 仓库（不触网）
- required_evidence: 新增回归测试 20 项全 GREEN + 9 个回归 PASS + 2 个预存红测试与基线一致
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-wt-create-top-level-return
- test_command: bash docs/system/workspace/scripts/tests/test-wt-create-top-level-return all
- expected_output: PASS: 20 checks, 0 failed
- expected_RED_output: FAIL: 4 of 16 checks failed
- actual_RED_output: 未修改 develop HEAD 基线 RED 4 项失败 —— 顶层 return 计数 3（应为 0）、三条失败分支均打印 `return: can only \`return' from a function or sourced script`；12 项既有能力保持 PASS（函数内 return 22、shim、三条业务文案、bash -n、清理动作、退出码、dev 分支清理）（AT-001-RED.log）
- actual_output: PASS: 20 checks, 0 failed；顶层 return 0 / 函数内 22；三条分支 exit 1、业务文案存在、无 bash 语法错误、dev 分支已清理（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261106T084804Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: static 组用括号深度分析统计顶层/函数内 return 数并断言 0/22，校验 shim、三条业务文案、清理动作数量、bash -n；behavior 组复用既有隔离 git 仓库骨架（真实 wt-create + worktree-common.sh + replica gate stub），通过可注入 stub 分别触发 pull identity mismatch、dev seed 强制失败、test init 强制失败，断言退出码 1、业务文案、无 bash `return` 语法错误、dev 分支已清理。
- red_how: fix RED — 用 `git show HEAD:wt-create` 还原到未修改 develop 状态后运行同一断言组，确认三条分支都输出 bash 语法错误。

## Unit
- acceptance_target: 顶层/函数内 return 作用域与静态契约
- testing_layer: unit
- target_environment: fix/raw-20261106T084804Z-top-level-return
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-create-top-level-return static

## Integration
- acceptance_target: R1..R6、Q1/Q2、四态/反查/恢复、平台回退不退化
- testing_layer: integration
- target_environment: 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir all
2. bash docs/system/workspace/scripts/tests/test-wt-create-recovery-dev-path all
3. python3 docs/system/workspace/scripts/tests/test-raw-issue-pull-platform-fallback.py

## End-to-End
- acceptance_target: 三条顶层失败分支真实执行
- testing_layer: end-to-end
- target_environment: 隔离 git 仓库（不触网）
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-create-top-level-return behavior

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实 fix 工位以项目真源命令执行；R2 物化 H1 自举生效；以未修改 develop HEAD 做基线对比，9 个回归 PASS、2 个预存红测试退出码与输出一致（仅时间戳差异）→ 0 新增失败；隔离 git 仓库三条失败分支真实执行全 GREEN；bin/check-epics-map 对齐通过；双平台 raw 副本用封装命令关闭、三份 fingerprint 一致。
