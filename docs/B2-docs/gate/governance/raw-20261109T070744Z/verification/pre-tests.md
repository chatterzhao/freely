# Pre-Tests: 门禁区分「修复既有损坏」与「多 issue 混入」
- issue_id: I-20261109T070744Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 一份前置 frontmatter 不可解析的 issue 文档被跨 key 修复时，门禁不得把它当作本次 merge 的 owner（GATE 1 / phase-vs-code / review-artifact / milestone 归属全部跳过），且 `--staged`（`pr-merge-guarded` 实际走的路径）与 `--range` 两条路径都要生效；基线可解析的跨 key 文档仍必须被拦截
- acceptance_target: 历史坏文档有合法修复路径，同时「一工位多 issue」纪律不被放宽
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 真实 gate 模块（`quality/governance-merge-gate`，非常量桩）+ 临时 git 仓库（真实 `git init` / commit / HEAD 基线）+ develop HEAD 基线快照对比；真机由 `raw-20261103T132517Z` 的 PR 合并验证
- required_evidence: 6 夹具 + 6 仓库/选择 + 1 反向守护共 13 项全 GREEN；develop 基线 RED `5 ok / 8 failed`
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-governance-structural-repair-exemption.py
- test_command: python3 docs/system/workspace/scripts/tests/test-governance-structural-repair-exemption.py all
- expected_output: SUMMARY: 13 ok, 0 failed
- expected_RED_output: SUMMARY: 5 ok / 8 failed（基线无豁免能力：4 类损坏判定全 False、staged/range 基线读取返回空、owner 剔除集合为空；5 项 PASS 是「不误判」守卫——正常 YAML、legacy bullet-only、干净基线不进豁免、反向守护）
- actual_RED_output: develop `6ab036e29` 基线快照运行**最终版** AT-001 → `SUMMARY: 5 ok, 8 failed`（AT-001-RED.log）。基线模块可加载但缺 `select_repair_only_paths`，测试以「无能力 stub」继续，逐项报告缺失行为。
- actual_output: 工位同一断言 → `SUMMARY: 13 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/governance/raw-20261109T070744Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5
- case_design: 夹具组直接喂 6 种 frontmatter 文本（glued 闭合 / 成对冲突标记 / YAML 内混入 bullet / 相邻字段粘连 / 正常 YAML / legacy bullet-only），断言损坏判定。仓库组在临时 git 仓库里提交损坏与干净两份 issue 文档，修改工作树后分别以 `--staged` 与 `--range` 解析基线，断言只有损坏那份被选入豁免集合。反向守护断言「可解析的跨 key 文档不被豁免」。
- red_how: fix RED — 同 #4148 的基线快照 `/tmp/r18-base`（develop `6ab036e29`），把最终版 AT-001 拷入快照 tests 目录，以 `--source-dir /tmp/r18-base` 运行。

## End-to-End
- acceptance_target: 真实 gate 模块在 staged / range 两条执行路径上都能识别损坏基线
- testing_layer: end-to-end
- target_environment: 临时 git 仓库 + 真实 gate 模块（`SourceFileLoader` 加载，非桩）
- required_evidence: AT-001（仓库组 6 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-governance-structural-repair-exemption.py repo

## Unit
- acceptance_target: 四类损坏与两类「不是损坏」的判定
- testing_layer: unit
- target_environment: fix/raw-20261109T070744Z-gate-structural-repair
- required_evidence: AT-001（夹具组 6 项 + 反向守护 1 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-governance-structural-repair-exemption.py fixture

## Integration
- acceptance_target: 门禁自身不退化（既有候选/里程碑/issue 链校验保持）
- testing_layer: integration
- target_environment: 工位 + develop HEAD 基线快照
- required_evidence: AT-001 + 相关回归
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-governance-gate-batch-read
2. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
3. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
4. python3 docs/system/workspace/scripts/tests/test-issue-sync-promote-b2

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 行为测试用临时 git 仓库，不触碰真实仓库历史；真实环境验证是「`raw-20261103T132517Z` 的 PR #4235 在 develop 侧合并门禁通过」，本轮收口时用 `freely pr-merge-guarded` 实测。
- real_environment_reason: 该缺陷只有在 `pr-merge-guarded` 于 develop 上触发 `pre-merge-commit`（`--staged`）时才暴露；AT-001 的 staged 用例就是按这条路径构造的，22:11 的实跑日志显示 28 条错误，修复后降为结构性修复 warning。
