# Pre-Tests: pkill -f 项目路径正则转义
- issue_id: I-20261109T074900Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 两处含项目路径的 `pkill -f` 必须经单一 helper 正则转义；转义后不误匹配同前缀 sibling，且仍匹配自身；固定 pattern 站点不动
- acceptance_target: 停止项目 A 不再误杀项目 B 的 A2A server
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 `pgrep -f` 对两个带标记 python 子进程做反向 PoC（不调用 pkill、不访问平台）+ 真实 bash 执行 helper + develop HEAD 完整基线快照
- required_evidence: 12 项全 GREEN；基线 RED `5 ok / 7 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-pkill-project-escape.py
- test_command: python3 docs/system/workspace/scripts/tests/test-pkill-project-escape.py
- expected_output: SUMMARY: 12 ok, 0 failed
- expected_RED_output: SUMMARY: 5 ok, 7 failed（C1/C2/B4/B5/B6 对照组 PASS）
- actual_RED_output: develop `d82ba3e46` 完整基线快照注入最终版 AT-001 → `5 ok, 7 failed`（AT-001-RED.log）
- actual_output: 工位同一断言 → `12 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/raw-20261109T074900Z/verification/test-evidence/AT-001-RED.log,docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/raw-20261109T074900Z/verification/test-evidence/AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 对照组证明未转义路径（`/tmp/work/proj.v1`）的正则确实匹配 sibling（`/tmp/work/projXv1`）、固定 pattern 站点仍在、真实 `pgrep -f` 未转义 pattern 命中 ≥2 进程而 `re.escape` 后只命中 1 个、`bash -n` 通过。静态组核对单一 helper、两处站点使用 `${_project_re}`、无裸 `${project}` 进 pkill、helper 用 `re.escape` + argv。行为组把 helper 从源码抽出在真实 bash 里执行，验证 `. + ( [` 均被转义、转义后不误匹配 sibling、仍匹配自身。
- red_how: fix RED — `git archive develop` 出完整快照并补齐 `.freely/tool-boundary-bootstrap.md`，把最终版 AT-001 拷入快照 tests 目录，以 `--source-dir` 运行。

## End-to-End
- acceptance_target: 真实进程上验证正则误杀与修复
- testing_layer: end-to-end
- target_environment: 两个带标记 python 子进程 + `pgrep -f`
- required_evidence: AT-001（B4/B5）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-pkill-project-escape.py

## Unit
- acceptance_target: helper 转义完整性与静态边界
- testing_layer: unit
- target_environment: fix/raw-20261109T074900Z-dispatch-cas-sse-pkill
- required_evidence: AT-001（S1–S4 + B1–B3）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-pkill-project-escape.py

## Integration
- acceptance_target: 既有外部输入/派发/配置能力不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 完整基线快照
- required_evidence: AT-001 + 5 个相关回归
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-external-input-boundary.py
2. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: PoC 只起两个存活 12s 的 `python3 -c "time.sleep(12)"` 子进程并 `terminate()` 清理，**不调用 pkill、不杀任何真实业务进程、不访问平台**。
- real_environment_reason: 真实 `pgrep -f` 命中数证明未转义 pattern 命中 ≥2 个进程、转义后只命中 1 个；helper 在真实 bash 中输出 `/tmp/work/proj\.v1\+2\(3\)`；`bash -n`、`check-epics-map`、`bin/test-all --ci` 与 5 个相关回归基线对比 0 新增失败。
