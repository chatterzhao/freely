# Pre-Tests: wt-close 分支解析数值守卫与残留工位回收
- issue_id: I-20261112T131130Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `_resolve_branch_from_raw_key` 不再双写计数、无匹配时无语法错误且 rc=0 空输出、只有 test-pre-merge 分支时可解析、单个 fix 分支与 ambiguous 拒绝不退化；develop 基线必须复现语法错误
- acceptance_target: 分支解析失败必须显式失败，且只剩测试沙箱的残留工位可被封装命令回收
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 临时 git 仓库（抽取真实 resolver 函数 + stub 分支，不触网、不动真工位）
- required_evidence: AT-001 静态 6 + 行为 5 + 基线控制 1 全 GREEN；unit 5 项 PASS
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-wt-close-branch-count.py
- test_command: python3 docs/system/workspace/scripts/tests/test-wt-close-branch-count.py
- expected_output: SUMMARY: 11 ok, 0 failed
- expected_RED_output: SUMMARY: 5 ok, 7 failed
- actual_RED_output: develop 1a6139375 快照上 S2–S6 全红（没有数值守卫与 test-pre-merge 回退）、B2 红（基线真的输出 syntax error in expression）、B4 红（test-pre-merge 解析不到）；基线控制 R1 通过，证明 RED 不是测试臆造（AT-001-RED.log）
- actual_output: SUMMARY: 11 ok, 0 failed；B1 空输出 rc=0、B2 无语法错误、B3 单 fix 分支、B4 test-pre-merge 残留、B5 ambiguous 仍拒绝（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261112T131130Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,unit-t-wt-close-count-01.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组断言计数写法、正则校验、test-pre-merge 回退与 return 1；行为组用 awk 抽取真实 resolver 函数，在 `git init` 沙箱里建 stub 分支后执行，覆盖无匹配 / 单 fix / 仅 test-pre-merge / 双候选四种拓扑；基线控制对 develop 源码跑同一断言并断言确实出现 `syntax error in expression`，防止「永远为真」的假绿。
- red_how: fix RED — git archive develop 导出基线树，用 --source-dir 与 --baseline 运行同一 AT。

## Unit
- acceptance_target: resolver 的计数守卫与 test-pre-merge 回退
- testing_layer: unit
- target_environment: fix/raw-20261112T131130Z-wt-close-count-guard
- required_evidence: t-wt-close-count-01.sh 5 项 PASS
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/unit/t-wt-close-count-01.sh

## Integration
- acceptance_target: 既有 wt-close 收口路径与 CI 子集不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；projections verify ok；三门禁 ok
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End
- acceptance_target: 合并后真机回收 R33.6 自证残留工位
- testing_layer: end-to-end
- target_environment: 主仓（合并后的 develop）
- required_evidence: wt-close --raw-key 20261112T040108Z 成功；git worktree list 只剩主工位
- blocker_taxonomy: execution_pending_or_failed
1. ./bin/freely wt-close --raw-key 20261112T040108Z --discard-unmerged --force --reason "<合规前缀+理由>"

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 缺陷在 R33.6 收尾时真机复现（两条语法错误 + exit 0 + 工位未删），修复后用同一命令真机回收。
