# 预研头脑风暴：candidate 验收边界、独立评审与 IBM 验收深化

## 背景

- Freely 的 pre-brainstorm 已能产出 `candidates.md` 并同步进入 `docs/milestones.md.candidate_issues`。
- 但 candidate 更像“问题摘要 + next_action”，缺少 candidate-level acceptance boundary。
- 同时，candidate 准备 promotion 到 IBM 时，也缺少规范化的独立 acceptance review 记录。
- 另外，IBM 过程虽然已经有 `prd.md` / `pre-tests.md` / `tasks.md` / issue-bound brainstorm，但还缺一条更明确的真源语义：
  - candidate 的 acceptance boundary 进入 IBM 后，应被继续深化成 issue-level acceptance，而不是简单复制或丢失。

## 主问题

需要同时解决两层问题：

1. 如何保证 future pre-brainstorm candidate 一定带 candidate-level acceptance boundary。
2. 如何保证进入 IBM 后，这层边界继续深化成 issue-level acceptance。

## 核心判断

最小可执行方案：

1. `candidate_format_version: v2`
- future candidate 默认使用 `v2`
- `v2` candidate 至少必须包含：
  - `acceptance_criteria`
  - `promotion_gate`
  - `open_questions`
  - `acceptance_reviews`

2. 独立 acceptance review
- candidate 准备 promotion 时，至少一次独立 review
- reviewer 优先：
  - subagent
  - fresh process
  - peer worker
- 高风险 candidate 再升到两次独立 review，而不是默认全部双审

3. IBM acceptance deepening
- candidate-level acceptance 不等于 issue-level acceptance
- 进入 IBM 后，应把：
  - `acceptance_criteria`
  - `promotion_gate`
  - `open_questions`
  深化到：
  - issue scope
  - issue acceptance
  - pre-tests
  - tasks
  - issue-bound brainstorm unresolved points

## enforcement 应放哪里

### 写入真源

- `candidate-recording.md`
- `doc-pre-brainstorm-execution/SKILL.md`

### 自动门禁

- `governance-check`

它负责：

- 对 `candidate_format_version: v2` 强制检查字段存在
- 对 `status: promoted` 的 `v2` candidate 强制至少一条 `acceptance_reviews`

### IBM 真源

- `doc-ibm-execution/SKILL.md`
- `issue-materialization-checklist.md`
- `ibm-completion-gate.md`

它负责表达：

- candidate acceptance 如何被 issue-level acceptance 吸收和深化

## 为什么不把内容质量硬编码进门禁

`governance-check` 只检查：

- 字段存在
- promoted 时 review 记录存在

它不判断内容质量。

内容质量仍由独立 AI review 判断，否则又会变回硬编码规则表。

## candidate-level acceptance

它回答：

- 这一轮 pre-brainstorm 什么时候算完成
- promotion 到 IBM 前还差哪些边界
- 当前还没收敛的问题是什么

最小字段：

- `acceptance_criteria`
- `promotion_gate`
- `open_questions`

## acceptance review 记录

`acceptance_reviews` 是 candidate 的规范化 review 区。

最小结构：

- `reviewer`
- `mode`
- `summary`
- `verdict`

推荐 `verdict`：

- `pass`
- `needs_more_research`
- `block_promotion`

## IBM acceptance deepening

进入 IBM 后，不应只说“issue scope 与 acceptance 稳定”。

还应更明确地表达：

- candidate 的 acceptance boundary 已被 issue-level acceptance 吸收
- `pre-tests.md` 与 `tasks.md` 已体现这层深化
- issue-bound brainstorm 中未决问题已足够收敛，不再阻断 dev

也就是说：

- pre-brainstorm 负责 candidate-level acceptance
- IBM 负责 issue-level acceptance deepening

## 完成标志

- future candidate 有可检查的 v2 schema
- promotion 前独立 review 有规范化落点
- `governance-check` 能拦住 future v2 candidate 缺字段
- IBM 真源已明确“从 candidate acceptance 到 issue acceptance deepening”的关系
