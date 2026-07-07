# Dev 阶段定义

## 是什么

TDD 实现阶段——按 pre-tests 和 prd 写代码。

## 输入

- RED 确认后的 pre-tests.md
- prd.md（实现方案）
- tasks.md（任务分解）

## 输出

- 实现代码（在 fix/raw-* 或 feature/raw-* 工位中）
- git commits（按 B1→B2→RED→dev→GREEN 顺序）
- code-reviews/implementation-decision-note.md

## 完成标志

- 所有 AT 对应的代码改动已实现
- git diff 覆盖 prd 描述的全部改动面
- tasks.md 全部子任务完成
- 代码已 commit
- pre-tests.md 的每条 AT: actual_output 填写（GREEN 阶段执行后填写）

## 完成后做什么

**调用 A2A PATCH state=input-required, reason=needs-review:dev**

Reviewer 按 `review-guidelines/dev-review.md` 检查 TDD 忠实度。
pass → 进入 GREEN。fail → 修复实现。
