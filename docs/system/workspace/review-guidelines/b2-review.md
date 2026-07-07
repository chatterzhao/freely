# B2 阶段审查指南

## 定位

B2 是设计到交付的阶段。Reviewer 检查：I-* issue 是否物化完整，设计产物（prd/pre-tests/tasks/code-review）是否覆盖了全部改动面，pre-tests 是否真实可执行。

## 检查项

### 1. I-* issue 物化完整性
- [ ] I-* issue 文件是否存在？
- [ ] 字段是否齐全（issue_id/phase_state/source_candidate/verification_artifact_dir/pre_tests_path）？
- [ ] milestones.md committed_issues 条目是否存在且路径正确？

### 2. PRD 质量
- [ ] prd.md 是否包含 Goal → 实现方案 → Dev-Loop Handoff？
- [ ] 实现方案是否基于 brainstorms 的分析结论？
- [ ] 改动范围是否清晰（列出具体文件）？

### 3. Pre-tests 覆盖度（重点）
- [ ] 是否覆盖全部改动面（不是挂一漏万）？
- [ ] 每条 acceptance item 的 test_command 是否真实可执行（不是占位符）？
- [ ] 测试层级是否合理（端到端优先，集成第二，单元第三）？
- [ ] Unit/Integration/End-to-End/Real-Environment 四个 section 是否完整？
- [ ] 每个 acceptance item 的 expected_output 是否具体可验证？

### 4. 文档完整性
- [ ] tasks.md 是否存在且任务分解合理？
- [ ] code-reviews/ 目录是否存在？
- [ ] Implementation Decision Note 的 5 字段是否完整（decision/why_this/alternatives/boundary/residual_risk）？

## 通过标准

全部检查项通过 → `PASS`。
pre-tests 有占位符 test_command → `FAIL, reason=AT-00X 的 test_command 是占位符，需要真实可执行的测试命令`。
pre-tests 未覆盖主要改动面 → `FAIL, reason=pre-tests 遗漏了 {改动面}，需要补充对应的 acceptance item`。

## 失败处理

输出具体失败原因 + 缺失文件/字段列表 → Worker 回到 B2 补充 → 重新提交审查。
