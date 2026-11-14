# Pre-Tests: I-* 收口链路对齐设计
- issue_id: I-20261114T033013Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: merge hook 能发现并正确处理本 lane 的 B1 raw 与 B2 linked；linked 收口走 `issue-sync batch <raw-key>`；`cmd-create` 对 linked 写 `platform_state`；wt-close 读取源保持 develop；基线红
- acceptance_target: 「merge 时收口 I-*」从死代码变成可执行链路
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 git 临时仓（main..feature）+ 源码静态断言
- required_evidence: AT-001 GREEN 30/0；基线 2/9
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-closeout-chain.py
- test_command: python3 docs/system/workspace/scripts/tests/test-closeout-chain.py
- expected_output: SUMMARY: 30 ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok, 9 failed
- actual_RED_output: develop f94f815ac 无 merge_issue_sync.py；hook 仍只 diff B1 且整树 git add；cmd-create 仍被 _fm_has_key 挡住；wt-close 仍用 PROJECT_ROOT（并附带 "module missing" 跳过行为组）（AT-001-RED.log）
- actual_output: SUMMARY: 30 ok, 0 failed；发现 B1+B2、按 raw-key 排除其它 raw、phase 行替换保序、hook 走 batch、create 写 platform_state、wt-close 读工位（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/platform-sync/close-merged/raw-20261114T033013Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ''
- task_refs: T1,T2,T3
- case_design: 静态断言接线（hook/create/wt-close）+ 纯函数判定表 + 临时 git 仓端到端（main..feature，两个 raw，验证发现、范围、落盘保序）。
- red_how: fix RED — git archive develop 导出基线树，用 --source-dir 运行同一 AT。

## Unit
- acceptance_target: 判定表与 phase 落盘
- testing_layer: unit
- target_environment: fix/raw-20261114T033013Z-merge-hook-linked-sync
- required_evidence: AT-001 S2–S5、S10–S11
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-closeout-chain.py

## Integration
- acceptance_target: 既有 merge/closeout 路径不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；test-gate-fail-closed / test-verdict-contract 仍绿
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End
- acceptance_target: 下一轮真实 merge 时 linked 被收口
- testing_layer: end-to-end
- target_environment: 下一次 pr-merge-guarded
- required_evidence: merge 输出含 `issue-sync batch <raw-key>`，且 linked 文档 platform_state=closed 随 merge 进入 develop
- blocker_taxonomy: execution_pending_or_failed
1. 下一次 pr-merge-guarded 的实际输出

## Real-Environment
- real_environment_status: pass
- real_environment_reason: R33.16 真机：工位 platform_state=closed、develop 缺失、平台 #4441 CLOSED，wt-close 却被拒 —— 三处缺陷同时暴露。
