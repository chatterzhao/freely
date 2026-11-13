# Pre-Tests: pull 与平台副本保持天然一致
- issue_id: I-20261113T084851Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: pull 镜像平台 comments 并保护本地终态；产物无需人工编辑即通过真实副本一致性门禁；重复 pull 幂等；基线必须复现三类红
- acceptance_target: 消除「手工编辑文档凑门禁」的绕过手法，且门禁强度一点不降
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 加载真实 adapter + 真实 reconciliation，仅 stub 传输函数（不触网、不动真平台）
- required_evidence: AT-001 静态 5 + 行为 8 + 基线控制 3 全 GREEN；unit 4 项 PASS
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-raw-issue-pull-parity.py
- test_command: python3 docs/system/workspace/scripts/tests/test-raw-issue-pull-parity.py
- expected_output: SUMMARY: 13 ok, 0 failed
- expected_RED_output: SUMMARY: 6 ok, 10 failed
- actual_RED_output: develop 02ee82705 快照上 S1–S5 全红（pull 不读 comments、无终态守卫）；B2/B3/B4/B6/B7 红（本地无 comment 块、真实 reconcile 判 content_diverged、absorbed 被降级、platform_state 丢失）；基线控制 R1/R2/R3 全通过，证明三类红都是真实缺陷而非断言臆造（AT-001-RED.log）
- actual_output: SUMMARY: 13 ok, 0 failed；B2 本地含镜像 comment 块，B3 `reconcile` 判 ok=True，B4 diagnostics 为空，B6/B7 终态保留，B8 幂等（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/platform-sync/close-merged/raw-20261113T084851Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,unit-t-raw-issue-pull-parity-01.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组断言 comments 读取、comment 块格式、终态枚举与保留；行为组用 `importlib` 加载真实 `platform-adapter.py`，只 mock `discover_raw_replicas` / `check_and_claim_assign_assignee` / `severity_from_replicas`，在临时目录物化，再把产物喂给**真实** `raw-reconciliation-gate._local_record` 与 `raw_reconciliation.reconcile` 判定；终态用例先写 absorbed 文档再二次物化；幂等用例连续物化两次；基线组对 develop 源码跑同一流程并断言三类缺陷真实存在。
- red_how: fix RED — git archive develop 导出基线树，用 --source-dir 与 --baseline 运行同一 AT。

## Unit
- acceptance_target: comments 镜像与终态保留的函数级行为
- testing_layer: unit
- target_environment: fix/raw-20261113T084851Z-raw-issue-pull-comment-parity
- required_evidence: t-raw-issue-pull-parity-01.sh 4 项 PASS
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/unit/t-raw-issue-pull-parity-01.sh

## Integration
- acceptance_target: 既有物化/收口路径与 CI 子集不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；projections verify ok；三门禁 ok
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End
- acceptance_target: 本轮自身收口链路不再出现 `phase_state=proposed` 或 raw 副本不一致拦截
- testing_layer: end-to-end
- target_environment: 本 issue 的 pr-create-guarded / wt-close
- required_evidence: PR 创建无需手工编辑 raw 文档
- blocker_taxonomy: execution_pending_or_failed
1. ./bin/freely pr-create-guarded

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 缺陷在 R33.8 / R33.6 收尾时真机复现（pull 重写后副本判红、absorbed 回退），修复后本轮自身 PR 链路即为验证。
