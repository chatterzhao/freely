# Pre-Tests: 外部输入不进代码体 + sed 跨平台
- issue_id: I-20261103T132636Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 外部分支名不得进入 `python3 -c` 脚本体（改为 argv）；工作区不得残留 BSD-only 的 `sed -i ''`；每个 `sed -i.bak` 必须在同一命令内清理备份
- acceptance_target: 审查外部 PR 不会在 maintainer 机器上执行攻击者代码；评审通过后的状态推进不再因 GNU sed 中止
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实工作区扫描 + 真实 bash/python 子进程（可执行注入 PoC）+ 临时文件上的 sed 行为；develop HEAD 基线快照对比
- required_evidence: 3 静态 + 4 行为共 7 项全 GREEN；基线 RED `4 ok / 3 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-external-input-boundary.py
- test_command: python3 docs/system/workspace/scripts/tests/test-external-input-boundary.py
- expected_output: SUMMARY: 7 ok, 0 failed
- expected_RED_output: SUMMARY: 4 ok / 3 failed（2 处插值仍在、6 处 BSD sed、1 处 `.bak` 无清理；4 项 PASS 是 PoC 与 sed 行为——它们本就成立，用来证明断言没有测错东西）
- actual_RED_output: develop `b6a0f392b` 基线快照注入最终版 AT-001 → `SUMMARY: 4 ok, 3 failed`（AT-001-RED.log）。PoC 输出 `fix/x\nPWNED`，证明插值形式确实执行攻击者代码。
- actual_output: 工位同一断言 → `SUMMARY: 7 ok, 0 failed`（AT-001-GREEN.log）；argv 形式输出 `GOT=fix/x');print('PWNED');#`（原样回显、无额外执行）。
- evidence_file: docs/B2-docs/runtime/daemon/raw-20261103T132636Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4
- case_design: 静态组扫描工作区（排除 tests）：`pr-review-guarded` 不得出现 `try_canonicalize_raw_key('$`、不得有 `sed -i ''`、每个 `sed -i.bak` 同行须有 `rm -f`。行为组用可执行 PoC 证明旧形式会执行 `print('PWNED')`，再用 argv 形式证明 payload 被原样接收且无额外输出；最后在临时文件上验证 `sed -i.bak` 生效且无 `.bak` 残留。
- red_how: fix RED — `git archive develop -- bin docs .githooks templates .gitee-ci.yml .github` 出 `/tmp/r22-base`，把最终版 AT-001 拷入快照 tests 目录，以 `--source-dir /tmp/r22-base` 运行。

## End-to-End
- acceptance_target: 注入 PoC 与 sed 真实行为
- testing_layer: end-to-end
- target_environment: 真实 bash/python 子进程 + 临时文件
- required_evidence: AT-001（行为 4 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-external-input-boundary.py

## Unit
- acceptance_target: 静态边界（插值形式、sed 形式、备份清理）
- testing_layer: unit
- target_environment: fix/raw-20261103T132636Z-no-string-codegen
- required_evidence: AT-001（静态 3 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-external-input-boundary.py

## Integration
- acceptance_target: 既有 git/生命周期能力不退化
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 相关回归
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-wt-close-comment-scan
2. bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2
3. python3 docs/system/workspace/scripts/tests/test-source-safe-library.py
4. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 注入 PoC 只在临时字符串上执行 `print`，不访问平台、不改仓库；sed 行为在临时文件上验证。
- real_environment_reason: 两处缺陷都只在真实 shell/python 执行时暴露；`bash -n` + `bin/test-all --ci` + `test-source-safe-library.py` + `test-wt-close-comment-scan` + `test-issue-sync-promote-b2` 全绿，确认替换未破坏既有命令。
