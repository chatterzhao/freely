# PRD: I-20261114T111702Z-A

- issue_id: I-20261114T111702Z-A
- source_candidate: docs/B1-docs/raw-20261114T111702Z/candidates.md#C-20261114T111702Z-A

## Goal

修复 `freely comment` 在平台评论写成功后因 `${PROJECT_ROOT}` 未定义而 rc≠0、ACP worker 通知静默失效的问题；保持平台写与通知能力不变，行数门禁不变。

## 实现方案

在 `cmd_comment()` 的两处 `python3 -c` 插值中，同行把 `${PROJECT_ROOT}` 替换为已全局定义的 `${SELF_ROOT}`。共 2 行、4 处引用；不新增行、不改接口、不改门禁。

## Dev-Loop Handoff

1. 先按 `verification/pre-tests.md` 跑 AT-001，确认 develop 基线 RED 并留证。
2. 实施同行变量替换，不动其它代码。
3. 跑 AT-001 GREEN、`bash -n` 语法检查、`bin/test-all --ci`。
4. test-pre-merge 工位 merge 后重跑 test-gate，再走 pr-create / pr-review / pr-merge / wt-close。

## 非目标

- 不改平台写逻辑、adapter、`agent_working` 接口。
- 不新增根路径变量、不上调 `.size-budget`。
- 不修其它 `PROJECT_ROOT` 用法（不同 scope）。
