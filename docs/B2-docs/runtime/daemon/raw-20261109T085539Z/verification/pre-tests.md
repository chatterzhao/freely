# Pre-Tests: worker 派发 JSON 化 + 边界 lint
- issue_id: I-20261109T085539Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: TSV 通道删除、派发走 JSON；含 tab/换行/引号的 prompt 逐字节保留；6 字段边界与顺序不变；畸形行显式报告并跳过；lint 覆盖 `python3 -c` 插值且不误报 argv 安全形式
- acceptance_target: 含代码块的 AI prompt 不再让 worker 被误标 `worktree_missing`
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 Python 子进程发射/解码 + 真机 bash `read -r -d ''` 冒烟 + develop HEAD 完整基线快照
- required_evidence: 16 项全 GREEN；基线 RED `3 ok / 13 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-worker-task-json-boundary.py
- test_command: python3 docs/system/workspace/scripts/tests/test-worker-task-json-boundary.py
- expected_output: SUMMARY: 16 ok, 0 failed
- expected_RED_output: SUMMARY: 3 ok, 13 failed（C1 旧 TSV 错位对照、C2 R22 argv 形式仍在、B9 R22 回归全绿）
- actual_RED_output: develop `bb5770500` 完整基线快照注入最终版 AT-001 → `3 ok, 13 failed`（AT-001-RED.log）
- actual_output: 工位同一断言 → `16 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/runtime/daemon/raw-20261109T085539Z/verification/test-evidence/AT-001-RED.log,docs/B2-docs/runtime/daemon/raw-20261109T085539Z/verification/test-evidence/AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 对照组直接模拟旧 TSV 拼接公式证明字段错位机理、确认 R22 argv 形式仍在、R22 回归全绿。静态组核发射侧 JSON Lines、解码器存在、派发循环不再按 tab 切分、`except: pass` 被替换、lint 存在。行为组构造含 `\t`/`\n`/`"`/`$HOME` 的 prompt 走发射→解码全链路，逐字节核对 message 与 6 字段顺序；插入畸形行验证 stderr 报告与跳过；空输入 no-op；lint 对违规片段 rc=1、对 argv 安全片段 rc=0、对真实 runtime 输出可计数基线。
- red_how: fix RED — `git archive develop` 出完整快照并补齐 `.freely/tool-boundary-bootstrap.md`，把最终版 AT-001 拷入快照 tests 目录，以 `--source-dir` 运行。

## End-to-End
- acceptance_target: 真实 bash 用 runtime 同款 read 形状消费 NUL 流，字段不串位
- testing_layer: end-to-end
- target_environment: 真实 bash 子进程 + 临时 NUL 流文件
- required_evidence: AT-001（B2/B4）+ 真机冒烟
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-worker-task-json-boundary.py

## Unit
- acceptance_target: JSON Lines 发射与 NUL 解码
- testing_layer: unit
- target_environment: fix/raw-20261109T085539Z-state-file-tsv-boundary
- required_evidence: AT-001（B1/B3/B5）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-worker-task-json-boundary.py

## Integration
- acceptance_target: 既有外部输入边界与生命周期能力不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 完整基线快照
- required_evidence: AT-001 + 6 个相关回归
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-external-input-boundary.py
2. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 故障注入在临时文件与 mock 层完成，不访问平台、不派发真实 worker；真机冒烟只验证 bash 读取形状。
- real_environment_reason: 用与 runtime 完全相同的 `while IFS= read -r -d '' ...; done < stream` 形状读取含 tab/换行/引号的 prompt，输出 `msg_tab_preserved=yes` / `msg_quote_preserved=yes` / `worktree=/tmp/wt`（未被污染）；`bash -n`、`check-epics-map`、`bin/test-all --ci` 与 6 个相关回归基线对比通过。
