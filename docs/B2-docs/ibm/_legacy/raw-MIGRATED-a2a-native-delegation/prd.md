# PRD: A2A-Native Delegation

## Goal
消除 Manager-Worker 委派中的 CSV 文件路径中转，改用 A2A Task.message 承载完整任务内容。

## Current vs Target

### Current (CSV)
```
Manager → 写 prompt 文件 → a2a-exit --workers=path1,path2
       → worker_prompts_csv ∈ A2A Task
       → runtime 读 CSV → 开文件 → 启 Worker
```

### Target (A2A-native)
```
Manager → a2a-exit --state=submitted --message="完整指令"
       → A2A Task.message = 完整委派内容
       → runtime: tasks/list --state=submitted
       → 读 task.message → 生成 prompt → 启 Worker
```

## Design Decisions

1. **Task.message 承载完整内容**: 对标 Routa createTask(message=story_yaml)
2. **动态生成 prompt file**: Worker 启动时从 Task.message 生成,不持久化路径
3. **tasks/list 替代 CSV**: runtime 委派检测改为查询 A2A tasks
4. **消除 worker_prompts_csv**: 所有引用改为 task.message

## Affected Files
- freely (runtime): 委派检测 + Worker 启动逻辑
- a2a_task.py: a2a-exit 参数变更
- a2a_server.py: 无(已有字段足够)
- manager-agent.md: prompt 模板更新
