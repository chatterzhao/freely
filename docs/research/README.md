# Research Workspace

当前阶段采用 Freely 最小治理面，只保留：

- `docs/PROJECT_INTENT.md`
- `docs/LAWS.md`
- `docs/CONSTITUTION.md`
- `docs/research/`

## 目标

先用研究驱动重构，避免在目录模型未定前继续扩展执行态文档。

## 目录约定

- `../pre-brainstorms/`: 新的 pre-brainstorm 主目录（按 `<id>/brainstorms.md + candidates.md` 组织）
- `deferred/`: 暂存历史文档资产，等待基于意图/法律/宪法讨论后重构
- `README.legacy.md`: 旧文档入口说明（保留供迁移参考）

## 规则

1. 未完成新文档模型讨论前，不在 `deferred/` 内继续追加执行态流程文档。
2. 新讨论、新决策优先写入 `docs/pre-brainstorms/<id>/`。
3. 当新模型达成后，再从 `deferred/` 选择性迁移到新结构。

## Skills 设计速记清单（防遗忘）

以下理念在设计任意 loop skill 时都应简洁对齐：

1. 宪法/法律优先于实现细节（先对齐约束，再写 skill 逻辑）。
2. Ring 与 SSOT：事实冲突时必须有单一事实源决议路径。
3. 文档自包含：产物应可独立消费，减少隐式依赖。
4. 验收先行：验收标准要可执行，优先保证集成跑通。
5. AI 自治优先：先保证闭环稳定可恢复，再优化局部质量。
6. `必须经过` 属于架构 enforcement；`怎么做` 属于 skill policy。
7. 文档写入统一通过文档 skill + write gateway + 审计记录。
