# Pre-Tests: 恢复 protected 门禁与 companion-only 沙箱回收
- issue_id: I-20261113T084813Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 守卫无条件拒绝 main/develop/test-pre-merge；resolver 不解析沙箱；companion-only 在 reason gate 之后只删工位+分支、无平台/Phase 7 副作用、dry-run 零副作用；基线复现被放宽的门禁
- acceptance_target: 恢复门禁原强度，用实现修复（而非放宽门禁）补齐残留沙箱回收
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 抽取真实守卫块/companion 函数 + sandbox git 仓库（不触网、不动真平台）
- required_evidence: guard AT `18 ok / 0 failed`、count AT `11 ok / 0 failed`、两个 unit 6/0 与 7/0、基线控制全通过
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-wt-close-test-premerge-guard.py
- test_command: python3 docs/system/workspace/scripts/tests/test-wt-close-test-premerge-guard.py
- expected_output: SUMMARY: 18 ok, 0 failed
- expected_RED_output: guard `8 ok / 12 failed`、count `10 ok / 2 failed`
- actual_RED_output: develop 677a06aae 快照上 guard S2–S8 与 B1/B3–B8 红（守卫仍有 --force 例外、无 companion 路径）、基线 R1/R2 通过；count S5/B4 红（resolver 仍解析沙箱）、R1 通过（AT-001-guard-RED.log / AT-001-count-RED.log）
- actual_output: guard `18 ok / 0 failed`、count `11 ok / 0 failed`；B4/B5 在沙箱存活期内查询 branch/worktree 确认真删除，B6 无平台/develop 副作用，B8 dry-run 零副作用（AT-001-guard-GREEN.log / AT-001-count-GREEN.log）
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261113T084813Z/verification/test-evidence/AT-001-guard-RED.log,AT-001-guard-GREEN.log,AT-001-count-RED.log,AT-001-count-GREEN.log,unit-t-wt-close-premerge-guard-01.log,unit-t-wt-close-count-01.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组断言守卫无例外、companion 路径存在且声明零副作用、resolver 不含沙箱回退；行为组抽取真实守卫块与 `_wt_retire_orphan_test_sandbox`，在 sandbox git 仓库里建 `test-pre-merge-*` 分支 + 真实 worktree 后执行，**在临时目录存活期内**取 `git branch --list` / `git worktree list` 快照（首版在函数返回后查询已删除目录，产生假绿，已修正）；基线组对 develop 源码断言「守卫有 --force 例外」与「resolver 解析沙箱」真实存在。
- red_how: fix RED — git archive develop 导出基线树，用 --source-dir 与 --baseline 运行同一 AT。

## Unit
- acceptance_target: 守卫绝对性、companion 零副作用声明、resolver 不解析沙箱
- testing_layer: unit
- target_environment: fix/raw-20261113T084813Z-restore-protected-guard
- required_evidence: t-wt-close-premerge-guard-01.sh 6/0、t-wt-close-count-01.sh 7/0
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/unit/t-wt-close-premerge-guard-01.sh
2. bash docs/system/workspace/scripts/tests/unit/t-wt-close-count-01.sh

## Integration
- acceptance_target: 既有 wt-close 收口路径与 CI 子集不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；projections verify ok；三门禁 ok
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End
- acceptance_target: 本轮自身 wt-close 走主路径且不被新 companion 路径干扰
- testing_layer: end-to-end
- target_environment: 本 issue 的收口链路
- required_evidence: `wt-close --raw-key 20261113T084813Z` done ✓
- blocker_taxonomy: execution_pending_or_failed
1. ./bin/freely wt-close --raw-key 20261113T084813Z

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 缺陷在 R33.9 合并后真机复现（沙箱走完整生命周期并触发平台关单/Phase 7），修复后由 AT 的 sandbox git 仓库真删工位/分支验证等价能力，且门禁强度恢复。
