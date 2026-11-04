# Implementation Decision Note

- issue_id: I-20261104T074512Z-A

## Decision
在 `bin/freely-package` 内新增 `refuse_dangerous_output()`，在 `validate_version` 之后、`rm -rf "$OUTPUT"` 之前调用。

## Why
- 参数解析阶段（`:46-52`）还拿不到默认输出路径（`:57-59` 才补齐）；放在版本校验之后可同时覆盖显式传参与默认值。
- 守卫是独立函数，可被测试静态断言存在性与顺序，也便于后续复用。

## Alternatives
- 在 `--output` 解析分支直接校验：无法覆盖默认路径，且会与后续逻辑重复判断。
- 引入独立校验脚本：为单点修复增加进程开销，不必要。

## Risks
- 白名单 `$HOME/.freely/versions/` 可能限制既有的外部输出用法；用 `FREELY_PACKAGE_ALLOW_OUTSIDE=1` 保留逃生门。
- 危险目标在测试中只做静态断言，不做真实删除；行为验证依赖安全路径实跑。
