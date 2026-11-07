# Pre-Tests: 两代 receipt 兼容 + 审计链总能跑完
- issue_id: I-20261107T090847Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `merge_path` allowlist 同时接受两代合法值（历史兼容）；完整 `governance-check` 在预存 `[FAIL]` 存在时仍跑完 receipt 审计并输出汇总行；真实/合法 `pr-merge-guarded` merge 不报 unknown；历史 `merge-guarded` 仍被接受；非法/缺失值仍明确 fail；不删除或削弱任何既有检查；`pr-merge-guarded` / `commit-msg.sh` / `post-checkout` 不变
- acceptance_target: 补齐 README 宣称第三层 post-merge audit，消除假阳性与静默失效双重失真
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离 git 仓库（真实 2-parent merge commit）
- required_evidence: 新增回归测试 9 静态 + 6 行为全 GREEN + 9 个回归基线对比零新增失败 + 真实 develop HEAD 复验
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-governance-receipt-audit
- test_command: bash docs/system/workspace/scripts/tests/test-governance-receipt-audit all
- expected_output: PASS: 8 checks, 0 failed（含 9 条静态断言与 6 个行为场景）
- expected_RED_output: FAIL: 3 of 8 checks failed（静态 7 项 FAIL + CASE A + CASE E）
- actual_RED_output: 未修改 develop HEAD（`0ad3941ff`）基线 RED —— allowlist 无新值、控制流未加固、check 函数未守卫；CASE A 抽取 audit 函数误报 `unknown Freely-Merge-Path 'pr-merge-guarded'`；CASE E 完整脚本在 line 874 `entries[@]: unbound variable` 提前退出、无汇总行；5 项既有能力保持 PASS（旧值接受、非法值拒绝、缺失 trailer 拒绝、完整脚本无假阳性、bash -n）（AT-001-RED.log）
- actual_output: 9 静态断言全 ok；CASE A/B 两代 receipt 接受、CASE C/D 非法/缺失值拒绝、CASE E 完整脚本输出 `Governance check failed with 12 error(s)` 汇总行、CASE F 无假阳性（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/governance/raw-20261107T090847Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: static 组用 Python 按函数体作用域检查 allowlist 与 5 处控制流守卫；behavior 组在隔离 git 仓库复制真实 `bin/governance-check` + 真源，用 `git merge --no-commit --no-ff` + `git commit` 构造真实 2-parent merge，分别注入新式/旧式/非法/缺失 receipt，抽取 audit 函数探针（含后置 helper）判定；另跑完整脚本断言汇总行与无假阳性。
- red_how: fix RED — 用 `git show HEAD:<file>` 把 governance-check 还原到未修改 develop 状态后运行同一断言组，确认假阳性与提前退出。

## Unit
- acceptance_target: allowlist 与控制流静态契约
- testing_layer: unit
- target_environment: fix/raw-20261107T090847Z-governance-receipt-audit
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-governance-receipt-audit static

## Integration
- acceptance_target: R1..R9、Q1/Q2、门禁链接线与 wt-create 能力不退化
- testing_layer: integration
- target_environment: 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-gate-fail-closed all
2. bash docs/system/workspace/scripts/tests/test-commit-msg-wireup all
3. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir all

## End-to-End
- acceptance_target: 真实 merge commit 审计与完整脚本汇总
- testing_layer: end-to-end
- target_environment: 隔离 git 仓库 + 真实 develop HEAD 只读复验
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-governance-receipt-audit behavior
2. 真实 develop HEAD 上抽取修复后 audit 函数复验 PROBE_ERRORS=0（AT-001-GREEN.log）

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在真实 fix 工位以项目真源命令执行；R2 物化 H1 自举生效；真实 develop HEAD 的 `pr-merge-guarded` merge 在修复后 audit `PROBE_ERRORS=0`（基线误报）；完整真源跑到汇总行；1 个真源还原到未修改 develop HEAD 做基线对比，9 个相关回归退出码逐一相同（2 个预存红测试输出变化为可观测性提升、已如实记录）→ 0 新增失败；bin/check-epics-map 对齐通过；双平台 raw 副本用封装命令关闭、三份 fingerprint 一致。
