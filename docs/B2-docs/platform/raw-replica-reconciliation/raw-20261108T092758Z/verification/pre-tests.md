# Pre-Tests: create/close 以平台侧发现为身份判定源
- issue_id: I-20261108T092758Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `cmd_create` 在「本地 platform_ids 缺某平台、但该平台已有唯一 canonical 副本」时不得重复建单、须回填真实 id；平台确认 missing 时照旧建单；读失败/ambiguous 时失败关闭拒绝建单；健康路径（缓存完整）零 discover I/O 零行为变化。`cmd_close` strict 前回填 partial 缓存使 close-multi 关闭全部真实副本，且非终态 raw 关闭不产生任何本地写入
- acceptance_target: 身份判定以平台侧事实为准；杜绝降级 pull 后的重复建单与漏关，零退化
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: 隔离 mock（stub `platform-adapter.py` / `gh` / `gitee-issue.py` + 真 `issue-sync` 源为库加载）+ develop HEAD 基线快照对比 + 真机 `discover-raw`→`replica_guard` 组合（只读，无写）；不调用真实平台写、不建真实单
- required_evidence: 8 静态 + 8 单元 + 12 行为断言全 GREEN；相关回归基线对比退出码一致
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-issue-sync-replica-guard.py
- test_command: python3 docs/system/workspace/scripts/tests/test-issue-sync-replica-guard.py all
- expected_output: SUMMARY: 28 ok, 0 failed
- expected_RED_output: SUMMARY: 7 ok, 13 failed（6 静态缺件 + 1 单元缺件 + create 重复/不回填 + degraded/ambiguous 仍建 + close 漏关/不回填/未通过严格契约）
- actual_RED_output: develop `a24ad958a` 基线快照 `--source-dir /tmp/r14_5-baseline` —— `SUMMARY: 7 ok, 13 failed`（AT-001-RED.log）
- actual_output: 工位同一断言 —— `SUMMARY: 28 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261108T092758Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: 隔离工程树把 `platform-adapter.py`（按 env 返回可控 discover-raw receipt、记录 close-multi 入参）、`gh`、`gitee-issue.py` 全部桩化，`issue-sync` 以 `ROOT_DIR` 源为库加载、`cmd_create`/`cmd_close` 直接驱动；行为矩阵覆盖 present/absent/unknown/ambiguous/healthy/create+close/非终态；纯 `classify_receipt` 单独单测 8 形态；静态断言绑定契约（guard 接线、纯模块、bash -n）。真机 read-only 组合验证 present(真实 4151/IKSPQ6) 与 indeterminate。
- red_how: fix RED — `git archive develop` 出基线快照 `/tmp/r14_5-baseline`（无 `replica_guard.py`、无 guard 接线），把最终版 AT-001 以 `--source-dir` 指向基线运行。

## Unit
- acceptance_target: `classify_receipt` 纯函数 8 形态（present/absent/unknown/ambiguous/ok-no-id/platform-missing/malformed/non-dict-entry）+ 静态契约
- testing_layer: unit
- target_environment: fix/raw-20261108T092758Z-create-replica-idempotency
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-issue-sync-replica-guard.py static
2. python3 docs/system/workspace/scripts/tests/test-issue-sync-replica-guard.py unit

## Integration
- acceptance_target: `issue-sync` 其他路径不退化（写通道、close 四段式、promote、protected-branch、wt-create 生命周期）
- testing_layer: integration
- target_environment: 工位 + 未修改 develop 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-issue-sync-replica-guard.py behavior
2. bash docs/system/workspace/scripts/tests/test-platform-write-channel
3. bash docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first
4. bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2
5. bash docs/system/workspace/scripts/tests/test-issue-sync-protected-branch-guard
6. python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py

## End-to-End
- acceptance_target: create 幂等 + close 全关对同一「partial 缓存 + 平台已有副本」结论一致，健康路径零 I/O
- testing_layer: end-to-end
- target_environment: 隔离 mock + 真机 discover-raw 只读组合
- required_evidence: AT-001
- blocker_budget: 0
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-issue-sync-replica-guard.py behavior
2. 真机 `platform-adapter.py discover-raw 20261103T132548Z` 管道 `replica_guard.py github|gitee`（present 带真实 id/url）、unknown receipt → indeterminate

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本缺陷是「create/close 信任缓存、未消费平台侧发现」，验证所需真实面是 `platform-adapter.discover_raw_replicas` 的返回形状与 `gh/gitee` 的建单/关闭副作用。建单/关闭副作用用隔离 mock 桩证明（真实 `issue-sync` 真源 + 桩化平台层，不写真实平台，符合 issue 验收「隔离 mock server 验证」）；`discover-raw` 返回形状用真机只读调用（#4151 → github ok 4151 / gitee ok IKSPQ6，url 齐全）与 `replica_guard.py` 组合验证，present 与 indeterminate 结论均正确。R14 现场复现证据（#4224 重复副本、ambiguous block、close #4224 无效、删重复后 allow）记入 brainstorms/IDN。真实「平台降级→重跑 create 不再重复」的端到端需制造真实平台抖动，按验收标准以隔离 mock 的固定 receipt 矩阵覆盖，真机只做 read-only 组合；post-merge 真实多轮自举（每轮 wt-create）即持续回归验证。
