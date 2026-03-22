# Brainstorm: integration-acceptance-first-verification-governance

## Goal

把“AI-native 验收优先看 integration / acceptance evidence”收进 IBM 与 verification 真源，避免后续 Freely 再退化成默认先读代码。

## Key Decisions

1. `pre-tests.md` 不是附属清单，而是 issue-level acceptance 控制面。
2. `pre-tests.md` 应优先描述：
   - smoke / integration / regression / non-goals
   - `pre-merge` 与 `post-merge` 验收分界（如存在）
3. verification 的默认顺序不是：
   - read code first
   - then maybe test
   而应是：
   - run or inspect integration / acceptance evidence first
   - then read code only where needed to explain risk or regression
4. code review 仍存在，但默认是二级验证面，不是主导 acceptance 面。

## Non-Goals

- 不在本 issue 中引入新的测试框架
- 不在本 issue 中统一所有 verification review 模板格式
- 不把“集成测试优先”误写成“永远不需要代码评审”

## Outcome

把 IBM / PRD / pre-tests / three-loop / LAWS 的关系写清，形成统一口径。
