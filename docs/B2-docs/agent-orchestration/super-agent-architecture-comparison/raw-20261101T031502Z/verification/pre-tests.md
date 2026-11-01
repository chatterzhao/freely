# Pre-Tests: Super-agent 架构对比、实现质量评估与方向立项

- issue_id: I-20261101T031502Z-A
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 研究文档含 7 处结构性差异、9 个编号章节，概念对照含“同名不同义”
- acceptance_target: 研究结构完整
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study
- required_evidence: 输出 7 / 9 / 1
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/super-agent-architecture-comparison/raw-20261101T031502Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c '^### D[0-9]' docs/B1-docs/raw-20261101T031502Z/brainstorms.md && grep -c '^## [0-9]\.' docs/B1-docs/raw-20261101T031502Z/brainstorms.md && grep -c '^## 8\. 同名不同义' docs/B1-docs/raw-20261101T031502Z/concept-map.md
- expected_output: 7 然后 9 然后 1
- expected_RED_output: 命令失败或计数低于预期
- actual_RED_output: 文档未创建时 grep 返回非零；初稿只有 5 处差异
- actual_output: 7 / 9 / 1
- evidence_file: verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: 初稿只有 5 处差异、无概念对照时计数不足；补齐后达到 7/9/1

### acceptance-2
- id: AT-002
- requirement: 四个 candidate 均为 promoted/proposed，且带 next_action / revisit_trigger
- acceptance_target: candidate 不伪造 promote，可被后续 scan 发现
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study
- required_evidence: 输出 4 / 4 / 4
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/super-agent-architecture-comparison/raw-20261101T031502Z/verification/test-evidence/acceptance-2.log
- test_command: grep -cE '^- status: (promoted|proposed)$' docs/B1-docs/raw-20261101T031502Z/candidates.md && grep -c '^- next_action:' docs/B1-docs/raw-20261101T031502Z/candidates.md && grep -c '^- revisit_trigger:' docs/B1-docs/raw-20261101T031502Z/candidates.md
- expected_output: 4 然后 4 然后 4
- expected_RED_output: 任一计数不等于 4/4/4
- actual_RED_output: 初稿只有 needs_research 且缺 revisit_trigger 时计数不足
- actual_output: 4 / 4 / 4
- evidence_file: verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- red_how: 草稿缺字段或状态未收敛时计数不足；补齐后达到 4

### acceptance-3
- id: AT-003
- requirement: 两张架构图的 HTML 与 SVG 均存在，两个 SVG 共含 4 个 region 标签
- acceptance_target: archify 图产物可交付
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study
- required_evidence: 四个文件非空，输出 4
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/super-agent-architecture-comparison/raw-20261101T031502Z/verification/test-evidence/acceptance-3.log
- test_command: test -s docs/B1-docs/raw-20261101T031502Z/super-agent-vs-freely-collaboration.html && test -s docs/B1-docs/raw-20261101T031502Z/super-agent-vs-freely-collaboration.svg && test -s docs/B1-docs/raw-20261101T031502Z/freely-harness-port-boundary.html && test -s docs/B1-docs/raw-20261101T031502Z/freely-harness-port-boundary.svg && cat docs/B1-docs/raw-20261101T031502Z/super-agent-vs-freely-collaboration.svg docs/B1-docs/raw-20261101T031502Z/freely-harness-port-boundary.svg | grep -c 'data-boundary-label'
- expected_output: 4
- expected_RED_output: 文件缺失或标签数不足
- actual_RED_output: 第二张图生成前文件不存在
- actual_output: 4
- evidence_file: verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: passed
- red_how: 图未生成时 test -s 失败；生成后通过

### acceptance-4
- id: AT-004
- requirement: raw issue 已吸收到 I-*，里程碑同时登记 I-* 与四个 candidate
- acceptance_target: raw/C/M/I 链路可追溯
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study
- required_evidence: 输出 1 / 2 / 3
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/super-agent-architecture-comparison/raw-20261101T031502Z/verification/test-evidence/acceptance-4.log
- test_command: grep -c "^phase_state: absorbed" docs/B1-docs/raw-20261101T031502Z/issue.md && grep -c 'I-20261101T031502Z-A' docs/milestones.md && grep -c 'C-20261101T031502Z-' docs/milestones.md
- expected_output: 1 / 至少 1 / 4
- expected_RED_output: 吸收前 phase_state 为 proposed
- actual_RED_output: phase_state 为 proposed，milestones 无 I-* 条目
- actual_output: 1 / 4 / 4
- evidence_file: verification/test-evidence/acceptance-4.log
- red-green-status: green
- status: passed
- red_how: 吸收前 grep absorbed 返回 0；吸收后通过

