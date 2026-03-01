# STORY

## Active Stories
- STORY-002: BMAD文档门禁自动化（已完成）
- STORY-003: pre-develop测试门禁与pre-push回归测试（进行中）

## STORY-002
### 背景
当前文档链路不完整且有占位符，无法稳定支持自治循环。

### Traceability
Intent -> PRD -> EPIC -> STORY -> Code/Test

### 领地边界（Territory）
- 文档领地：`docs/brainstorms/BRAINSTORM.md`、`docs/planning/PRD.md`、`docs/planning/EPIC.md`、`docs/planning/STORY.md`、`docs/continuity/PROGRESS.md`、`docs/continuity/RECOVERY.md`
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

## STORY-003
### 背景
当前流程需满足“先测试后集成”的要求：本项目只允许变更先进入`pre-develop`验证，不允许直接推送/合并到`develop`。现有hook仅保护`main`，需补齐`develop`门禁并提供可复现测试。

### Traceability
Intent -> PRD -> EPIC -> STORY -> Code/Test

### 领地边界（Territory）
- 文档领地：`docs/brainstorms/BRAINSTORM.md`、`docs/planning/PRD.md`、`docs/planning/EPIC.md`、`docs/planning/STORY.md`、`docs/CONSTITUTION.md`、`README.md`
- 代码领地：`.githooks/pre-push`、`bin/test-pre-push-hook`
- 冲突敏感文件：`docs/CONSTITUTION.md`、`.githooks/pre-push`
- 合并路径：`feature/story-003-predevelop-gate -> pre-develop`（禁止直合`develop`）

### ORE-Test（文档阶段先验测试）
1. ORE-001（规则一致性）：
   - O: 宪法、STORY、hook文案都声明“禁止推送develop，测试走pre-develop”。
   - R: 任一文档未更新会导致执行冲突。
   - E: 通过`rg -n "pre-develop|develop"`检查关键文件一致性。
2. ORE-002（main保护不回归）：
   - O: 新增develop门禁不应破坏main门禁。
   - R: 条件判断重构后可能误放行main。
   - E: 回归测试必须包含main阻断用例。
3. ORE-003（feature正常放行）：
   - O: feature推送不应被误拦截。
   - R: 规则过严会阻断日常开发流。
   - E: 回归测试包含feature放行用例。

### 验收标准
1. `.githooks/pre-push`阻止`main`与`develop`直推，且输出策略来源。
2. `bin/test-pre-push-hook`执行通过，覆盖ORE-002/003与develop阻断用例。
3. 文档和README明确“先合并到pre-develop做测试，再决定是否进入develop”。

### 开发后补充测试用例
- T-003-01: 空输入（无ref行）应返回0。
- T-003-02: `remote_ref=refs/heads/develop`时返回非0。
- T-003-03: `local_ref=refs/heads/develop`时返回非0。
- T-003-04: `main`推送在无`FREELY_ALLOW_MAIN_PUSH=1`时返回非0。
- T-003-05: `feature/*`推送返回0。
- T-003-06: `main`推送在`FREELY_ALLOW_MAIN_PUSH=1`时返回0（保留应急通道）。

### 依赖
- 宪法第2章（分支与worktree）
- 宪法第10章（文档纪律）
- 宪法第11章（子代理不可用时需记录串行回退）
