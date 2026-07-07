# tasks: 封装命令文档系统化

- issue_id: I-20260706T232728Z-A
- created_at: 2026-07-06

## Task 1: 新建 `docs/system/workspace/commands.md` 封装命令权威参考

- **文件**: `docs/system/workspace/commands.md`（新建）
- **内容**:
  - 为什么用封装命令（每个命令封装了多个步骤）
  - 7 个封装命令的完整参考（语法、封装步骤、使用场景）
- **验证**: AT-006, AT-007
- **状态**: pending

## Task 2: 增强 AGENTS.md 速查表

- **文件**: `AGENTS.md`（修改）
- **改动**:
  - 将现有"场景→正确命令→禁止"表改为"你想做什么→用这个命令→它封装了什么→禁止"
  - 保持"禁止操作"区的已有门禁约束不变
- **验证**: AT-001, AT-007
- **状态**: pending

## Task 3: SKILL.md 添加意图→命令速查章节

- **文件**: `docs/system/workspace/skills/freely-workflow-guarded-execution/SKILL.md`（修改）
- **改动**:
  - 在铁律区域（"硬性规则"）之前新增"意图→命令速查"章节
  - 用表格形式：意图 | 正确做法 | 错误做法 | 原因
- **验证**: AT-002, AT-007, AT-008
- **状态**: pending

## Task 4: .githooks/bin/gh 拦截消息增强

- **文件**: `.githooks/bin/gh`（修改）
- **改动**:
  - `pr create` 拦截消息：加"为什么"（封装了 pull develop、dry-run gate、push、双平台 PR）
  - `pr merge` 拦截消息：加"为什么"（封装了 PR gate、promotion gate、双平台同步）
  - `issue close/reopen` 拦截消息：加"为什么"（封装了双平台同步）
- **验证**: AT-003, AT-007
- **状态**: pending

## Task 5: .githooks/pre-commit.sh 拦截末尾流程提示

- **文件**: `.githooks/pre-commit.sh`（修改）
- **改动**:
  - 在 develop 分支拦截消息末尾增加正向引导：
    - "你刚才想做的是 git commit → 对应封装命令是 freely pr-create-guarded"
    - 完整流程概览链接
- **验证**: AT-004
- **状态**: pending

## Task 6: .githooks/pre-push.sh 拦截末尾流程提示

- **文件**: `.githooks/pre-push.sh`（修改）
- **改动**:
  - 在 pr-create-guarded 未执行时的 push 拦截消息中增加正向引导
  - 提示正确命令和流程
- **验证**: AT-005
- **状态**: pending

## Task 7: 一致性校验 + deploy-skills

- **操作**:
  - 交叉 grep 确保所有位置命令名一致（AT-007）
  - 执行 `freely deploy-skills` 确保 SKILL.md 语法正确（AT-008）
- **验证**: AT-007, AT-008
- **状态**: pending

## 依赖

Task 1-6 互相独立，可并行执行。Task 7 依赖 Task 1-6 完成。
