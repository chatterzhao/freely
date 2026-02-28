# PRD

## 问题
当前BMAD核心文档普遍为占位内容，缺少可执行校验机制，导致“先文档后开发”和“可追踪变更链路”难以被持续执行。

## 目标
1. 建立完整且中文化的BMAD链路文档（Brainstorm/PRD/EPIC/STORY）。
2. 提供可执行脚本，校验文档完整性与Traceability最低要求。
3. 将校验流程纳入项目README，支持本地日常执行。

## 范围
- 新增`bin/bmad-check`脚本。
- 更新`docs/PRD.md`、`docs/EPIC.md`、`docs/STORY.md`、`docs/PROGRESS.md`、`docs/RECOVERY.md`、`docs/brainstorm/BRAINSTORM.md`。
- 更新根目录`README.md`的执行指引。

## 非目标
- 不在本轮实现完整CI流水线。
- 不在本轮实现多项目调度器或Tauri/Rust主程序。

## 验收标准
1. 运行`bin/bmad-check`返回成功，并输出检查摘要。
2. 若文档包含TBD占位符或缺关键章节，脚本返回非0并提示具体文件。
3. 文档中存在清晰映射：Intent -> PRD -> EPIC -> STORY -> Code/Test。