### acceptance-5
- id: AT-005
- requirement: develop 合并门禁通过
- acceptance_target: 治理链路完整
- testing_layer: integration
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study
- required_evidence: 输出 Develop merge governance gate passed.
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/super-agent-architecture-comparison/raw-20261101T031502Z/verification/test-evidence/acceptance-5.log
- test_command: ./bin/governance-merge-gate --range develop..HEAD
- expected_output: Develop merge governance gate passed.
- expected_RED_output: 门禁报 raw/C/M/I 链路缺失
- actual_RED_output: 未吸收时门禁报 lifecycle 缺失
- actual_output: Develop merge governance gate passed.
- evidence_file: verification/test-evidence/acceptance-5.log
- red-green-status: green
- status: passed
- red_how: raw 未 absorbed、I-* 未物化时门禁失败；补齐后通过

### acceptance-6
- id: AT-006
- requirement: P0 harness-status 的 5 项单测全部通过
- acceptance_target: 能力矩阵、cache 聚合、require 失败、缺表、未知工具都有回归
- testing_layer: unit
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study
- required_evidence: 输出 Ran 5 tests 与 OK，退出 0
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/super-agent-architecture-comparison/raw-20261101T031502Z/verification/test-evidence/acceptance-6.log
- test_command: python3 docs/system/workspace/scripts/tests/test-harness-status.py
- expected_output: Ran 5 tests 然后 OK
- expected_RED_output: harness_status.py 不存在时 ImportError/FileNotFoundError
- actual_RED_output: 实现前脚本不存在，测试文件全部失败
- actual_output: Ran 5 tests / OK
- evidence_file: verification/test-evidence/acceptance-6.log
- red-green-status: green
- status: passed
- red_how: 先写测试，脚本不存在时 5 项失败；实现后 5 项通过

### acceptance-7
- id: AT-007
- requirement: CLI 能输出合法 JSON，且包含 adapter/cache/roles/required 结构
- acceptance_target: `freely harness-status` 可被脚本消费
- testing_layer: integration
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study
- required_evidence: 输出 ok
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/super-agent-architecture-comparison/raw-20261101T031502Z/verification/test-evidence/acceptance-7.log
- test_command: ./bin/harness-status --project . --json | python3 -c "import json,sys; d=json.load(sys.stdin); assert {'adapter','cache','roles','required'} <= set(d); print('ok')"
- expected_output: ok
- expected_RED_output: bin/harness-status 不存在或输出非 JSON
- actual_RED_output: 实现前入口不存在
- actual_output: ok
- evidence_file: verification/test-evidence/acceptance-7.log
- red-green-status: green
- status: passed
- red_how: 实现前入口不存在；实现后 JSON 可解析

### acceptance-8
- id: AT-008
- requirement: README 的本地链接全部存在，且总览图 SVG/HTML 非空
- acceptance_target: 对外文档不出现死链
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study
- required_evidence: 输出 ok
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/super-agent-architecture-comparison/raw-20261101T031502Z/verification/test-evidence/acceptance-8.log
- test_command: python3 -c "import pathlib,re; s=pathlib.Path('README.md').read_text(); ps=[p for p in re.findall(r'\]\(([^)]+)\)', s) if not p.startswith(('http','#'))]; missing=[p for p in ps if not pathlib.Path(p).exists()]; assert not missing, missing; assert pathlib.Path('docs/assets/freely-architecture.svg').stat().st_size>0; assert pathlib.Path('docs/assets/freely-architecture.html').stat().st_size>0; print('ok')"
- expected_output: ok
- expected_RED_output: README 死链或图缺失时 AssertionError
- actual_RED_output: 初稿 skill 路径不存在时被检查出来
- actual_output: ok
- evidence_file: verification/test-evidence/acceptance-8.log
- red-green-status: green
- status: passed
- red_how: 先跑链接检查；修正 `.claude/skills` 路径后通过

## Unit

- acceptance_target: 本次为文档/研究交付，无运行时代码单元
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 不适用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 变更只含 Markdown/HTML/SVG 与里程碑元数据，没有可单测的函数或模块
- replacement_evidence: acceptance-1 / acceptance-2 的结构校验

## Integration

- acceptance_target: 文档链路与里程碑绑定
- testing_layer: integration
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study
- required_evidence: acceptance-4、acceptance-5
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 集成面由 governance-merge-gate 覆盖，单独集成测试无额外信号
- replacement_evidence: acceptance-5 的门禁输出
