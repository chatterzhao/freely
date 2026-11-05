---
issue_id: I-20261104T074512Z-A
issue_path: docs/B2-docs/runtime/package-output-guard/raw-20261104T074512Z/issues/I-20261104T074512Z-A.md
phase_state: completed
---

- issue_id: I-20261104T074512Z-A
- issue_path: docs/B2-docs/runtime/package-output-guard/raw-20261104T074512Z/issues/I-20261104T074512Z-A.md

## Implementation Decision Note

- decision: 在 `bin/freely-package` 内新增 `refuse_dangerous_output()`，在 `validate_version` 之后、`rm -rf` 之前调用。
- why_this: 参数解析阶段还拿不到默认输出路径（`:57-59` 才补齐），放在版本校验之后可同时覆盖显式传参与默认值；守卫是独立函数，便于测试断言与复用。
- alternatives_considered: 在 `--output` 解析分支直接校验（无法覆盖默认路径且重复判断）；引入独立校验脚本（为单点修复增加进程开销）。
- boundary_non_goals: 不实现 `--dry-run`；不改 allowlist；不改默认输出路径；不处理 `--output ""`。
- residual_risk: 白名单 `$HOME/.freely/versions/` 可能限制既有外部输出用法，需 `FREELY_PACKAGE_ALLOW_OUTSIDE=1` 放行；危险目标仅做静态断言，行为验证依赖安全路径实跑。
