# Brainstorm: verification-contract-and-premerge-adequacy-governance

## Key Decisions

1. 这轮先 materialize 成单一 owner，而不是先拆两个 owner。
2. merge gate 的角色是最后兜底并给诊断，不是代替 manager / worker 设计测试。
3. `pre-tests.md` 仍是唯一真源；handoff 与 gate 只消费它的 machine-readable 摘要。
4. `pre-tests.md` 必须有固定四章：`Unit`、`Integration`、`End-to-End`、`Real-Environment`；章节不适用时必须写有限枚举 reason，而不是直接省略。

## Main Tension

如果只加强 prompt，不加强 gate，执行者仍可能在 promote 出口前漏测或漏标状态。
如果只加强 gate，不加强 prompt，执行者会继续在入口就拿不到明确测试义务。

因此最佳边界是：

- prompt 负责前置传达测试义务
- `pre-tests.md` 负责长期 canonical truth
- gate 负责最后兜底并明确失败层级

## Chosen Boundary

本 owner 只冻结三件事：

1. handoff 必带的 verification metadata
2. `pre-tests.md` 的四章骨架与 item-level adequacy schema
3. `test-pre-merge-* -> develop` fallback adequacy gate 的诊断模型

不在本轮同时做：

- 自动测试编排
- 全仓历史回填
- path-based relevance guessing

## Diagnostic Taxonomy

gate 至少应明确区分：

1. `pre_tests_missing`
   - `pre-tests.md` 缺失，或没有写出当前 issue 需要的测试任务 / acceptance items
2. `testcase_derivation_missing`
   - 任务存在，但没从任务派生出具体测试用例 / acceptance item
3. `execution_missing`
   - 测试项存在，但没执行，或 artifact 仍是 `pending://`
4. `verification_state_missing`
   - 已经执行，但 `status`、`not_applicable` 理由、替代证据或完成标记没写对

## Required Sections

`pre-tests.md` 第一阶段至少强制四个章节：

1. `Unit`
2. `Integration`
3. `End-to-End`
4. `Real-Environment`

不适用必须使用有限 reason type：

- `change_not_touching_this_layer`
- `no_executable_boundary_at_this_layer`
- `protected_environment_only`
- `human_observation_only`
- `covered_by_more_realistic_required_surface`

## Expected Landing

完成后，Freely 不再只会给出一个含糊的 “verification inadequate”。
系统会把失败落点明确告诉执行者：

1. 先补 `pre-tests`
2. 还是先把任务派生成测试项
3. 还是先真正执行测试
4. 还是先把测试完成情况和证据回写
