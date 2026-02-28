# STORY

## Active Stories
- STORY-002: BMAD文档门禁自动化

## STORY-002
### 背景
当前文档链路不完整且有占位符，无法稳定支持自治循环。

### Traceability
Intent -> PRD -> EPIC -> STORY -> Code/Test

### 领地边界（Territory）
- 文档领地：`docs/brainstorm/BRAINSTORM.md`、`docs/PRD.md`、`docs/EPIC.md`、`docs/STORY.md`、`docs/PROGRESS.md`、`docs/RECOVERY.md`
- 代码领地：`bin/bmad-check`、`README.md`
- 冲突敏感文件：`README.md`
- 合并路径：`feature/story-002-bmad-cycle -> pre-develop`（禁止直合`develop`）

### 验收标准
1. `bin/bmad-check`可以检查BMAD关键文档存在性、占位符与关键章节。
2. 脚本失败时明确打印文件级问题列表并返回非0。
3. README包含执行示例，开发者可在本地复现检查流程。

### 验证方式
- 正向：执行`bin/bmad-check`应成功。
- 反向：临时制造占位符应触发失败（验证后恢复）。

### 依赖
- 宪法第10章（BMAD纪律）
- 宪法第12章（Territory并行开发）
