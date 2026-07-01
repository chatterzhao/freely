# PRD: 修复 _review_guide 未定义变量

## Goal
修复 `bin/pr-review-guarded` L506 未定义变量导致的 crash。

## Scope
- 单行修复：L506 `$_review_guide` → `skill:freely-tdd-review`
- 无其他文件改动
- 无 API 变更

## Dev-Loop Handoff
- RED: 确认 ACP 不可用时脚本 crash
- dev: 应用修复
- GREEN: bash -n 语法检查 + 验证变量引用
