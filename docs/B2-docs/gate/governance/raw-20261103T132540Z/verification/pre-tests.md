# Pre-Tests: 合并门禁读 verdict，评审判定不再默认通过
- issue_id: I-20261103T132540Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 合并侧只认字面 `pass`（`fail`/`needs_changes`/缺失/不可解析一律阻断并打印原因）；写侧默认值由 `pass` 反转为 `needs_changes` 且不再出现 `_review_verdict="pass"` 默认赋值；`--verdict` 覆盖只接受三值、缺 `--reason` 被拒、reason 落痕进 review 文档；审计侧 `completed` 不再裸 `continue`，要求绑定 review 产物且声明 `verdict=pass`，显式非 pass 不可翻盘；401 份真实 review 文档（含 `- verdict: **pass**` 粗体历史写法）解析零不可判定；解析逻辑全仓只有一份
- acceptance_target: 修复「文件存在即评审通过」以及「无法判定默认通过」的双层失真，让合并门禁的强制力第一次建立在真实证据上
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: fix 工位 + develop HEAD 基线快照（`git archive develop -- docs bin`）
- required_evidence: 新增回归测试 19 项静态断言 + 4 个判定行为场景 + 真实语料普查全 GREEN；11 个回归以未修改 develop HEAD 基线对比零新增失败；真实工位 `verdict: fail` 反向探针阻断
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-verdict-contract
- test_command: bash docs/system/workspace/scripts/tests/test-verdict-contract all
- expected_output: SUMMARY: 13 ok, 0 failed（19 项静态断言全 ok、CASE A–J 十个行为场景全 ok、census 401 review docs / 399 with verdict / 0 unparseable）
- expected_RED_output: SUMMARY: 2 ok, 2 failed（静态 19 项中 13 项 FAIL：shared helper 缺失、assist 断言连带失败、merge guard 仍按文件存在打印 pass、review guard 默认 pass、gate completed 裸 continue；behavior 因 shared helper 缺失整体中止）
- actual_RED_output: develop HEAD 基线快照（`git archive develop -- docs bin`，未含本轮任何改动）运行最终版 AT-001 —— 静态 13 项 FAIL / 5 项 PASS（PASS 的是 bash -n 与两条既有文案断言），behavior 首行即 `[FAIL] helper missing (cannot test parsing)` 中止，汇总 `SUMMARY: 2 ok, 2 failed`；证明能力整体缺失而非部分退化（AT-001-RED.log）
- actual_output: 工位运行同一份最终版断言：静态 19 项全 ok（含「merge guard 不得出现第二份 verdict 正则」「gate 必须用共享解析器」「gate completed 必须要求绑定 review」），CASE A–E 解析五态、CASE G–J 合并决策四态（fail 阻断 / 粗体 pass 放行 / 无 verdict 阻断 / needs_changes 阻断）、CASE F 真实语料普查 `401 review docs, 399 with verdict, 0 unparseable`，汇总 `SUMMARY: 13 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/governance/raw-20261103T132540Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,AT-001-REGRESSION-BASELINE.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: static 组用 Python 同时读 wrapper + 解析模块 + 三个消费者，断言「共享真源存在 / 读侧委托共享判定 / 无第二份正则 / 写侧无 pass 默认 / gate 必须要求绑定 review」；behavior 组直接调用读侧真正使用的判定函数 `freely_review_verdict_check`（不是复制逻辑），覆盖 fail、粗体 pass、无 verdict、needs_changes 四态并断言退出码；CASE F 对 401 份真实 review 文档逐份解析，防历史写法自锁。
- red_how: fix RED — `git archive develop -- docs bin` 出未修改基线快照，把最终版测试拷入后运行；不修改任何基线文件。

## Unit
- acceptance_target: verdict 解析契约（两种历史写法、粗体/反引号/引号剥离、非法值 fail-closed）
- testing_layer: unit
- target_environment: fix/raw-20261103T132540Z-verdict-contract
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-verdict-contract static

## Integration
- acceptance_target: R8 门禁 fail-closed / R9 commit-msg 接线 / R9.5 receipt 审计 / wt-create 四态与既有治理能力不退化
- testing_layer: integration
- target_environment: 工位 + 未修改 develop HEAD 基线对比
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-gate-fail-closed all
2. bash docs/system/workspace/scripts/tests/test-commit-msg-wireup all
3. bash docs/system/workspace/scripts/tests/test-governance-receipt-audit all
4. bash docs/system/workspace/scripts/tests/test-wt-create-four-state-dir all

## End-to-End
- acceptance_target: 真实工位反向探针（review 写 `verdict: fail` → 合并侧与审计侧都阻断）+ 真实 pass 受控合并
- testing_layer: end-to-end
- target_environment: fix 工位真实 pr-merge-guarded / governance-merge-gate --staged
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-verdict-contract all
2. review 文档置 `- verdict: fail` → ./bin/freely pr-merge-guarded develop <branch> 非零退出并打印 blocked
3. review 文档置 `- verdict: fail` 并 stage → governance-merge-gate --staged 报 completed 非 pass
4. 还原 pass 后真实 pr-merge-guarded 成功合并

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 全部改动在真实 fix 工位用项目真源命令（`./bin/freely`、`bash docs/system/workspace/scripts/tests/...`）执行；RED 基线取自 `git archive develop`（不改基线文件）；真实 review 文档 401 份普查零不可判定；反向探针在真实工位对真实门禁执行；最终以真实 `pr-create-guarded` / `pr-merge-guarded` / `wt-close` 闭环。
