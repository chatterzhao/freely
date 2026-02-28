# 文档结构说明

本项目遵循宪法约束下的 BMAD 文档工程。

## 可追溯链路
每个非 trivial 变更必须可追溯：

Intent -> PRD -> EPIC -> STORY -> Code/Test

## 基线文档
- `CONSTITUTION.md`：硬约束与治理规则
- `PROJECT_INTENT.md`：项目目标与运行模型
- `PRD.md`：需求目标、范围、验收标准
- `EPIC.md`：EPIC 级拆分
- `STORY.md`：可执行 STORY 与验收标准
- `PRE_TEST.md`：开发前测试设计与门禁用例（必需）
- `PROGRESS.md`：周期进展与连续性记录
- `RECOVERY.md`：阻塞/崩溃恢复检查点
- `brainstorm/`：Brainstorm 记录
- `review/`：评审记录

## 执行顺序
1. 先 Brainstorm
2. 再 PRD/EPIC/STORY
3. 开发前先写 `PRE_TEST.md`
4. 通过 `freely doctor` 文档门禁
5. 再进入开发与测试
