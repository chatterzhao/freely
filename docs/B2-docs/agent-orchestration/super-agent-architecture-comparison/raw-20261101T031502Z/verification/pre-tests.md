# Pre-Tests: Super-agent 架构对比研究与方向立项

- issue_id: I-20261101T031502Z-A
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: B1 研究文档包含 Input / Problem / 九个编号章节 / Appendix，且有 5 处结构性差异
- acceptance_target: 研究文档结构完整
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study
- required_evidence: 命令退出 0，输出 5
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/super-agent-architecture-comparison/raw-20261101T031502Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c '^### D[0-9]' docs/B1-docs/raw-20261101T031502Z/brainstorms.md && grep -c '^## [0-9]\.' docs/B1-docs/raw-20261101T031502Z/brainstorms.md
- expected_output: 5 然后 9
- expected_RED_output: 命令失败或计数小于 5
- actual_RED_output: 文档未创建时 grep 返回非零；创建后计数达到 5/9
- actual_output: 5 / 9
- evidence_file: verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: 文档未写时 grep 失败；写作后计数达到预期

### acceptance-2
- id: AT-002
- requirement: 两个 candidate 均为 needs_research，且带 next_action / revisit_trigger / milestone
- acceptance_target: candidate 不伪造 promote，可被后续 scan 发现
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study
- required_evidence: 输出 2 / 2 / 2
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/super-agent-architecture-comparison/raw-20261101T031502Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c '^- status: needs_research' docs/B1-docs/raw-20261101T031502Z/candidates.md && grep -c '^- next_action:' docs/B1-docs/raw-20261101T031502Z/candidates.md && grep -c '^- revisit_trigger:' docs/B1-docs/raw-20261101T031502Z/candidates.md
- expected_output: 2 然后 2 然后 2
- expected_RED_output: 任一计数不等于 2
- actual_RED_output: 初始候选草稿缺少 revisit_trigger 时计数为 0
- actual_output: 2 / 2 / 2
- evidence_file: verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- red_how: 草稿缺字段时计数为 0；补齐后达到 2

### acceptance-3
- id: AT-003
- requirement: 架构对比图 HTML 与 SVG 均存在，SVG 含两个 region 标签
- acceptance_target: archify 图产物可交付
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study
- required_evidence: 文件非空，输出 2
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/super-agent-architecture-comparison/raw-20261101T031502Z/verification/test-evidence/acceptance-3.log
- test_command: test -s docs/B1-docs/raw-20261101T031502Z/super-agent-vs-freely-collaboration.html && test -s docs/B1-docs/raw-20261101T031502Z/super-agent-vs-freely-collaboration.svg && grep -c 'data-boundary-label' docs/B1-docs/raw-20261101T031502Z/super-agent-vs-freely-collaboration.svg
- expected_output: 2
- expected_RED_output: 文件缺失或标签数不足
- actual_RED_output: 生成前文件不存在
- actual_output: 2
- evidence_file: verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: passed
- red_how: 图未生成时 test -s 失败；生成后通过

### acceptance-4
- id: AT-004
- requirement: raw issue 已吸收到 I-*，里程碑同时登记 I-* 与两个 candidate
- acceptance_target: raw/C/M/I 链路可追溯
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261101T031502Z-super-agent-collab-study
- required_evidence: 输出 absorbed / 1 / 2
- evidence_level: real_env
- artifact_ref: docs/B2-docs/agent-orchestration/super-agent-architecture-comparison/raw-20261101T031502Z/verification/test-evidence/acceptance-4.log
- test_command: grep -c "^phase_state: absorbed" docs/B1-docs/raw-20261101T031502Z/issue.md && grep -c 'I-20261101T031502Z-A' docs/milestones.md && grep -c 'C-20261101T031502Z-' docs/milestones.md
- expected_output: 1 / 至少 1 / 2
- expected_RED_output: 吸收前 phase_state 为 proposed
- actual_RED_output: phase_state 为 proposed，milestones 无 I-* 条目
- actual_output: 1 / 2 / 2
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
