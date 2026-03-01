# 文档结构说明

本项目遵循宪法约束下的 BMAD 文档工程，并采用可扩展目录模型。

## 可追溯链路
每个非 trivial 变更必须可追溯：

Intent -> PRD -> EPIC -> STORY -> Code/Test

## 基线文档与目录
- `CONSTITUTION.md`：硬约束与治理规则（治理入口）
- `PROJECT_INTENT.md`：项目目标与运行模型（治理入口）
- `planning/PRD.md`：需求目标、范围、验收标准
- `planning/EPIC.md`：跨 EPIC 的索引/总览
- `planning/STORY.md`：跨 STORY 的索引/当前执行入口
- `validation/PRE_TEST.md`：开发前测试设计与门禁用例（必需）
- `continuity/PROGRESS.md`：全局连续性主记录（source of truth）
- `continuity/RECOVERY.md`：阻塞/崩溃恢复检查点
- `brainstorms/`：Brainstorm 记录（集合目录）
- `reviews/`：评审记录（集合目录）
- `progress/`：按 EPIC 归档的周期进度历史（集合目录）
- `epics/`：按 `epic-slug` 拆分的 EPIC 资产（替代旧 `bmad/`）

## 目录职责分工
- `continuity/PROGRESS.md` 负责“当前状态”和“下一步”。
- `progress/<epic-slug>/...` 负责“历史周期明细”和可审计追踪。
- `epics/<epic-slug>/` 负责该 EPIC 的目标、分解、故事清单与资产。
- `epics/<epic-slug>/progress.md` 可以存在，但仅作为摘要；不得替代 `continuity/PROGRESS.md` 与 `progress/*`。

## 执行顺序
1. 先 Brainstorm
2. 再 PRD/EPIC/STORY（并落到对应 epic 目录）
3. 开发前先写 `validation/PRE_TEST.md`
4. 通过 `freely doctor` 文档门禁
5. 再进入开发与测试
