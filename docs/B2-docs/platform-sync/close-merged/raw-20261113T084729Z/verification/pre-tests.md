# Pre-Tests: linked 收口回归 batch 单一路径与等价门禁
- issue_id: I-20261113T084729Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 直连 close 拒绝 linked；batch 使用专用动作；close_linked 具备 phase_state/B2 证据/平台 id 的 Phase 1 严格校验且失败零平台写入；成功回写 phase_state/platform_state 而非 status；raw 严格契约未放宽；基线复现宽松行为
- acceptance_target: 恢复设计意图中的单一收口路径与门禁强度，不产生第二套判据或状态语义
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 effect 入口 + 记录调用的 stub adapter（不触网、不动真平台）
- required_evidence: AT-001 静态 7 + 行为 12 + 基线控制 2 全 GREEN；unit 10 项 PASS
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-issue-sync-close-linked.py
- test_command: python3 docs/system/workspace/scripts/tests/test-issue-sync-close-linked.py
- expected_output: SUMMARY: 19 ok, 0 failed
- expected_RED_output: SUMMARY: 8 ok, 13 failed
- actual_RED_output: develop 7715ef030 快照上 S1–S7 全红（无 batch 专用动作、无 phase 守卫、仍写 status）；B2/B3/B6/B7/B8/B9 红（不写 platform_state、写 status、in_dev 被关且真的调用了平台、缺证据路径仍写平台）；基线控制 R1/R2 通过，证明宽松行为真实存在（AT-001-RED.log）
- actual_output: SUMMARY: 19 ok, 0 failed；B6/B7 `in_dev` 被拒且 adapter 零调用，B8/B9 缺证据路径被拒且零调用，B2/B3 写 platform_state 不写 status，B12 raw 契约仍拒绝 linked（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/platform-sync/close-merged/raw-20261113T084729Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,unit-t-linked-close-01.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组断言单一路径与状态字段；行为组让 stub adapter 把每次调用写入 `ADAPTER_LOG`，从而验证「拒绝时零平台写入」是运行时事实而非源码推测；覆盖 completed/in_dev/缺路径/部分关单/kind=raw/close-platforms 对 linked；基线组对 develop 源码跑同条件并断言 `in_dev` 真的被关、`status: closed` 真的被写入。
- red_how: fix RED — git archive develop 导出基线树，用 --source-dir 与 --baseline 运行同一 AT。

## Unit
- acceptance_target: batch 单一路径、phase 守卫、零平台写入、状态字段
- testing_layer: unit
- target_environment: fix/raw-20261113T084729Z-linked-close-batch-policy
- required_evidence: t-linked-close-01.sh 10 项 PASS
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/unit/t-linked-close-01.sh

## Integration
- acceptance_target: raw 收口与 CI 子集不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；projections verify ok；三门禁 ok
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End
- acceptance_target: 合并后遗留 linked 由 batch 按设计路径核对
- testing_layer: end-to-end
- target_environment: 主仓（合并后的 develop）
- required_evidence: `./bin/freely issue-sync batch --project <工位>` 不再出现 linked 收口失败
- blocker_taxonomy: execution_pending_or_failed
1. ./bin/freely issue-sync batch --project <工位>

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 缺陷在 R33.8 真机暴露（AI 逐条 close 绕过 batch、且 in_dev 也可关），修复后用同一 CLI 验证拒绝对外直连、由 batch 驱动。
