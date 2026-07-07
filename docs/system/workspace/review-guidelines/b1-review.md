# B1 阶段审查指南

## 定位

B1 是问题到决策的阶段。Reviewer 检查：Worker 是否对 raw issue 做了充分的根因分析，brainstorms 是否探索了多个方案，candidate 是否忠实消化了 brainstorms。

## 检查项

### 1. 根因分析质量
- [ ] brainstorms.md 的 Problem/Discovery 是否理解了 raw issue 的核心问题？
- [ ] 是否分析了影响范围和严重程度？
- [ ] 是否有 value_check（确认 issue 仍有价值，未被其他 candidate 覆盖）？

### 2. 方案探索充分性
- [ ] 是否探索了至少 2-3 个方案（Option）？
- [ ] 每个方案是否有具体的优缺点分析（不是走过场的"Option X 最好"）？
- [ ] 选定的方案（Decision）是否有清晰的论证？

### 3. Candidate 忠实消化
- [ ] candidate 的 acceptance_criteria 是否对应 brainstorms 的 Decision？
- [ ] promotion_gate 是否反映边界分析和依赖关系？
- [ ] decision_reason 是否从 brainstorms 推导出来（不是凭空的新想法）？
- [ ] scope 判断是否合理（一个 raw issue → 一个 candidate）？

### 4. 文档完整性
- [ ] brainstorms.md 是否存在且内容充实？
- [ ] candidates.md 是否存在？candidate 字段是否齐全（status/milestone/decision/acceptance_criteria/promotion_gate）？
- [ ] milestones.md 的 candidate_issues 条目是否正确？

## 通过标准

全部检查项通过 → `PASS`。
根因分析是走过场的 → `FAIL, reason=根因分析不充分，需要重新分析 raw issue 的核心问题`。
只有一个方案 → `FAIL, reason=方案探索不足，至少需要 2 个方案的对比分析`。

## 失败处理

输出具体失败原因和建议 → Worker 回到 B1 补充 → 重新提交审查。
