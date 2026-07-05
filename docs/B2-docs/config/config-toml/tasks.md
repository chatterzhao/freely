# Tasks: config.toml.example overhaul + init + merge lock
- issue_id: I-20260630T224941Z-A

## Task 1: config.toml.example 修订
- 文件: `templates/config.toml.example`
- 移除 IFLOW_MAX_TURNS (已失效)
- 标记 AI_TOOL 已废弃
- 修正 7 个默认值对齐代码
- 新增 AI_TOOL_CAPABILITIES, AI_TOOL_POLICY, FREELY_ACP_*_BIN
- 所有注释去除代码引用
- 依赖: Subagent 字段研究

## Task 2: init 自动创建 config.toml
- 文件: `docs/system/workspace/scripts/runtime/freely` (cmd_init)
- 新增 config.toml 自举逻辑: 复制 example → 代填已知值
- --reset: 备份(时间戳) + 覆盖
- --auto: 跳过确认; 无 --auto: y/N 30s 超时
- 依赖: Task 1

## Task 3: merge lock 死锁诊断
- 文件: `docs/system/workspace/scripts/worktree/pr-merge-guarded`
- 写 PID 到锁目录
- 等待时检查进程存活
- 存活→提示等待; 已死→死锁警告+清理指引
- 依赖: 无

## Task 4: 更新 epics-map.svg
- 文件: `docs/epics-map.svg`
- 新增 config-toml-example epic + overhaul story
- 依赖: Task 1-3

## Task 5: RED+GREEN 验证
- 执行 pre-tests.md 全部 acceptance items
- 依赖: Task 1-4
