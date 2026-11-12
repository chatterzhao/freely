# Pre-Tests: 预演与恢复路径不得产生不可逆副作用
- issue_id: I-20261112T131150Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: wt-close 的 Phase 6b 在 DRY_RUN=true 时零副作用（不动 worktree / branch / agent_working / agent-id.env），DRY_RUN=false 时行为与现状一致；wt-create 不再隐式改写已终态 raw 的 phase_state，重开必须显式 --reopen 且写入 dev 工位内的文档副本，主仓保持干净
- acceptance_target: 「预演」与「恢复」两条路径不再产生不可逆副作用
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 本地隔离沙箱（抽取真实 Phase 6b 代码块 + stub git，不触网、不动真工位）
- required_evidence: AT-001 静态 8 项 + 行为 3 项全 GREEN；负向控制证明 DRY_RUN=false 仍会清理；unit 5 项全 PASS
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-wt-close-dryrun-safety.py
- test_command: python3 docs/system/workspace/scripts/tests/test-wt-close-dryrun-safety.py
- expected_output: SUMMARY: 12 ok, 0 failed
- expected_RED_output: SUMMARY: 3 ok, 9 failed
- actual_RED_output: develop 8ad2c2a83 快照（git archive develop）上运行同一 AT，rc=1：S2/S3/S4 说明 Phase 6b 完全不看 DRY_RUN；S5/S6 说明没有 --reopen；S7/S7b 说明 phase 改写落在调用方路径；B1 真实出现 dry-run 仍向 git 发 worktree remove + branch -D（AT-001-RED.log）
- actual_output: SUMMARY: 12 ok, 0 failed；B1 dry-run 下 git 未收到任何破坏性动词，B2 仍打印 [DRY-RUN] 计划，B3 负向控制（DRY_RUN=false）确实收到 worktree remove + branch -D（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261112T131150Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,unit-t-worktree-preview-01.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组对 wt-close 的 Phase 6b 文本与 wt-create 的 reopen 逻辑做结构与语义断言；行为组用 awk 从源码抽取真实 Phase 6b 块，在临时沙箱里以 stub git 执行——dry 组断言 git log 无破坏性动词、stdout 有 [DRY-RUN]；负向控制以 DRY_RUN=false 跑同一块，断言两个动词都到达 git，防止「永远为真」的假绿。
- red_how: fix RED — 用 git archive develop 导出基线树，再用 --source-dir 指向该树运行同一 AT。

## Unit
- acceptance_target: Phase 6b 的 DRY_RUN 分支与 wt-create 的 rewrite 目标
- testing_layer: unit
- target_environment: fix/raw-20261112T131150Z-wt-close-dryrun-side-effects
- required_evidence: t-worktree-preview-01.sh 5 项 PASS
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/unit/t-worktree-preview-01.sh

## Integration
- acceptance_target: 既有 wt-close / wt-create 路径不退化；三门禁与 CI 子集全绿
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；projections verify ok；check-runtime-size / check-bin-projection / check-epics-map ok
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci
2. ./bin/freely projections verify --project .

## End-to-End
- acceptance_target: 真实 wt-close --dry-run 不再删测试工位；真实 wt-create 不再改主仓
- testing_layer: end-to-end
- target_environment: 本 issue 自身的收口链路
- required_evidence: 本轮的 pr-create-guarded / pr-merge-guarded / wt-close 全程无 dry-run 破坏；合并后主仓 git status 干净
- blocker_taxonomy: execution_pending_or_failed
1. ./bin/freely wt-close --raw-key 20261112T131150Z --dry-run  （必须不删 test 工位）
2. ./bin/freely wt-close --raw-key 20261112T131150Z

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本轮开发前已在真机复现两处缺陷（R33.6 收尾时 test 工位被 dry-run 删除、主仓被 auto-reopen 写脏），修复后以同一封链路验证。
