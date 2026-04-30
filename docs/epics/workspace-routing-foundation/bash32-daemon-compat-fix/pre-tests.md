# Pre-tests — bash 3.2 daemon 兼容性修复

- issue_id: `I-20260429-1745-A`
- issue_path: `docs/epics/workspace-routing-foundation/bash32-daemon-compat-fix/issues/I-20260429-1745-A.md`

## 验收项

1. daemon 启动：`./bin/freely daemon start --project <path>` 在 bash 3.2 上正常启动，不自杀
2. supervisor 稳定性：运行 30s 无 restart loop，lifecycle trace 显示 L010→L020→L040 完整通过
3. 回归：`bash -n docs/system/workspace/scripts/runtime/freely` 语法检查通过
4. 回归：`./bin/governance-check` 无新增错误
