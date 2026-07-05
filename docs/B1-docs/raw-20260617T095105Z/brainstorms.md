# Brainstorm: A2A-Native Delegation

## Discovery

### 当前问题
Manager-Worker 委派使用 CSV 文件路径中转:
1. Manager AI 写 prompt 文件 → a2a-exit --workers=path1,path2 (CSV)
2. CSV 存入 A2A Task 的 worker_prompts_csv 字段
3. freely runtime 读 CSV → 打开文件 → 启动 Worker

问题:
- CSV 不是 A2A 标准字段，JSON-RPC handler 会丢弃
- 文件路径在项目根/工位间不一致
- 两层存储(prompt 文件 + A2A Task)容易不同步
- 需要 _rest_request 绕过 JSON-RPC 来保留该字段(额外复杂度)

### 行业参考
- **Routa**: Coordinator 通过 createTask(message=story_yaml) 委派, Task.message 承载完整规范
- **A2A 标准**: tasks/send 的 message 字段承载任务内容, Task state 机管理生命周期
- **JiuwenSwarm**: Leader 直接创建 Task, Teammate 查询并执行

### 核心洞察
A2A Task 的 message 字段就是为承载委派内容设计的。不需要额外的 CSV 层。
Worker prompt 文件可以从 Task.message 动态生成,不需要持久化文件路径。

## Decision

**Promote**. 彻底消除 worker_prompts_csv 字段和 CSV 中转机制,改用 A2A Task.message 原生委派。
