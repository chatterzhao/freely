# PRD: candidate-acceptance-review-governance

## Problem

candidate 若没有显式 acceptance boundary 和 promotion 前独立 review，就会让 IBM materialization 与后续验收边界依赖临场判断。

## Product Requirement

Freely 必须对 future candidate 建立最小 acceptance schema、独立 acceptance review 记录，并在 IBM 阶段深化为 issue-level acceptance。

## Non-goals

- 不让 `governance-check` 判断内容质量
- 不要求所有 candidate 默认双审
- 不把 candidate acceptance 和 issue acceptance 混成同一层语义
