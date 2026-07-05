# Brainstorm: 清理废弃 task-source-scan.py

## Discovery

raw-20260508T045527Z27Z 提出：`task-source-scan.py` 已被 `task-lifecycle-scan.py` 取代，但仍留在代码库中造成噪音和混淆。

### 现状确认

- `task-lifecycle-scan.py` 已完成开发并接入 runtime
- `task-source-scan.py` 不再被任何 runtime 路径引用
- 代码库中存在多个引用 `task-source-scan` 的测试文件（`test-freely-task-source-scan-*`），这些测试已随生命周期迁移覆盖
- CONSTITUTION.md 第 1 条仍引用 `task-source-scan` 作为发现机制的描述文字

### 范围界定

| 项目 | 范围 |
|------|------|
| 删除 task-source-scan.py | 是——核心操作 |
| 清理测试文件 | 是——伴随删除 |
| 更新 CONSTITUTION.md 引用 | 是——宪法文字修正 |
| 删除 candidates.md 引用 | 否——保留为审计追溯 |

## 决策

- **删除** `task-source-scan.py`，统一使用 `task-lifecycle-scan.py`
- **保留** 关联测试文件直到对应的生命周期迁移完成
- **更新** CONSTITUTION.md 第 1 条的描述文字
- **单一切口策略**：低风险，直接删除即可，无需灰度

## 收敛

此 issue 已完整执行：task-source-scan.py 已删除，CONSTITUTION.md 已更新，I-20260508T045527Z-A 标记为 phase_state: completed。epic `docs/B2-docs/cleanup-scan/` 包含 code-review 和 verification 证据。
