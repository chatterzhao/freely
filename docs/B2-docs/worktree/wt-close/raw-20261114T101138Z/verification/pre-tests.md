# Pre-Tests: dropped 收口自动写关闭理由并防重新物化

- issue_id: I-20261114T101138Z-A

## Acceptance Items

### acceptance-1

- id: AT-001
- requirement: `close_dropped` 评论先于关闭；GitHub 以 `not planned` 关闭；Gitee 关闭带 `--comment`；评论失败不关任何平台；`close_issue` 扩展默认参数后既有 `close-raw`/`close-multi`/CLI `close` 行为不变；`pull_raw_issue` 全 CLOSED 副本返回 None；`wt-close --force --reason` 关单前本地瞬时 `phase_state=dropped` 且 `completed_at`/`closeout_note` 齐全、`validate()` 通过
- acceptance_target: dropped 收口把关闭理由落盘到平台评论并以 not-planned 关闭，且不破坏既有关闭路径
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: 真实执行 adapter 与 wt-close 编排
- required_evidence: AT-001 GREEN 7/0；基线 0/7
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-wt-close-dropped-closeout.py
- test_command: python3 docs/system/workspace/scripts/tests/test-wt-close-dropped-closeout.py
- expected_output: SUMMARY: 7 ok, 0 failed
- expected_RED_output: AttributeError / TypeError（close_dropped 不存在或 close_issue 无 reason 参数）
- actual_RED_output: develop 无 close_dropped、GitHub close_issue 无 --reason
- actual_output: SUMMARY: 7 ok, 0 failed
- evidence_file: docs/B2-docs/worktree/wt-close/raw-20261114T101138Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ''
- task_refs: T1
- case_design: 用 FakeHandler 记录每次平台调用顺序，断言 comment 先于 close、GitHub 传 `--reason not planned`、Gitee 传入 comment_body、评论失败时无平台关闭；monkeypatch discover 全 CLOSED 验证 pull fail-closed；对 GitHub handler 直接断言 `--reason` 出现/缺失。
- red_how: fix RED — 对 develop 基线运行同一 AT。

## Unit

- acceptance_target: close_dropped / handler 签名 / pull guard
- testing_layer: unit
- target_environment: fix/raw-20261114T101138Z-dropped-closeout
- required_evidence: AT-001 S1–S7
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-wt-close-dropped-closeout.py

## Integration

- acceptance_target: 既有 adapter / wt-close 测试不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all 相关用例全绿（test-platform-adapter-raw-identity / test-command-lifecycle-raw-metadata / test-issue-sync-close-linked / test-wt-close-dryrun-safety）
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci
