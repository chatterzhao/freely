# Pre-Tests: SDD frontmatter 解析所有权收口
- issue_id: I-20261103T132517Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 同一份 issue frontmatter 只由 `raw_metadata_contract` 一套代码解析；损坏的 frontmatter 不再静默变成空 dict，而是显式报 `metadata_validation_error`；`scan`、`bin/issue-sync`、门禁对同一份坏输入给出一致结论；存量 23 份坏文档被幂等修复；**历史格式不退化**——无 YAML 块的 linked 文档仍按 `- key: value` bullet 解析，且 186 处 bullet 声明的 `phase_state` 一个都不能丢
- acceptance_target: 「frontmatter 坏了」这件事从「AI 反复做无用功的隐性症状」变成一条可定位、可修复的显式错误；且收口动作不把 184 份历史格式文档误判为损坏
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 隔离 git/文件夹具（真实 `task-lifecycle-scan.py::parse_frontmatter`、真实 `raw_metadata_contract.parse_issue_text`、真实 `frontmatter_contract_cli.py`、真实 `read_issues_dir`）+ develop HEAD 基线快照对比 + 真机全量 B1/B2 文档只读校验
- required_evidence: 9 静态 + 12 行为共 21 项全 GREEN；18 项相关回归 worktree/baseline 退出码对比；全量 1082 份 B1+B2 文档解析差异逐份定性
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-frontmatter-ownership.py
- test_command: python3 docs/system/workspace/scripts/tests/test-frontmatter-ownership.py all
- expected_output: SUMMARY: 21 ok, 0 failed
- expected_RED_output: SUMMARY: 7 ok, 14 failed（静态 5：无 CLI、契约无新入口、scan 仍自带 `yaml.safe_load`、`_fm_get` 非薄封装、无 repair；行为 2：glued 文档 scan 仍返回空、`read_issue` 抛 `ParserError` 而非 `MetadataValidationError`；CLI 相关 6 项因单所有者缺失整体 FAIL；真机 827 份 B1 因基线无 `parse_issue_text` 全部计为不可严格解析）
- actual_RED_output: develop `6ab036e29` 基线快照（`git archive develop -- bin docs .githooks templates`）注入**最终版** AT-001 → `SUMMARY: 7 ok, 14 failed`（AT-001-RED.log）。7 项 PASS 是既有能力守卫 + 历史格式守卫（`legacy bullet-only linked issue keeps parsing`、`no real B2 linked issue is misreported as damaged`、`every bullet-declared phase_state survives`），证明夹具可跑通、且这两条守卫在旧实现上本就成立（它们守的是「不要退化」，不是「新功能」）
- actual_output: 工位同一断言 → `SUMMARY: 21 ok, 0 failed`（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/gate/platform/raw-20261103T132517Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log,AT-001-REGRESSION-BASELINE.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3,T4,T5,T6,T7,T8,T9
- case_design: 静态组断言「单一所有者已接线」（CLI 存在、契约暴露 `validate_issue_path`/`parse_issue_text`、scan 不再自带 `yaml.safe_load`、`_fm_get` 是薄封装、repair 默认 dry-run 且幂等）。行为组用隔离夹具覆盖 5 种输入：①glued 闭合 `---`；②git 冲突标记；③非法 YAML；④**无 YAML 块的 legacy bullet 文档**；⑤正常文档。再驱动真实 `read_issues_dir` 断言错误进入 `metadata_validation_error` 而非空 phase。最后对真机全量 B1（827 份）+ B2 I-*（255 份）做只读校验与「零假损坏 / 零 phase_state 丢失」双守卫。真实项目 `.freely/run` 零写入。
- red_how: fix RED — `git archive develop -- bin docs .githooks templates` 出基线快照 `/tmp/r18-base`，把最终版 AT-001 拷入快照的 `docs/system/workspace/scripts/tests/`，以 `--source-dir /tmp/r18-base` 运行，基线文件一个不改。

## End-to-End
- acceptance_target: 坏 frontmatter 从「静默空 metadata」变成「显式可定位错误」，且 repair 能把它修好；历史 bullet 格式文档不被误判
- testing_layer: end-to-end
- target_environment: 隔离夹具（真实 `read_issues_dir` + 真实 `parse_issue_text` + 真实 CLI 子进程）驱动完整链路：坏文档落盘 → scan 读取 → 错误上浮 → CLI 读取失败 → repair 修复 → 严格解析通过 → scan 不再报错
- required_evidence: AT-001（行为 12 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-frontmatter-ownership.py behavior

## Unit
- acceptance_target: frontmatter 单一所有者契约
- testing_layer: unit
- target_environment: fix/raw-20261103T132517Z-sdd-frontmatter-ownership
- required_evidence: AT-001（静态 9 项）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-frontmatter-ownership.py static

## Integration
- acceptance_target: frontmatter 解析/写入收口后，issue-sync 写通道、生命周期、severity、证据链、平台副本、打包安装态等既有能力不退化
- testing_layer: integration
- target_environment: 工位 + 未修改 develop HEAD 基线快照
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. bash docs/system/workspace/scripts/tests/test-platform-write-channel
2. bash docs/system/workspace/scripts/tests/test-issue-sync-close-terminal-first
3. bash docs/system/workspace/scripts/tests/test-issue-sync-promote-b2
4. bash docs/system/workspace/scripts/tests/test-test-gate-record
5. bash docs/system/workspace/scripts/tests/test-wt-close-comment-scan
6. bash docs/system/workspace/scripts/tests/test-governance-gate-batch-read
7. python3 docs/system/workspace/scripts/tests/test-raw-reconciliation.py
8. python3 docs/system/workspace/scripts/tests/test-raw-replica-degraded.py
9. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-raw-metadata.py
10. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-materialization.py
11. python3 docs/system/workspace/scripts/tests/test-feedback-severity.py all
12. python3 docs/system/workspace/scripts/tests/test-install-state.py all
13. python3 docs/system/workspace/scripts/tests/test-github-label-autocreate.py all
14. python3 docs/system/workspace/scripts/tests/test-platform-handler-probe.py
15. python3 docs/system/workspace/scripts/tests/test-scan-frontmatter-nested.py
16. python3 docs/system/workspace/scripts/tests/test-platform-open-parity.py
17. python3 docs/system/workspace/scripts/tests/test-test-evidence-chain.py all
18. python3 docs/system/workspace/scripts/tests/test-command-lifecycle-wt-close.py
19. bin/test-all --ci

## Real-Environment
- real_environment_status: pass
- real_environment_exception: 行为测试全在隔离夹具里跑，不写真实 `.freely/run`；真实环境只做**只读**全量校验（1082 份 B1+B2 文档严格解析 + 与 develop 基线逐字段对比），修复真实文档时用 `repair --apply` 且第二次 dry-run 必须为 0。真实证据由本轮收口时在 test-pre-merge 工位执行 `freely test-gate run` 产生，门禁据此放行 `pr-create-guarded`。
- real_environment_reason: 18 项回归中 16 项 MATCH；`test-platform-open-parity.py` 的 DIFF 是已登记的 R59 数据缺陷（`20261108T134701Z` GitHub 副本缺失，Gitee IKTSRS）——基线快照无平台访问能力，空集合对空集合假 OK，非本分支退化；`test-command-lifecycle-wt-close.py` 为预存红，两边同值；`test-test-evidence-chain.py` 首轮基线 red 是快照漏了 `.gitee-ci.yml`/`.github`，补齐后 MATCH，均已在回归日志写明。

## 全量解析不退化口径

对 `docs/B1-docs/*/issue.md` + `docs/B2-docs/**/issues/I-*.md` 共 1082 份文档，比较「develop 基线解析结果」与「工位解析结果」：

- 差异文档 25 份 = 23 份本轮修复的存量文档（12 B1 + 11 B2）+ 2 份本 issue 自己新增的 B1/B2 文档；
- 除这 25 份外，其余 1057 份字段级完全一致；
- 工位侧 `metadata_validation_error` 计数为 **0**（收口前该口径会误报 184 份历史格式文档）；
- 186 处 `- phase_state:` bullet 声明全部仍能解析出 `phase_state`。
