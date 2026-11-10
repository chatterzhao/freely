# Pre-Tests: 平台写收口到 adapter
- issue_id: I-20261104T080014Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `bin/issue-sync` 不再直连 `gh issue create/comment/close/edit`，四类写全部经 `platform-adapter.py issue-write-one` 路由到 handler；adapter 单平台 create 在 stub `gh` 下带 labels 并返回 url
- acceptance_target: 平台写实现只剩 adapter 一份，issue-sync 只编排
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: `git archive develop` 隔离基线 / 工位真源；行为测试用临时 git repo + PATH 前置 `gh` stub，不访问真实平台、不改真实 issue
- required_evidence: 3 静态 + 1 行为 = 4 项全 GREEN；基线 RED `0 ok / 4 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-platform-sync-entrypoint.py
- test_command: python3 docs/system/workspace/scripts/tests/test-platform-sync-entrypoint.py
- expected_output: SUMMARY: 4 ok, 0 failed
- expected_RED_output: SUMMARY: 0 ok / 4 failed
- actual_RED_output: develop `9348b2661` 基线 + 最终版 AT-001 → `0 ok, 4 failed`（AT-001-RED.log）：issue-sync 含 4 种直连写、adapter 无 `issue-write-one`、行为不可用。
- actual_output: 工位同一断言 → `4 ok, 0 failed`（AT-001-GREEN.log）。
- evidence_file: docs/B2-docs/platform/issue-sync-entrypoint/raw-20261104T080014Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态断言 issue-sync 无 4 种直连写、含 adapter + `issue-write-one`、adapter 分支路由 `add_comment`；行为用临时 git repo + `gh` stub，跑 `issue-write-one github create "" T B "kind/raw,phase/proposed"`，断言 stub 收到 `issue create` 与 `--label`、stdout 含 url。
- red_how: `git archive develop | tar -x -C /tmp/r27-base`，只注入最终版 AT-001，`--source-dir` 运行。
- implementation_findings: ①adapter 输出 JSON，`_gh_create` 的 url 提取必须止于引号，否则 `NEW88"}}` 会被当成 issue id；②`issue-write-one` 需要 `FREELY_PLATFORM_REPO` 覆盖，否则夹具无 git remote 时 repo 为空；③两个既有 issue-sync 夹具需补 adapter/新命令 stub（promote-b2 已补并恢复 23/0）。

## End-to-End
- acceptance_target: adapter 单平台 create 的真实 CLI 路径
- testing_layer: end-to-end
- target_environment: 临时 repo + gh stub
- required_evidence: AT-001（行为 1 项）+ `bin/test-all --ci`
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-platform-sync-entrypoint.py
2. bin/test-all --ci

## Unit
- acceptance_target: 写入口静态契约
- testing_layer: unit
- target_environment: feature/raw-20261104T080014Z-platform-sync-entrypoint
- required_evidence: AT-001（静态 3 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-platform-sync-entrypoint.py

## Integration
- acceptance_target: issue-sync / adapter / 平台探针不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 8 项回归
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2
2. bash docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first
3. bash docs/system/workspace/scripts/tests/test-issue-sync-protected-branch-guard
4. python3 docs/system/workspace/scripts/tests/test-issue-sync-replica-guard.py
5. python3 docs/system/workspace/scripts/tests/test-platform-adapter-gitee-search.py
6. python3 docs/system/workspace/scripts/tests/test-platform-adapter-github-rest-fallback.py
7. python3 docs/system/workspace/scripts/tests/test-platform-handler-probe.py
8. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 行为测试只跑本地 `gh` stub 与临时 git repo，不访问 GitHub/Gitee；真实平台写不在本 AT 覆盖范围（由既有 adapter 探针与后续真实 PR 流程覆盖）。
- real_environment_reason: AT-001 RED `0/4` → GREEN `4/0`；`test-issue-sync-promote-b2` 23/0、`test-issue-sync-close-terminal-first` 27/0、`test-platform-*` 全绿、`test-all --ci` 10/0。`test-issue-sync-replica-guard.py` 基线 6 failed、工位 4 failed（receipt/close-multi 路径既有失败，无新增类别）。
