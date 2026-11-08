# Pre-Tests: 安装态版本可证明且与 develop 同步
- issue_id: I-20261105T121046Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `latest` 落后 / 悬空、PATH 链接悬空、hash 漂移都要被检查器显式报告；打包写关键文件 sha256 清单；`--activate` 原子切换 `latest` 且失败保留旧版本、不覆盖健康链接；同 HEAD 幂等；`freely doctor` 与 merge followthrough 都接同一真源；全部行为测试隔离 `FREELY_HOME`
- acceptance_target: 开发态与安装态的身份可机器证明，合并 develop 后受控同步
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 临时 `FREELY_HOME` + 临时 git 项目树（真实 `install_state.py` / 真实 CLI）+ develop HEAD 基线快照对比
- required_evidence: 10 静态 + 13 行为共 23 项全 GREEN；21 个相关回归 worktree/baseline 退出码全 MATCH；真机合并后 followthrough 自举刷新安装态
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-install-state.py
- test_command: python3 docs/system/workspace/scripts/tests/test-install-state.py all
- expected_output: SUMMARY: 23 ok, 0 failed
- expected_RED_output: SUMMARY: 21 failed（静态 8：无 install_state 库/CLI、freely-package 无 --activate/auto/hash 清单、merge 无打包触发、doctor 无接线；行为 13：落后/悬空/漂移都不报、无清单、无原子激活、CLI 无判定）
- actual_RED_output: develop `c1949aa24` 基线快照（`git archive develop -- bin docs`）放入**最终版** AT-001 —— `SUMMARY: 2 ok, 21 failed`（AT-001-RED.log）。2 项 PASS 是「freely-package 存在」「cmd_doctor 存在」两条守卫，证明测试夹具本身可跑通。
- actual_output: 工位同一断言 —— `SUMMARY: 23 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/platform/raw-20261105T121046Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,AT-001-REGRESSION-BASELINE.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7
- case_design: 静态组断言四处真源接线 + 2 条既有能力守卫；行为组用 tempfile 建临时 home 与临时 git 项目树，import 真实 `install_state.py`、跑真实 `install-state-check.py`，覆盖落后/悬空 latest/悬空 PATH 链接/hash 漂移/清单写入/原子激活/同步通过/幂等/健康链接保留/CLI 退出码与 JSON。真实 `~/.freely` 与 `~/.local/bin` 零写入。
- red_how: fix RED — `git archive develop -- bin docs` 出基线快照，把最终版 AT-001 拷入后以 `--source-dir /tmp/r16-base` 运行，基线文件一个不改。

## Unit
- acceptance_target: 接线契约（唯一真源、CLI、打包参数、merge 触发、doctor 输出）
- testing_layer: unit
- target_environment: fix/raw-20261105T121046Z-install-state-version-check
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-install-state.py static

## Integration
- acceptance_target: 打包/门禁/写通道/生命周期/契约等既有能力不退化
- testing_layer: integration
- target_environment: 工位 + 未修改 develop HEAD 基线快照
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-freely-doctor-build-artifact-exposure-gate
2. bash docs/system/workspace/scripts/tests/test-freely-doctor-execution-boundary-audit
3. bash docs/system/workspace/scripts/tests/test-freely-doctor-supply-chain-gate
4. bash docs/system/workspace/scripts/tests/test-freely-package-output-guard
5. bash docs/system/workspace/scripts/tests/test-package-runtime-allowlist-parity
6. bash docs/system/workspace/scripts/tests/test-worktree-seed-package-parity
7. bash docs/system/workspace/scripts/tests/test-platform-write-channel
8. bash docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first
9. bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2
10. bash docs/system/workspace/scripts/tests/test-test-gate-record
11. bash docs/system/workspace/scripts/tests/test-wt-close-comment-scan
12. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
13. python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
14. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
15. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-materialization.py
16. python3 docs/system/workspace/scripts/tests/test-platform-handler-probe.py
17. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-wt-close.py
18. python3 docs/system/workspace/scripts/tests/test-scan-frontmatter-nested.py
19. python3 docs/system/workspace/scripts/tests/test-platform-open-parity.py
20. bash docs/system/workspace/scripts/tests/test-governance-gate-batch-read
21. python3 docs/system/workspace/scripts/tests/test-feedback-severity.py

## End-to-End
- acceptance_target: 隔离安装态的四类故障与激活后的一致性
- testing_layer: end-to-end
- target_environment: 临时 FREELY_HOME + 临时 git 项目树
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-install-state.py behavior

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 行为测试不执行真实打包（那会写 ~/.freely）；真实打包与激活由本轮合并时 `pr-merge-guarded` 的 followthrough 自举执行。
- real_environment_reason: 只读真机检查在开工前已复现症状：`install-state-check.py --project <worktree>` 报 `installed state is behind project HEAD (packaged_from=444985f50, head=c1949aa24)` 且 `installed version has no hash manifest`。21 个回归 worktree/baseline 退出码全 MATCH：3 个 doctor gate 与 `test-command-lifecycle-wt-close.py` 为预存红（两边同值）；2 个 package 测试首轮 DIFF 经核实是 `git archive -- bin docs` 快照缺 `.githooks/`、`templates/`、`.freely/tool-boundary-bootstrap.md`，补齐后两边均 0（详见 AT-001-REGRESSION-BASELINE.log 的 NOTE）。
