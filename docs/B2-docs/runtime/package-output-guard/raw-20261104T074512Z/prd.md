# PRD: freely-package 输出路径安全守卫

- issue_id: I-20261104T074512Z-A

## Goal
`freely-package` 在删除旧输出之前，拒绝 `/`、`$HOME`、`..` 以及解析后落在系统根或用户主目录的目标；默认只允许写入 `$HOME/.freely/versions/`，外部目录需显式放行。

## Modules
- `bin/freely-package`：新增 `refuse_dangerous_output()`，在 `validate_version` 之后、`rm -rf` 之前调用。
- `docs/system/workspace/scripts/tests/test-freely-package-output-guard`：守卫存在性、执行顺序、危险模式覆盖、安全路径实跑。

## Invariants
- 缺省输出仍为 `$HOME/.freely/versions/$VERSION`。
- 安全路径的打包产物与行为不变。
- allowlist 与版本校验逻辑不变。

## Non-Goals
- 不实现 `--dry-run`（后续独立事项）。
- 不改 allowlist、不改打包内容、不改版本命名规则。
- 不处理 `--output ""`（已有默认目录兜底）。

## Eval Plan
- unit：守卫存在、顺序在 rm 之前、三类危险模式被覆盖、拒绝文案存在。
- integration：安全目标在临时目录完成打包。

## Dev-Loop Handoff
RED：守卫缺失时测试失败（已复现）。实现后 GREEN。
