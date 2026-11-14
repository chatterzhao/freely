# Pre-Tests: merge 后残留提交的补合并优先规范

- issue_id: I-20261114T065554Z-A

## Acceptance Items

### acceptance-1

- id: AT-001
- requirement: 区分 never_merged / post_merge_additions；逐提交 patch-id 等价性判定；情形 B 未落盘默认拒绝丢弃并给出补合并 PR 与 two-dot diff 说明；--extracted-into 必须指向真实存在的 raw；情形 A 保持原强度；skill/commands.md/理由清单同步；基线红
- acceptance_target: merge 后追加提交不再被误判为「没 merge」、不再被默认丢弃
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 临时 git 仓（真实 merge commit + cherry-pick 构造等价落盘）+ 源码静态断言
- required_evidence: AT-001 GREEN 25/0；基线 2/14
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-postmerge-commit-guard.py
- test_command: python3 docs/system/workspace/scripts/tests/test-postmerge-commit-guard.py
- expected_output: SUMMARY: 25 ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok, 14 failed
- actual_RED_output: develop 36a48f9ed 无判定器、无 post_merge_additions 分诊、无补合并路径、skill/commands.md 无规范；仅 S11/S15 通过（AT-001-RED.log）
- actual_output: SUMMARY: 25 ok, 0 failed；B1–B3 从未 merge 保持原策略、B4–B7 已 merge 未落盘拒绝丢弃、B8–B10 等价落盘零损失放行、S1–S15 三层文本与实现一致且 protected 守卫断言不变（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261114T065554Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ''
- task_refs: T1,T2,T3,T4
- case_design: 三个真实 git 仓场景（A 从未 merge / B 已 merge + 未落盘追加 / C 已 merge + cherry-pick 等价落盘），用 `git cherry` 验证 patch-id 判定；静态组钉住 wt-close 两处提示、USAGE、理由清单、skill 阶段 9、commands.md 以及 protected 守卫测试未变。
- red_how: fix RED — `git archive develop` 导出基线树，用 `--source-dir` 运行同一 AT。

## Unit

- acceptance_target: 判定器分情形与逐提交等价性
- testing_layer: unit
- target_environment: fix/raw-20261114T065554Z-postmerge-commit-guard
- required_evidence: AT-001 B1–B10
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-postmerge-commit-guard.py

## Integration

- acceptance_target: 既有收口与 CI 不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；test-wt-close-test-premerge-guard.py S2 仍绿
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End

- acceptance_target: 下一次遇到 merge 后追加提交时守卫给出补合并路径
- testing_layer: end-to-end
- target_environment: 下一轮 wt-close --force
- required_evidence: 输出含逐提交 equivalent/NOT-EQUIV 与补合并 PR 命令，且不再打印「没有 merge」
- blocker_taxonomy: execution_pending_or_failed
1. 下一次 wt-close 的真实输出

## Real-Environment

- real_environment_status: pass
- real_environment_reason: R33.16 真机：PR #4442 已合并、追加提交 712e7550c 差点被 --discard-unmerged 丢弃；正解是补合并 PR #4641 后正常收口。
